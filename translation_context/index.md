# translation_context 目录说明

更新时间：2026-10-05

本目录保存翻译规范、术语、剧情背景和审校记录，不参与游戏打包。所有内容以当前工作区为准；修改译文后必须同步更新对应记录，否则校验工具会报告过期。

## 文件清单

| 文件 | 类型 | 内容 | 维护方式 |
| --- | --- | --- | --- |
| `AGENTS.md` | Agent交付规范 | 新会话必读顺序、增量翻译流程、记录输出和交付检查 | 完整规范唯一出处，根目录入口引用本文件 |
| `index.md` | 索引 | 目录用途、文件分工、工作流 | 增删文件时同步 |
| `style_guide.md` | 规范 | 中文行文、标点、标签、口语与语气要求 | 出现新的通用规则时追加 |
| `terminology.md` | 规范 | 人名、称谓、专名、固定译法 | 新增术语必须登记 |
| `characters.md` | 背景 | 角色档案与说话风格 | 角色理解变化时更新 |
| `storylines.md` | 背景 | 剧情线、场景链、分支事实 | 场景核对完成后更新 |
| `progress.md` | 记录 | 各批次修复进度与验收口径 | 每批完成后追加 |
| `file_inventory.md` | 记录 | plot 文件清单与覆盖统计 | 覆盖口径变化时更新 |
| `recurring_terms.md` | 记录 | 重复称呼、口癖、专名复查 | 与 `recurring_terms.json` 配套 |
| `english_residuals.md` | 记录 | 英文残留与非英语例外判定 | 出现新例外时更新 |
| `input_codes.md` | 规范 | 游戏内可输入代码与翻译兼容 | 新增密码类文本时更新 |
| `release.md` | 规范 | 版本兼容矩阵、发版检查清单、上游更新流程 | 版本或发布流程变化时更新 |
| `mod_review_history.json` | 历史记录（机器） | 已移出翻译审计的Mod审校历史 | 不作为当前翻译覆盖，Mod验证另行记录 |
| `manual_review.json` | 记录（机器） | 每文件人工审校台账：逐条指纹、当前覆盖状态与未结项，不写批次历史 | 由审校脚本读写，勿手工改行号 |
| `extracted_language_review.json` | 记录（机器） | 提取文本的修改日志、阅读批次、收敛项 | 改动后同步指纹与结论 |
| `sentence_patterns.json` | 记录（机器） | 已确认句式基准，用于一致性回归 | 改动句式后同步目标串 |
| `recurring_terms.json` | 记录（机器） | 术语回归规则，供审计脚本读取 | 通过脚本校验 |
| `version_migration_8194.json` | 记录（机器） | 8194新增/退役节点、保留的历史审读项及官方引擎验证范围 | 本次迁移证据；当前进度查`progress.md` |
| `extracted_routes.json` | 记录（机器） | 提取文件与源模块的对应关系 | 拆并文件时更新 |

## 新增规则查阅入口

| 主题 | 当前规则与记录位置 |
| --- | --- |
| 新版对白归位、源行号、末尾old/new表 | [style_guide.md](style_guide.md#新增规则的适用与记录)中的源码顺序规则；迁移进度查progress |
| 对话按钮标点及同类复查 | [style_guide.md](style_guide.md#对话按钮选项的结尾标点强制)：普通结尾不带句号，内部逗号及语气标点保留 |
| 鸣谢页灰色用户名 | [terminology.md](terminology.md#鸣谢页用户名)、[english_residuals.md](english_residuals.md#鸣谢页署名例外) |
| 设置悬浮说明、同类文本格式、GitHub图标 | [style_guide.md](style_guide.md#设置说明与同类提示的一致性)；回归提示定译查terminology |
| 联系人姓名与Bridget姓氏 | [terminology.md](terminology.md#角色姓名强制)、[characters.md](characters.md#bridget)：Krüger保留ü |
| 本体更新日志正文与标题 | [style_guide.md](style_guide.md#本体更新日志翻译与版本维护)、[terminology.md](terminology.md#游戏更新日志) |
| 联系人六类身份标签与更新兼容 | [terminology.md](terminology.md#联系人分类标签)、[style_guide.md](style_guide.md#联系人动态身份标签与版本更新) |

以上规则适用于未来版本的同类文本；最新用户确认优先于历史批次说明。实际实现和验收范围查[progress.md](progress.md)，规则存在不代表对应界面已完成全部验收。

## 台账与变更记录分工

`manual_review.json` 回答“哪些条目被人工看过，当前还缺什么”，用行号和原文／译文指纹锁定版本，`note` 只写当前覆盖状态与未结项，历次改了什么查 `progress.md` 批次记录与 `extracted_language_review.json` 的 `changes`；台账不代表译文质量通过。`extracted_language_review.json` 回答“改了什么、为什么改”，保存修改前后对照、阅读批次和已收敛的问题。`sentence_patterns.json` 与 `recurring_terms.json` 是回归基线，供 `tools/` 下的审计脚本比对当前译文，用于发现文风漂移和术语不一致。

三份机器记录都由脚本生成或更新，手工编辑容易造成指纹失效。改动译文后应运行：

```
python tools/validate_translations.py --changed
python tools/audit_sentence_consistency.py --check-approved translation_context/sentence_patterns.json
python tools/audit_recurring_terms.py --changed --fail-on-mismatch
python tools/audit_manual_coverage.py
```

`audit_manual_coverage.py` 只检查记录完整性：报告过期文件、缺失文件和指纹不符，不证明译文可读或场景已验收。测试脚本 `tools/test_translation_audits.py` 覆盖审计工具的静态正反例。

## 状态口径

“已阅读”“已校对”“已改写”“质量通过”是四种不同结论。阅读批次只说明该范围被连续读过；校对说明已按上下文检查语义与语气；改写说明译文已更新并需要重新记录指纹；质量通过需要对应条目在当前版本上给出明确结论。露骨段落只做语义准确性与语句通顺度校对，不扩展原文没有的描写。

## 日期与主题的组织方式

除 `progress.md` 的“进度摘要”和“批次记录（按日期）”外，本目录文档不按日期分章。规范类文件（`style_guide.md`、`terminology.md`、`characters.md`、`recurring_terms.md`、`english_residuals.md`、`input_codes.md`）按主题组织；剧情与文件类文件（`storylines.md`、`file_inventory.md`）按线路或批次范围归组，把历次按日期堆积的记录并入对应主题。需要追溯某一批改了什么，查 `progress.md` 的批次记录和 `extracted_language_review.json` 的 `proofreading_batches`；需要查当前结论，查对应规范文件。

## 排版规范

- Markdown标题、正文段落、表格、列表和代码块之间统一隔一行；禁止连续空行。
- 同一列表的相邻条目不插空行，表头、分隔行及数据行连续排列；角色档案遵循相同规则。列表中的独立说明段按段落处理，不合并内容。
- 保留代码块内部排版、列表缩进、表格列和源文引用；不因排版改写剧情结论。
- 文件使用UTF-8无BOM、LF换行并以一个换行结束；JSON沿用两空格缩进，保持字段、数组次序及指纹含义。
- 遗留疑问的当前版本结论集中见[progress.md](progress.md#遗留疑问的8194复查)，历史批次保留原日期与证据边界，已收敛的术语状态回写对应主题。

## 新会话与增量翻译交接

本目录[AGENTS.md](AGENTS.md)规定新会话的必读顺序、版本确认、增量迁移、主题回写及交付检查，完整规范在此维护；仓库根目录仅保留引用入口。将本文件夹交付给其他Agent时，明确要求先读取本目录AGENTS.md及索引；规则随文件保存，不依赖旧聊天记录。单独交付文件夹提供规范和证据，实际翻译与工具验收还需要匹配版本的翻译源、官方源和仓库tools。

格式统一使用`python tools/check_translation_context.py --fix`，再运行不带`--fix`的检查。检查覆盖本目录Markdown/JSON；只调整排版，不改写规则、剧情或审读结论。无效JSON、重复字段及非标准数值会报错，且预检失败时不写任何文件。CI运行只读格式检查与工具测试，格式不符会失败；人工仍须检查内容是否进入正确主题及遗留疑问是否有证据。

新会话可使用以下交接文字，并填写实际版本和路径：

```text
请先读取所交付translation_context文件夹内的AGENTS.md与index.md，按必读顺序确认现有规则和遗留状态。
旧游戏版本：<旧版>；新游戏版本：<新版>；官方原包/源码路径：<路径>。
请进行增量翻译，保留源注释和行号，将对白归位、old/new置末，并复查同类UI及既有疑问。
按现有主题回写translation_context，运行格式检查与适用审计，分别报告文本和游戏内验证范围。
提交/推送/发包要求：<本次授权范围>。
```

## 清理规则

一次性任务的范围清单、待办队列和中间产物不长期存放在本目录：结论并入 `progress.md`、`extracted_language_review.json` 或对应规范文件后即删除，避免与本目录的长期记录重复。判断某文件是否可删，先确认没有工具或文档引用它。

## 变更记录

- 2026-09-13：登记目录全部文件；一次性清单文件（`proofreading_remaining_65.json`、`remaining_review.json`）结论并入 `extracted_language_review.json` 后删除；统一各文件头部用途说明；跨文件重复段落改为单一出处；`manual_review.json` 的无条目文件由 `pending` 收敛为 `non_translation_support_file`；同一行多次修订补记 `revision`／`is_latest`。
