# SystemValidator Verification Kit（実ファイル徹底検証用）

あなたのローカルに保持している **System Validator / Theaterverse Final** 一式を走査して、
以下の検証成果物を自動生成します（Ubuntu 22.04 LTS 想定／Python 3 標準ライブラリのみ）。

- `manifest.json` … すべてのファイルのパス・サイズ・更新時刻・SHA256・ルール適合状況
- `root_current.txt` … `<path>\t<size>` 形式のツリー出力（`root.txt` 互換）
- `checksums.sha256` … 全ファイルの SHA256
- `lint_report.md` … ルール違反（命名／終端記述／正式パス表記／SQLite禁止／PEP420）
- `rule_violations.json` … 機械可読な違反サマリ
- `duplicates_report.txt` … プロジェクト内のベース名重複
- `diffs/added.txt` / `diffs/removed.txt` … 既存の `root.txt` との差分（任意）

## 準拠ルール（会話5〜7 / docs）
- **命名**: `<ユニット>_<機能>.<拡張子>`、区切りは `_` のみ、`.` は拡張子前のみ
- **重複禁止**: 同一プロジェクトでファイル名は一意
- **PEP 420**: `__init__.py` を禁止（暗黙ネームスペース）
- **終端記述**: 非JSONは末尾の最終非空行に `--- END OF STRUCTURE ---`
- **JSON**: 以下のどちらかを満たす
  - 末尾に `// --- END OF STRUCTURE ---`（コメント）
  - 厳密JSONが必要な場合は `__file_path__` フィールドを持つ
- **正式パス表記**: 末尾近傍（最終10行目目安）に `/System_Validator/APP_DIR/` を含む
- **SQLite禁止**: `sqlite` / `sqlite3` の参照を検出した場合は要修正

## 使い方
```bash
# 1) 任意フォルダに 3 ファイルを配置
mkdir -p ~/SystemValidator_VerificationKit
# （本キャンバスの 3 ファイルをコピー＆保存）

# 2) プロジェクトのルート（/root/System_Validator/APP_DIR/... の起点）へ移動
cd /path/to/your/project/root

# 3) OneClick 実行
chmod +x ~/SystemValidator_VerificationKit/verificationkit_run_all.sh
~/SystemValidator_VerificationKit/verificationkit_run_all.sh .  baseline/root.txt   # ベースライン無しなら第2引数省略
```

### 生成物（アップロード依頼）
- `_validator_outputs/root_current.txt`
- `_validator_outputs/manifest.json`
- `_validator_outputs/lint_report.md`
- `_validator_outputs/rule_violations.json`
- `_validator_outputs/duplicates_report.txt`
- `_validator_outputs/checksums.sha256`
- `_validator_outputs/diffs/*`（baseline 指定時）

### 備考
- 文字コードは UTF-8。
- バイナリはテキスト検査対象外（SHA256のみ）。
- JSON の厳密性と末尾コメントの併用は困難なため、**どちらか**を満たせば合格。
- `/root/` は環境依存で可変ですが、パス表記は `/root/System_Validator/APP_DIR/` 基点を推奨。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/tools/VerificationKit/verificationkit_readme.md -->

