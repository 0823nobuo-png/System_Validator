#!/usr/bin/env python3
"""
SystemValidator Verification Kit - SAFE MODE (v2)
- Accepts commented END markers for code files
- Whitelists common standard filenames for naming rule
- Skips END marker & formal path checks for non-text/binary files

Outputs (_validator_outputs under --root):
- manifest.json, root_current.txt, checksums.sha256
- lint_report.md, rule_violations.json, duplicates_report.txt
- diffs/* (if baseline provided)

Usage:
  python verificationkit_validator_scan_safe2.py --root <project_root> [--baseline <root.txt>]
"""
import os, sys, argparse, hashlib, json, re
from datetime import datetime
from pathlib import Path

NAMING_REGEX = r'^[A-Za-z0-9]+_[A-Za-z0-9_]+'
END_MARKER = '--- END OF STRUCTURE ---'
EXCEPT_BASENAMES = {'.env', '.env.example', 'requirements.txt'}

COMMENTED_END_PATTERN = re.compile(r"^\s*(#|//)\s*---\s*END\s*OF\s*STRUCTURE\s*---\s*$")
BLOCK_END_PATTERN = re.compile(r"^\s*/\*\s*---\s*END\s*OF\s*STRUCTURE\s*---\s*\*/\s*$")

HASH_STYLE_EXTS  = {'.py','.sh','.sql','.yml','.yaml','.ini','.env','.cfg','.conf','.service'}
SLASH_STYLE_EXTS = {'.ts','.tsx','.js'}
RAW_STYLE_EXTS   = {'.md','.txt'}


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def sniff_is_text(path: Path, max_bytes=4096) -> bool:
    try:
        with path.open('rb') as f:
            chunk = f.read(max_bytes)
        return b'\x00' not in chunk
    except Exception:
        return False


def read_tail_lines_utf8(path: Path, n=15):
    if not sniff_is_text(path):
        return []
    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            return [ln.rstrip('\n') for ln in f.readlines()[-n:]]
    except Exception:
        return []


def check_json_rules(path: Path, tail_lines):
    res = {'is_json': False, 'json_comment_end_ok': False, 'json_has_file_path': False, 'json_parse_ok': False}
    if path.suffix.lower() != '.json':
        return res
    res['is_json'] = True
    if any(END_MARKER in ln and '//' in ln for ln in tail_lines):
        res['json_comment_end_ok'] = True
    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.splitlines()
        while lines and (lines[-1].strip().startswith('//') or lines[-1].strip() == '' or lines[-1].strip().startswith('<!--') or lines[-1].strip() == '-->'):
            lines.pop()
        obj = json.loads('\n'.join(lines))
        res['json_parse_ok'] = True
        if isinstance(obj, dict) and '__file_path__' in obj:
            res['json_has_file_path'] = True
    except Exception:
        pass
    return res


def end_marker_ok_for_text(path: Path, tail_lines, is_json, json_comment_ok, json_has_file_path) -> bool:
    if is_json:
        return json_comment_ok or json_has_file_path
    # Non-JSON text: last non-empty line must be raw or commented END
    last = None
    for ln in reversed(tail_lines):
        if ln.strip():
            last = ln.strip()
            break
    if not last:
        return False
    if last == END_MARKER:
        return True
    if COMMENTED_END_PATTERN.match(last):
        return True
    if BLOCK_END_PATTERN.match(last):
        return True
    return False


def check_naming_rule(path: Path) -> bool:
    base = path.name
    if base in EXCEPT_BASENAMES:
        return True
    if '.' not in base:
        return False
    stem = base.rsplit('.',1)[0]
    return re.match(NAMING_REGEX, stem) is not None


def has_formal_path_hint(tail_lines) -> bool:
    joined = '\n'.join(tail_lines)
    return '/System_Validator/APP_DIR/' in joined


def grep_forbidden_sqlite(path: Path) -> bool:
    if not sniff_is_text(path):
        return False
    try:
        txt = path.read_text('utf-8', errors='replace').lower()
        return ('sqlite' in txt or 'sqlite3' in txt)
    except Exception:
        return False


def build_tree_text(root: Path) -> str:
    out = []
    for dp, dns, fns in os.walk(root):
        if '_validator_outputs' in dp.split(os.sep):
            continue
        dns.sort(); fns.sort()
        rel_dir = os.path.relpath(dp, root)
        if rel_dir == '.':
            rel_dir = ''
        for name in fns:
            p = Path(dp) / name
            rel = str(Path(rel_dir) / name) if rel_dir else name
            try:
                size = p.stat().st_size
            except Exception:
                size = -1
            out.append(f"{rel}\t{size}")
    return '\n'.join(out)


def compute_diffs(current_paths_set, baseline_lines):
    base_paths = set()
    for ln in baseline_lines:
        p = ln.split('\t',1)[0].strip()
        if p:
            base_paths.add(p)
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
    violations = {'naming_rule': [], 'end_marker': [], 'formal_path_hint': [], 'forbidden_sqlite': [], 'pep420_init': []}
    sha_lines = []
    by_name = {}

    for dp, dns, fns in os.walk(root):
        if '_validator_outputs' in dp.split(os.sep):
            continue
        dns.sort(); fns.sort()
        for fn in fns:
            p = Path(dp) / fn
            rel = str(p.relative_to(root))
            by_name.setdefault(p.name, []).append(rel)

            try:
                st = p.stat(); size = st.st_size; mtime = datetime.fromtimestamp(st.st_mtime).isoformat()
            except Exception:
                size = -1; mtime = ''
            digest = ''
            try:
                digest = sha256sum(p)
            except Exception:
                pass

            is_text = sniff_is_text(p)
            tail = read_tail_lines_utf8(p, 15) if is_text else []
            jinfo = check_json_rules(p, tail)

            naming_ok = check_naming_rule(p)
            if not naming_ok:
                violations['naming_rule'].append(rel)

            # Non-text/binary files: skip both checks
            if not is_text:
                end_ok = True
                formal_ok = True
            else:
                end_ok = end_marker_ok_for_text(p, tail, jinfo['is_json'], jinfo['json_comment_end_ok'], jinfo['json_has_file_path'])
                formal_ok = has_formal_path_hint(tail)

            if not end_ok:
                violations['end_marker'].append(rel)
            if not formal_ok:
                violations['formal_path_hint'].append(rel)

            sqlite_bad = grep_forbidden_sqlite(p)
            if sqlite_bad:
                violations['forbidden_sqlite'].append(rel)
            if p.name == '__init__.py':
                violations['pep420_init'].append(rel)

            manifest.append({
                'path': rel, 'size': size, 'mtime': mtime, 'sha256': digest,
                'is_text': is_text,
                'is_json': jinfo['is_json'],
                'json_comment_end_ok': jinfo['json_comment_end_ok'],
                'json_has_file_path': jinfo['json_has_file_path'],
                'json_parse_ok': jinfo['json_parse_ok'],
                'end_marker_ok': end_ok,
                'naming_ok': naming_ok,
                'formal_path_hint_ok': formal_ok,
            })
            if digest:
                sha_lines.append(f"{digest}  {rel}")

    dups = {name: paths for name, paths in by_name.items() if len(paths) > 1}

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
    lint_md.append('# SystemValidator Lint Report (SAFE MODE v2)')
    lint_md.append('')
    lint_md.append(section('Naming Rule Violations', violations['naming_rule']))
    lint_md.append('')
    lint_md.append(section('Missing END Marker (raw or commented; text files only)', violations['end_marker']))
    lint_md.append('')
    lint_md.append(section('Missing Formal Path Hint (last ~10 lines; text files only)', violations['formal_path_hint']))
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

    print(f"[OK] SAFE v2 scan complete. Outputs in: {out_dir}")

if __name__ == '__main__':
    main()

# policy path hint:
# /root/System_Validator/APP_DIR/tools/VerificationKit/verificationkit_validator_scan_safe2.py
# --- END OF STRUCTURE ---
