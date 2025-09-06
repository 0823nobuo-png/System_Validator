# System Validator / Theaterverse Final
仕様書: Mistral-7B Shared Instance 構成

---

## 概要
- **目的**: mistral:7b を単一インスタンスとして両システムで共用する。
- **方式**: プラグイン `plugin_llm_mistral7b` がアダプタを通じて呼び出し、排他制御で共用。
- **利用場面**: AI 物語生成システムにおけるセンターユニット共通基盤。

## 設計要点
1. **構成共有仕様 (C01)**
   - mistral:7b を一元起動。
   - 複数プロセスから共用。
2. **起動と連携手順書 (C02)**
   - 起動スクリプトで環境変数を設定。
   - API 接続で LLM 呼び出し。
3. **競合リスクと安全対策 (C03)**
   - Lock ファイルで実行衝突防止。
   - GPU/CPU リソース競合を制御。
4. **呼び出し抽象化 (C04)**
   - Adapter 層で将来のエンジン変更に対応。
   - OpenAI API や llama.cpp にも移行可能。
5. **排他制御・ステータス監視 (C05)**
   - lock ファイルと DB ステータス管理。
   - 使用中可視化。
6. **Web UI での使用中可視化 (C06)**
   - 5秒ごと更新。
   - plugin_ui_console に統合。
7. **使用履歴の DB 保存と分析 (C07)**
   - プロンプトと結果を DB に保存。
   - 分析可能に。
8. **統合テスト計画 (C08)**
   - 競合テスト、ログ連動性検証。

## 実装ポイント
- `plugin_llm_mistral7b` 内に adapter/config を整備。
- 共用 lock 制御は `db/plugin_registry` に保存。
- UI コンソールから利用状況を確認。

## 運用
- **OneClick 起動**時に mistral:7b が自動起動。
- **Blue/Green 切替**対象外（共有のため常時稼働）。

## 強化提案
- 今後は Qwen 系と統合した「動的 LLM プール」化を検討。
- GPU 割当の動的最適化。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_spec_mistral7b_shared.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_spec_mistral7b_shared.md
--- END OF STRUCTURE ---
