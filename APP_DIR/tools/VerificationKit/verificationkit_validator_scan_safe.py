#!/usr/bin/env python3
"""
SystemValidator Verification Kit - SAFE MODE Scanner (ASCII only)
- Accepts commented END markers for code files
- Whitelists common standard filenames for naming rule

Outputs (_validator_outputs under --root):
- manifest.json, root_current.txt, checksums.sha256
- lint_report.md, rule_violations.json, duplicates_report.txt
- diffs/* (if baseline provided)

Usage:
  python verificationkit_validator_scan_safe.py --root <project_root> [--baseline <root.txt>]
"""
import os, sys, argparse, hashlib, json, re
from datetime import datetime
from pathlib import Path

NAMING_REGEX = r'^[A-Za-z0-9]+_[A-Za-z0-9_]+'
END_MARKER = '--- END OF STRUCTURE ---'
# Whitelisted standard filenames that should not count as naming violations
EXCEPT_BASENAMES = {'.env', '.env.example', 'requirements.txt'}

CODE_HASH_PREFIXES = {'#', '//'}
BLOCK_END_PATTERN = re.compile(r"^\s*/\*\s*--- END OF STRUCTURE ---\s*\*/\s*$")
COMMENTED_END_PATTERN = re.compile(r"^\s*(#|//)\s*--- END OF STRUCTURE ---\s*$")

COMMENT_STYLE = {
    # hash-style
    '#': {'.py', '.sh', '.sql', '.yml', '.yaml', '.ini', '.env', '.cfg', '.conf', '.service', '.txt', '.md'},
    # slash-slash style
    '//': {'.ts', '.tsx', '.js'}
}


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def is_text_file(path: Path, max_bytes=4096) -> bool:
    try:
        with path.open('rb') as f:
            sample = f.read(max_bytes)
        return b'\x00' not in sample
    except Exception:
        return False


def read_tail_lines(path: Path, n=15):
    if not is_text_file(path):
        return []
    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        return [ln.rstrip('\n') for ln in lines[-n:]]
    except Exception:
        return []


def check_json_rules(path: Path, tail_lines):
    res = {
        'is_json': False,
        'json_comment_end_ok': False,
        'json_has_file_path': False,
        'json_parse_ok': False,
    }
    if path.suffix.lower() != '.json':
        return res
    res['is_json'] = True

    joined_tail = '\n'.join(tail_lines)
    if END_MARKER in joined_tail and '//' in joined_tail:
        res['json_comment_end_ok'] = True

    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.splitlines()
        while lines and (lines[-1].strip().startswith('//') or lines[-1].strip().startswith('<!--') or lines[-1].strip().startswith('-->') or lines[-1].strip() == ''):
            lines.pop()
        content2 = '\n'.join(lines)
        obj = json.loads(content2)
        res['json_parse_ok'] = True
        if isinstance(obj, dict) and '__file_path__' in obj:
            res['json_has_file_path'] = True
    except Exception:
        res['json_parse_ok'] = False

    return res


def check_end_marker(path: Path, tail_lines, is_json, json_comment_end_ok, json_has_file_path):
    if is_json:
        return json_comment_end_ok or json_has_file_path

    # Non-JSON: accept either raw END_MARKER or a commented variant according to extension
    last_nonempty = None
    for ln in reversed(tail_lines):
        if ln.strip():
            last_nonempty = ln.rstrip()
            break
    if last_nonempty is None:
        return False

    if last_nonempty.strip() == END_MARKER:
        return True
    if COMMENTED_END_PATTERN.match(last_nonempty):
        return True
    if BLOCK_END_PATTERN.match(last_nonempty):
        return True
    return False


def check_naming_rule(path: Path):
    base = path.name
    if base in EXCEPT_BASENAMES:
        return True
    if '.' not in base:
        return False
    stem = base.rsplit('.', 1)[0]
    return re.match(NAMING_REGEX, stem) is not None


def find_formal_path_hint(tail_lines):
    joined_tail = '\n'.join(tail_lines)
    return ('/System_Validator/APP_DIR/' in joined_tail)


def grep_forbidden_sqlite(path: Path):
    if not is_text_file(path):
        return False
    try:
        txt = path.read_text('utf-8', errors='replace').lower()
        return ('sqlite' in txt or 'sqlite3' in txt)
    except Exception:
        return False


def build_tree_text(root: Path):
    output = []
    for dirpath, dirnames, filenames in os.walk(root):
        if '_validator_outputs' in dirpath.split(os.sep):
            continue
        dirnames.sort(); filenames.sort()
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == '.': rel_dir = ''
        for name in filenames:
            p = Path(dirpath) / name
            rel = str(Path(rel_dir) / name) if rel_dir else name
            try:
                size = p.stat().st_size
            except Exception:
                size = -1
            output.append(f"{rel}\t{size}")
    return '\n'.join(output)


def compute_diffs(current_paths_set, baseline_lines):
    base_paths = set()
    for ln in baseline_lines:
        part = ln.split('\t', 1)[0].strip()
        if part:
            base_paths.add(part)
    added = sorted(list(current_paths_set - base_paths))
    removed = sorted(list(base_paths - current_paths_set))
    return added, removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', help='Project root to scan')
    ap.add_argument('--baseline', default=None, help='Optional baseline root.txt to diff against')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[ERROR] root does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    out_dir = root / '_validator_outputs'
    out_dir.mkdir(exist_ok=True)

    manifest = []
    violations = {
        'naming_rule': [],
        'end_marker': [],
        'formal_path_hint': [],
        'forbidden_sqlite': [],
        'pep420_init': [],
    }
    sha_lines = []
    filename_to_paths = {}

    for dirpath, dirnames, filenames in os.walk(root):
        if '_validator_outputs' in dirpath.split(os.sep):
            continue
        dirnames.sort(); filenames.sort()
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = str(p.relative_to(root))

            filename_to_paths.setdefault(p.name, []).append(rel)

            try:
                stat = p.stat(); size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
            except Exception:
                size = -1; mtime = ''

            try:
                digest = sha256sum(p)
            except Exception:
                digest = ''

            tail_lines = read_tail_lines(p)
            json_info = check_json_rules(p, tail_lines)
            end_marker_ok = check_end_marker(p, tail_lines, json_info['is_json'], json_info['json_comment_end_ok'], json_info['json_has_file_path'])
            naming_ok = check_naming_rule(p)
            formal_path_ok = find_formal_path_hint(tail_lines)
            sqlite_bad = grep_forbidden_sqlite(p)

            if not naming_ok:
                violations['naming_rule'].append(rel)
            if not end_marker_ok:
                violations['end_marker'].append(rel)
            if not formal_path_ok:
                violations['formal_path_hint'].append(rel)
            if sqlite_bad:
                violations['forbidden_sqlite'].append(rel)
            if p.name == '__init__.py':
                violations['pep420_init'].append(rel)

            manifest.append({
                'path': rel, 'size': size, 'mtime': mtime, 'sha256': digest,
                'is_text': bool(tail_lines),
                'is_json': json_info['is_json'],
                'json_comment_end_ok': json_info['json_comment_end_ok'],
                'json_has_file_path': json_info['json_has_file_path'],
                'json_parse_ok': json_info['json_parse_ok'],
                'end_marker_ok': end_marker_ok,
                'naming_ok': naming_ok,
                'formal_path_hint_ok': formal_path_ok,
            })
            if digest:
                sha_lines.append(f"{digest}  {rel}")

    dups = {name: paths for name, paths in filename_to_paths.items() if len(paths) > 1}

    (out_dir / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (out_dir / 'root_current.txt').write_text(build_tree_text(root), encoding='utf-8')
    (out_dir / 'checksums.sha256').write_text('\n'.join(sha_lines), encoding='utf-8')
    (out_dir / 'rule_violations.json').write_text(json.dumps(violations, ensure_ascii=False, indent=2), encoding='utf-8')
    dup_lines = []
    for name, paths in sorted(dups.items()):
        dup_lines.append(f"{name}\t" + ' | '.join(paths))
    (out_dir / 'duplicates_report.txt').write_text('\n'.join(dup_lines), encoding='utf-8')

    def section(title, items):
        s = [f"## {title}"]
        if not items:
            s.append('- OK')
        else:
            for it in items:
                s.append(f"- {it}")
        return '\n'.join(s)

    lint_md = []
    lint_md.append('# SystemValidator Lint Report (SAFE MODE)')
    lint_md.append('')
    lint_md.append(section('Naming Rule Violations', violations['naming_rule']))
    lint_md.append('')
    lint_md.append(section('Missing END Marker (raw or commented)', violations['end_marker']))
    lint_md.append('')
    lint_md.append(section('Missing Formal Path Hint (last ~10 lines)', violations['formal_path_hint']))
    lint_md.append('')
    lint_md.append(section('Forbidden SQLite Mentions', violations['forbidden_sqlite']))
    lint_md.append('')
    lint_md.append(section('PEP 420 Violations (__init__.py found)', violations['pep420_init']))
    (out_dir / 'lint_report.md').write_text('\n'.join(lint_md), encoding='utf-8')

    if args.baseline:
        base_path = Path(args.baseline).expanduser().resolve()
        if base_path.exists():
            try:
                base_lines = base_path.read_text(encoding='utf-8', errors='replace').splitlines()
                current_set = set([m['path'] for m in manifest])
                added, removed = compute_diffs(current_set, base_lines)
                diffs_dir = out_dir / 'diffs'
                diffs_dir.mkdir(exist_ok=True)
                (diffs_dir / 'added.txt').write_text('\n'.join(added), encoding='utf-8')
                (diffs_dir / 'removed.txt').write_text('\n'.join(removed), encoding='utf-8')
            except Exception as e:
                (out_dir / 'diffs_error.txt').write_text(str(e), encoding='utf-8')

    print(f"[OK] SAFE scan complete. Outputs in: {out_dir}")

if __name__ == '__main__':
    main()

# policy path hint:
# /root/System_Validator/APP_DIR/tools/VerificationKit/verificationkit_validator_scan_safe.py
# --- END OF STRUCTURE ---
