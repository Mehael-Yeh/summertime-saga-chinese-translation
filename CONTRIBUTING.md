# 参与翻译

本项目是 [Summertime Saga](https://summertimesaga.com/) 的非官方简体中文翻译。仓库只包含翻译源、适配脚本和构建工具，不包含游戏本体。

## 开始之前

1. 确认你的改动面向哪个游戏版本。当前翻译只保证 `21.0.0-wip.7944` 可用，其他版本的行号和脚本可能不兼容。
2. 安装 Python 3.9 以上（仓库自带工具不依赖第三方库）。
3. 克隆仓库，不要直接把游戏本体提交进来。

## 翻译文件怎么改

- 译文位于 `tl/zh_hans/`，结构对应游戏脚本。只改 `new "..."` 里的中文，不要动 `old "..."`、变量、标签、缩进和翻译块 ID。
- 变量、占位符、格式标签必须原样保留；`{dom=强势}` 这类标签只汉化等号后的显示值。
- 中文与英文姓名、品牌、缩写之间不加空格，例如“我找Anon聊过了”。
- 不确定人名、地名、称呼、物品名怎么译时，先查 `translation_context/terminology.md`、`recurring_terms.md` 和 `characters.md`，不要另造新译法。
- 遇到同一表达在短距离内重复出现两次以上，先按 `translation_context/recurring_terms.md` 的触发规则做跨文件复查，再定译。

## 提交前必须跑的检查

```powershell
python tools/validate_translations.py --changed
python tools/audit_sentence_consistency.py --check-approved translation_context/sentence_patterns.json
python tools/audit_recurring_terms.py --changed --fail-on-mismatch
python tools/audit_mixed_spacing.py
python tools/audit_manual_coverage.py
git diff --check
```

改动译文后，`manual_review.json` 里的条目指纹会失效，`audit_manual_coverage.py` 会报告 STALE。需要同步刷新对应条目的哈希和阅读记录，具体做法见 `translation_context/index.md`。

如需在本地构建汉化包，见 `translation_context/release.md`。默认不要在提交里附带 `dist/zh_hans.rpa`。

## 提交信息与 PR

- 提交信息说明改了什么、面向哪些文件；一次 PR 聚焦一类改动（例如统一某个术语，或完成某一场景）。
- PR 描述里写清楚：涉及文件、改动原因、跑过的检查命令和结果。
- 新增或修改术语、句式基准时，同时更新 `translation_context` 下对应文件，并在 PR 里说明依据。
- CI 会运行与本地相同的审计；审计失败时先修复，不要用跳过检查的方式合并。

## 不要做的事

- 不要修改 `README.md`、`LICENSE` 或构建产物。
- 不要用全局查找替换处理重复词；相同英文在不同角色、关系阶段或语境下可以有不同的正确译法。
- 不要把开发占位符、内部字段或非玩家可见文本当对白翻译。
- 不要为通过校验而调整原文注释或删除翻译块；旧块清理必须以引擎报告的 orphan 清单为依据。

## 术语与风格参考

| 文件 | 内容 |
| --- | --- |
| `translation_context/index.md` | 目录说明与维护流程 |
| `translation_context/style_guide.md` | 行文、标点、标签与语气规范 |
| `translation_context/terminology.md` | 人名、地名、专名与固定译法 |
| `translation_context/characters.md` | 角色语气档案 |
| `translation_context/recurring_terms.md` | 重复称呼与句式基准边界 |
| `translation_context/storylines.md` | 剧情线与分支事实 |
| `translation_context/release.md` | 版本兼容与发版流程 |
