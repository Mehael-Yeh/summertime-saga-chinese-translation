# 翻译精修进度

## 2026-09-12 剩余语义问题修复（当前源码）

- 修正2个翻译文件共27处：8处剧情阶段提示、14处住宅客厅提示、3处直播表达及2处日记歧义。原文、变量、格式标签与脚本结构不变。
- 术语和语境边界归入terminology.md、english_residuals.md、recurring_terms.md；句式基准扩展到141条。
- 全仓323个翻译文件校验、141条句式回归、登记术语及中英文间距检查通过。未进行场景游玩验证；静态检查不代表所有对白均已逐句精修。
- 本轮不改README，不构建RPA。以下归档信息是先前构建记录，不包含本轮27处源码修订。

## 2026-09-12 清理7944的Lint提示（当前结果）

- 按用户要求撤回README的全部本轮修改，README相对HEAD无差异；不进行场景游玩验证。
- 依据7944引擎的`default_translates`与`language_translates`实际清单，移除22个文件中的171个orphan翻译块，不再保留这些旧版遗留块。未删除任何当前默认翻译标识；仅移除1条不再有对应原文的句式基准，现有114条。
- 默认中文启动脚本的初始化优先级从1000调整为999，仍在普通初始化之后执行，消除超出有效范围的提示。
- 在全新隔离目录进行compile与Lint：无异常回溯，Orphan Translations及初始化优先级提示均已消除。Lint仅保留引擎通用的`config.check_conflicting_properties`检查建议和测试说明；不通过禁用Lint掩盖问题。
- 全仓323个翻译文件校验、114条句式回归、术语及间距检查通过。当前引擎报告34,840个中文对白块。
- 已重新编译并构建`dist/zh_hans.rpa`：651个文件、46,058,563字节，逐文件校验通过；SHA-256：`7c33f43386d96478df0c3a489d4b0b772500698fa396dc92cd6526f4706f99ac`。以下旧构建结果为历史记录，不代表当前产物。

## 2026-09-12 7944完整检查与编译包验证

- 本轮起点为用户已提交的`b465e25`；以用户指定的`21.0.0-wip.7944`游戏本体为最终依据，在独立目录验证，不安装到用户游戏或改动其存档。
- 从原始`src.rpa`反编译363个文件，全部成功；剧情原文注释摘要匹配34,862条，差异0条，另127条不能由本工具直接核实。恢复64处错误注释，修复51处译文／显示控制内容，涉及旧版遗留块及对应错误；新增1条日记漏译。
- 日记按字节码常量中的36页、296条非空字符串核对映射和格式标记。294条有译文，剩余2条仅含姓名变量或表情符号；保护标记差异0。确认实际界面按页内行序显示，不按翻译文件顺序拼接。尚未逐页做视觉排版验收。
- 全仓323个翻译文件校验通过；115条句式基准、全部登记术语和混排空格检查均为0 mismatch。另核对15个修改文件，变动仅限译文、64处已验证原文注释与1组新增字符串，程序结构保持一致。
- Ren’Py 8.5.3在完整7944隔离副本中compile通过，无异常回溯；运行`translate zh_hans`未生成新增文件、未发现空译文。实际引擎加载的中文翻译含35,011个对白块。
- Lint已运行：保留旧版orphan翻译、原有`init 1000`优先级警告及检查冲突属性的建议。不是“零提示”，也不代替逐场景游玩。
- 按“先编译、再打包”生成`dist/zh_hans.rpa`：651个文件、46,099,218字节，含323个编译脚本。归档与编译目录逐字节验证通过；仅安装RPA的第二个隔离副本确实加载zh_hans，Lint正常完成。SHA-256：`955f29bcfede1ee8431893c06f967037cfe0bb66ad6d246f278aadcc36c2294e`。
- 新增`--require-compiled`防止把缺少编译脚本的源码包误当作可安装包；已验证其能拒绝缺少323个编译脚本的目录。本轮未提交、推送或发布。

## 2026-09-12 发包后全仓静态检查与部分语义修订

保留既有手工修改，对323个RPY文件、38,110对文本进行静态扫描。本轮修订25个文件、123处文本，涵盖人物资料、称谓、指代与中文表达。结构、登记术语和混排空格检查通过；全仓逐句审校及游戏内验证尚未完成。规则、人物信息和待查项已分别归入风格指南、角色档案、术语表与重复表达记录。

## 2026-09-12 Debbie 的 mister 语境修正

复查 Debbie 的8处 mister：7处指 Anon，其中5处“先生”按语境改为“你这小子”“小坏蛋”或直接表达警告、拒绝；已合适的电视提醒与庭院“小坏蛋”保留。电话中对威胁者的1处不改。同步更新术语、角色档案和审计规则。

## 2026-09-12 非地名英文残留

修复10条目标字符串：2条气泡编辑器操作、1句完整日记、1处lite、1处mesmerizing、1处LARPer、3处物品名及1条网页评论。非英语与混合语言句本轮不改；保留理由和开发占位问题见 `english_residuals.md`。新增4条术语审计规则，按用户说明恢复12个月份全称为英文，撤掉June校验例外；防止共享字符串翻译影响角色姓名。

## 2026-09-12 地名与中英文间距专项

再次排查：Consum-R→购乐百货（19处）、Hillside Mall→山畔商场、Rusty Angus→锈牛酒吧、Glazies→糖霜甜甜圈店；另修正灯室、房车营地、育幼院、小客厅、竞技场的 UI 译名，合计27处。同步更正 Consum-R 保留英文的旧规则，并增加5条场所名称审计规则。

后续按用户确认，将 Ara Ara 的 UI、菜单、任务和对话共10处统一为“啊啦啊啦”，同时将欢迎词调整为“欢迎光临……”，保留店名兼招呼语的日式韵味。

对照两份 sets.rpy，核对 18 个地点专名；统一 Cosmic Cumics→宇宙漫画、Cupid→丘比特、Saga Financial→传说金融、Ara Ara→啊啦啊啦、Sugar Tats→甜蜜纹身、CineSaga→传说影院。按用户意见与场所设定同步修订 UI：Pink→粉色诱惑、Retro Strike→复古全中。Raven Hill 的 11 处完整名称已为渡鸦山，无旧译残留。

全仓清理 32 个文件中 111 条译文的中英文间空格，保留英文词组内部空格及程序标记。同步更新 terminology.md、style_guide.md、recurring_terms.md 与 recurring_terms.json，增加 16 条地名规则及只读间距审计工具 tools/audit_mixed_spacing.py，并清除旧文档（含 storylines.md）中要求店名保留英文的冲突规则。本次完成源码修复与静态验证，未构建 RPA、未进行游戏内验收。


更新时间：2026-08-06

## 状态说明

- **完成**：已通读完整文件，完成英文对照、纯中文复读、原文复核及格式校验。
- **规则修复**：仅修复可高置信确认的姓名、标签或变量问题，尚未对完整剧情逐条精修。
- **待处理**：尚未完成完整场景级精修。

## 已完成文件

| 文件 | 剧情线/场景 | 主要角色 | 状态 | 主要修复 | 校验 |
|---|---|---|---|---|---|
| `tl/zh_hans/src/plot/mar01.rpy` | Maria线；Tony/Maria 生育后的披萨店成人场景与关系安抚 | Maria、Tony、Anon | 完成 | 通读完整场景并精修感谢、生育双关、顾客掩饰、性交与高潮、负罪感安抚；统一中文省略号、成人动作强度和 Maria 主动粗俗口吻；保留所有英文姓名与变量 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar02.rpy` | Maria线；Tony与Anon讨论 Maria 产后继续发生关系及再生育计划 | Tony、Anon、Maria（被提及） | 完成 | 通读完整场景并精修 Tony 的支持与施压、Anon 的犹豫和关系推进；统一 Tony 专属称呼 `champ` →“冠军”；保留性行为动作强度、粗俗语气和英文姓名 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_baby.rpy` | Maria线；怀孕确认、单胎/双胎生产、医院探访、产后恢复与返回披萨店 | Maria、Tony、Anon、新生儿 | 完成 | 通读单胎与双胎全部分支；精修怀孕生产、教父关系、产后关怀和成人双关；修复“听醒”“娃娃脸”等误译；统一 `champ`、`cannoli`、单复数代词及英文姓名 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_cook.rpy` | Maria线；Maria在厨房为Anon准备食物并推进亲密关系 | Maria、Anon | 完成 | 通读完整场景并精修 40 个翻译块；统一 cannoli 等意大利食物术语；修复厨房动作、暧昧双关、成人语气和 Maria 对 Anon 的称呼；保留英文姓名、变量与 Ren’Py 结构 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/maria.rpy` | Maria 线；公寓与披萨店的通用入口、出口、菜单及储藏室短互动 | Maria、Anon、Tony（被提及） | 完成 | 精修 58 个对话块和 4 个菜单文本；按关系阶段区分“小子”与“帅哥”，将后期 `lookin’ for trouble` 处理为性邀约式“找刺激”；修复菜单主题、工钱占位符外围中文及储藏室连续互动 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/maria_lounge.rpy` | Maria 线；公寓客厅夜间访问、无人应门及 Tony 休息日拦截 | Maria、Tony、Anon | 完成 | 精修 13 个翻译块；纠正整文件多处译文错位和截断，恢复夜间内心独白、敲门声、Maria 邀请进门、无人应门及让 Tony 休息的完整逻辑；按实际生效方式保留 TODO 块中的中文拦截文本 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_dark.rpy` | Maria线；夜间造人、内射/拔出分支、骑乘、“恶魔三人行”及双重插入 | Maria、Tony、Anon | 完成 | 通读 369 组英文—中文对应；精修 Tony 的造人指导和粗俗起哄、Maria 后期主动口吻、Anon 的迟疑与参与；统一 `champ`、`capisce/capiche`、`Devil's Threeway`、`The Kidney Shifter`、`cannoli` 及成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_couch.rpy` | Maria线；Tony熟睡、半醒或看球时，Maria与Anon在沙发上发生性行为，并以棒球双关贯穿多条场景 | Maria、Tony、Anon、Carmella | 完成 | 通读 640 个翻译块；精修射精、内射、上垒、满垒、界外球和“横着做披萨”等双关；统一 Tony 的 `champ`→“冠军”、The Falsettos→《假声》以及 Carmella 英文姓名；恢复露骨性行为和 Maria 主动语气，全文消除活动译文中的 ASCII 省略号和直角引号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_door.rpy` | Maria线；久未造访后的卧室性交、央求、拔出/内射与续战分支 | Maria、Anon、Tony（被提及） | 完成 | 精修后期关系中的主动邀约、央求与 Anon 掌控节奏；明确区分内射期待和拔出后的保密要求；统一连续拆句、女性高潮和动作义“肏” | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_kitchen.rpy` | Maria线；披萨店后厨的试探、速战速决与食物式成人双关 | Maria、Anon | 完成 | 精修 38 个翻译块；保留 Maria 经营者的警觉和后期直接欲望；统一 `au jus`→“肉汁”、`Yes, ma’am.`→“是，老板娘”及未完成连续句 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/mar_pantry.rpy` | Maria线；储藏室工作压力、性邀约、内射/拔出与事后交接 | Maria、Anon、Tony（被提及） | 完成 | 精修 90 个翻译块；恢复“休息”双关、再次怀孕诉求和拔出分支差异；统一女性高潮、`Cum in me`、`Gimme another baby` 及连续拆句 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb01.rpy` | Debbie线开端；陌生索款威胁、父亲债务疑云及 Diane 园艺工作分支 | Debbie、Anon、Diane（被提及） | 完成 | 通读 77 个翻译块；理顺电话冲突、Debbie 强装镇定、Anon 主动分担和菜园分支；统一 `sweetie`→“亲爱的”、中文省略号、内心独白括号与父亲称谓 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb02.rpy` | Debbie线早期；父亲遗留报纸、填字游戏双关、意外亲吻与 Anon 首次性反应 | Debbie、Anon | 完成 | 通读 71 个翻译块和 4 个选项；恢复 `Dick` 的英文填字与性双关，修复捡笔动作、碰头安慰、勃起反应及错位内心独白；统一 `sweetie`、省略号、中文括号与英文填字答案 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb03.rpy` | Debbie线早期；承担家务、修剪草坪、地下室毛巾事故与首次明确身体吸引 | Debbie、Anon、Jenny | 完成 | 通读 219 个翻译块和 3 个选项；修复父亲责任承接、`my boy` 误译、洗衣动作、裸体/勃起场景、Debbie 的掩饰、蜘蛛借口及三分支连续性；统一全角括号和中文省略号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb04.rpy` | Debbie线早期；浴室水管爆裂、家庭维修责任与 Jenny 湿衣试探 | Debbie、Jenny、Anon | 完成 | 通读 188 个翻译块并精修 154 处；理顺关总水阀、获取扳手、湿衣脱衣试探和四类维修见证分支；强化 Debbie 的经济压力与照顾者鼓励、Jenny 的尖刻挑衅及 Anon 承接父亲责任的成长 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb05.rpy` | Debbie线早期；家务分担、卧室送衣、腿部按摩与暧昧边界 | Debbie、Anon | 完成 | 通读完整场景并精修约 171 处；理顺家务承接、背痛与压力、乳液气味和私人物品分心、按摩中的身体吸引及 Debbie 及时叫停；统一 `sweetie`、中文省略号、全角括号，并保留早期关系阶段的含蓄强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb06.rpy` | Debbie线早期；按摩回忆、偷拿润肤露、使用内裤自慰被撞见及事后边界谈话 | Debbie、Anon | 完成 | 通读 126 个翻译块；理顺按摩记忆、气味诱发的性冲动、Debbie 撞见后的震惊与自我安慰，以及她理解自慰但明确禁止在卧室或使用内裤的边界；统一 `sweetie`、润肤露、自慰、内裤、中文省略号、中文双引号和全角括号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb07.rpy` | Debbie线早期暧昧推进；夜间共看爱情片、意外触碰勃起及双方首次持续性幻想 | Debbie、Anon | 完成 | 通读 141 个翻译块；理顺选片争论、电影情色转折、脚部误触、Debbie 对尺寸的震惊与幻想、Anon 的尴尬掩饰及温柔告别；以“挺得住”保留 `solid` 的承受/勃起双关，并回扣“巴西 Bum Bum”产品名 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb08.rpy` | Debbie线；商场同行、Cupid试衣、首次接吻与事后回避 | Debbie、Anon、Kassy、Jenny（被提及） | 完成 | 通读 375 个翻译块和 6 个选项；精修购物邀请、童年照片笑点、女装店调侃、更衣室拉链、电影回调、首次接吻及双方不同的事后心理；修复反译、连续拆句、拉链方向和关系阶段，统一省略号、中文双引号与内心括号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb09.rpy` | Debbie线；首次接吻后的性梦、Ursula乱入噩梦及关系认知变化 | Debbie、Anon、Ursula | 完成 | 通读 33 个翻译块；理顺 Debbie 安抚与性诱惑的连续拆句、Ursula 的学校羞耻威胁及 Anon 醒后的自我审视；修复称谓误译、机翻语序、ASCII 省略号和半角内心括号，保留梦境露骨强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb10.rpy` | Debbie线；Debbie自慰幻想、Anon与Jenny偷窥及Jenny借机要挟 | Debbie、Anon、Jenny | 完成 | 通读 88 个翻译块；精修门外误判、自慰幻想、Anon确认幻想对象、Jenny撞破偷窥及后续要挟；修复连续拆句、自慰俚语、女性高潮、双关笑话、中文引号、省略号和内心括号，区分幻想中的欲望与现实中的同意 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb11.rpy` | Debbie线；早餐性梦、小丑噩梦、梦遗惊醒及Jenny隔门挖苦 | Anon、Debbie、Jenny | 完成 | 通读 88 个翻译块；理顺Jenny炫耀新裙、Debbie桌下口交、人物变成小丑、阴茎变羊驼及咬伤惊醒的梦境递进；修复连续拆句、口交拟声、食物性双关、梦遗笑点、中文省略号和内心括号，保留梦境欲望与现实关系的区别 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb12.rpy` | Debbie线；借性焦虑请求指导、再次接吻、Jenny撞见及重新划定边界 | Debbie、Anon、Jenny | 完成 | 通读 128 个对话块和 3 个选项；理顺梦境话题转为性焦虑的试探、商场接吻回扣、“纯教学”自我辩护、大学接吻技巧、扁桃体炎掩饰及Jenny的尖刻揭穿；修复代词、连续拆句、中文省略号、双引号与内心括号，区分真实吸引、主动试探和现实边界 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb13.rpy` | Debbie线；汽车发动机损坏、Josie 保修/付款分支、Jiang 上门修车及车内关系推进 | Debbie、Anon、Josie、Jiang | 完成 | 通读 486 个对话块和 4 个选项；理顺车辆损坏、八千美元维修费、延长保修与自费分支，精修 Josie 的电话性暗示和 `bowl cut` 固定挖苦、Jiang 的修车/性双关，以及 Debbie 与 Anon 从责任感安慰推进到独处接吻、触碰勃起但仍拒绝进一步性接触的边界变化；统一中文省略号、双引号、内心括号和车辆术语 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb14.rpy` | Debbie线；再次偷拿内裤自慰、Debbie撞见、观看自慰、射精及浴室私下自慰 | Debbie、Anon、Mia（被提及） | 完成 | 通读 193 个对话块和 5 个选项；区分接受、退让及同龄女生建议分支，保留 Debbie 的真实吸引与照顾者边界、Anon 的欲望和越界责任；统一中文省略号、内心括号、菜单标点及 Anon 对 Debbie 的 `ma’am`“夫人”称呼 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb15.rpy` | Debbie线；浴室偷窥、擅自闯入与隐私边界重申 | Debbie、Anon、Jenny（被提及） | 完成 | 通读 40 个对话块和 2 个选项；理顺 Anon 将此前亲密许可误判为更广泛同意、闯入浴室后被 Debbie 制止及双方事后自责的逻辑；保留 Debbie 对 Anon 的吸引与明确隐私边界，统一中文省略号、内心括号和连续拆句 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb16.rpy` | Debbie线；Jenny遗留色情片、房东房客剧情映照、共同自慰与事后关系确认 | Debbie、Anon、Jenny、色情片角色 | 完成 | 通读 281 个翻译块；理顺 Anon 被色情片挑起欲望、Debbie 撞见后允许继续、双方互相观看自慰与描述幻想、Debbie 高潮、Anon 射精及事后罪恶感安抚；统一 `landlady`“房东太太”、中文省略号、内心括号和 Anon 对 Debbie 的 `ma’am`“夫人”，保留“只此一次”的真实边界 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb17.rpy` | Debbie线；共同自慰后的夜间反思、潜入卧室触摸 Anon 及主动停止越界 | Debbie、Anon | 完成 | 通读 66 个翻译块；理顺 Debbie 从罪恶感、自我否认转向偷看、隔着内裤触摸、直接抚弄阴茎及性交幻想，保留她以“帮忙”为借口的自我合理化和最终主动离开的真实边界；统一中文省略号、内心括号、成人动作强度及睡梦语气 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb18.rpy` | Debbie线；俄罗斯打手入侵、Anon保护 Debbie、浴室照顾与首次主动手淫 | Debbie、Anon、Jenny、Dimitri、Igor、Yumi、Harold、Raz（被提及） | 完成 | 通读 178 个翻译块；理顺打手入侵、Anon受伤、报警掩护、Debbie自责及以照顾和奖励为由主动手淫的关系推进；保留 Dimitri 的性威胁、Igor 的迟钝笑点、Debbie 照顾者式色情口吻及“只能到手淫”为止的新边界；统一中文省略号、内心括号和姓名变量 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb19.rpy` | Debbie线；失眠夜谈、丧亲孤独、主动同床与首次性交 | Debbie、Anon、Jenny（被提及）、Diane（被提及） | 完成 | 通读 304 个翻译块；理顺助眠药、亡夫留下的空床、Anon 不愿趁脆弱推进关系及 Debbie 主动邀请同床的情感基础；完整精修亲吻、身体爱抚、口交、摩擦、首次插入性交、互相表白、拔出/内射及多阶段停止分支，保留每个分支的真实同意边界和次日谨慎重复约定；统一中文省略号、内心括号、女性高潮表达及 `ma’am`“夫人” | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb20.rpy` | Debbie线；厨房偷听、向 Diane 复盘关系升级及道德顾虑疏导 | Debbie、Diane、Anon | 完成 | 通读 154 个翻译块；理顺从献殷勤、自慰被撞见、摆姿势帮助射精、共同洗澡到手淫的完整复盘；区分 Debbie 的羞耻、受用与年龄/照顾者负罪感，强化 Diane 开放直白的闺蜜调侃，并保留 Anon 偷听后选择给 Debbie 时间消化的边界 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb21.rpy` | Debbie线；Jenny母女冲突、陪看烘焙节目、沙发亲密升级及乳交被撞见 | Debbie、Anon、Jenny | 完成 | 通读 305 个翻译块；理顺 Debbie 因 Jenny 冷落而受伤、Anon 安慰和表白、舔舐与高潮后主动止步、继续依偎、乳交及 Jenny 撞见后的冲突；修复损坏文本、英文姓名音译、连续拆句和成人动作表达，并保持 Debbie 的照顾者语气、真实欲望与越界负罪感并存 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb22.rpy` | Debbie线；深夜进入Anon房间、欲望自辩、主动口交及梦魇分支 | Debbie、Anon、Diane（被提及）、Jenny（被提及）、Ursula（梦境） | 完成 | 通读 121 个对话块和 2 个菜单选项；理顺 Debbie 从房东/照顾者负罪感到接受自身欲望、主动触摸与口交、Anon 醒来后的惊慌逃离，以及追赶/回床分支和 Ursula 梦魇；统一内心括号、省略号、连续拆句与重复台词，并保留 Debbie 成熟照顾口吻和真实成人欲望 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb23.rpy` | Debbie线；深夜口交后的回避、渡鸦山私谈和解及Cupid泳衣试穿 | Debbie、Anon、Kassy | 完成 | 通读完整场景；理顺 Debbie 因趁 Anon 熟睡口交而自责回避、双方在渡鸦山区分熟睡时无法回应与醒来后的真实愿望、和解后再次主动口交，以及Cupid蓝色／紫色／白色泳衣试穿和试衣间“搭扣卡住了”的掩饰；保留 Debbie 的身体不自信、房东身份顾虑与真实欲望 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb24.rpy` | Debbie线；泳池裸泳、Diane推动Debbie正视欲望、浴袍搜索及拒绝同床 | Debbie、Diane、Anon、Jenny（浴室分支） | 完成 | 通读 342 个翻译块；修复 Anon 未来家庭归属的指代错译，理顺跨块连续句；精修手淫、口交、乳交、隔衣磨蹭、舔阴／舔肛及泳池挑逗；统一女性复数、中文括号、省略号和浴袍搜索分支口吻 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb25.rpy` | Debbie线；泳池挑逗后的欲望失控、夜间游荡、首次主动性交及次日退缩 | Debbie、Anon、Jenny（被提及）、Diane（被提及）、色情片角色 | 完成 | 通读 428 个翻译块；精修 Debbie 在家中转移注意力却不断联想到 Anon 的连续场景、主动口交与首次明确要求插入、性交和高潮、内射／拔出分支、事后爱意及次日因年龄差和房东责任退缩；修复眼镜蛇和 `gotten into` 双关、连续拆句、女性高潮、复述引号及成人表达强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/deb26.rpy` | Debbie线；Diane出谋划策、Cupid礼服、Ara Ara正式约会与关系公开 | Debbie、Anon、Diane、Jenny、Hana、Titomi | 完成 | 通读853个翻译块；理顺Diane劝Anon坚定沟通、送礼服、正式约会、未来承诺、女体盛与普通点餐分支、回家性交及次日公开亲密；统一`Charge`结账语义、`succulent`误读笑点、Diane的`stud`称呼、Anon对Debbie的`ma’am`“夫人”；地名现按专项规则统一为丘比特、啊啦啊啦；英文姓名保留 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb27.rpy` | Debbie线；傍晚泳池调情、裸体跳水、被发现风险与泳池性交 | Debbie、Anon、Jenny（被提及）、邻居（被提及） | 完成 | 通读133个翻译块；精修泳池邀约、忍者神龟笑点、裸体跳水、性交、被邻居或Jenny发现的刺激、高潮失控及事后含糊告别；理顺三组连续拆句，统一`Cowabunga`复述、`sweetie`“亲爱的”、中文括号、省略号和双引号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过（327个文件） |
| `tl/zh_hans/src/plot/deb_baby.rpy` | Debbie生育支线；怀孕确认、Jenny知情、孕期日常、生产、医院恢复、母婴回家与产后照顾 | Debbie、Anon、Jenny、Diane、Micoe、新生儿 | 完成 | 通读758个翻译块及16个菜单项；精修怀孕阶段关系变化、Frank冷冻精子圆谎、单胎/双胎分支、父亲身份掩饰、医院和产后代词、房客身份错位笑点、托儿所及乳头刺激双关；清除“娃娃脸”等误译 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过（327个文件） |
| `tl/zh_hans/src/plot/deb_island.rpy` | Debbie支线；厨房中岛台调情、Jenny撞见风险、舔阴与台面性交、体外射精/内射分支 | Debbie、Anon、Jenny、Jane（被提及） | 完成 | 通读153个翻译块及2个菜单项；精修关系后期的主动调情、房东身份玩笑、舔阴和台面性交；理顺Jenny在家/外出、连续拆句、女性高潮及体外射精/内射差异；统一`landlady`“房东太太”、中文省略号和成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过（327个文件） |
| `tl/zh_hans/src/plot/deb_kitchen.rpy` | Debbie支线；早餐厨房调情、Jenny在旁/洗澡/不在分支、从背后性交及内射/体外射精 | Debbie、Anon、Jenny | 完成 | 通读205个翻译块及1个菜单项；精修“香肠肉饼”“拍松肉”“更能填饱我”等连续食物/性双关，理顺Jenny发现风险、女性高潮与潮喷、射精主语、腿软连续句、房东身份调情和事后清理；统一中文省略号、括号与成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过（327个文件） |
| `tl/zh_hans/src/plot/deb_laundry.rpy` | Debbie支线；洗衣房调情、洗衣量/射精量双关、烘干机乳交、骑乘性交及内射/体外射精 | Debbie、Anon、Jenny（被提及） | 完成 | 通读332个翻译块及2个菜单项；精修`load`与`spin cycle`双关、连续拆句、`boobs`/`breasts`/`tits`用词层级、房东身份调情、女性高潮与射精主语，并理顺事后家务及晚餐过渡 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过（327个文件） |
| `tl/zh_hans/src/plot/deb_lobby.rpy` | Debbie支线；客厅中的亲密互动、Jenny回家风险及成人关系推进 | Debbie、Anon、Jenny（被提及） | 完成 | 通读完整场景；精修房东太太身份调情、亲吻、性交及内射/体外射精分支；统一 `landlady`→“房东太太”、`sweetie`→“亲爱的”、中文省略号和成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_mall.rpy` | Debbie支线；商场购物、车内亲密互动与怀孕后日常 | Debbie、Anon、Jenny（被提及） | 完成 | 通读完整场景；精修购物闲聊、车内接吻、Raven Hill 骑乘与口交分支、一起高潮、体外/内射和怀孕后日常；统一 `sweetie`、中文省略号、弯引号、人物语气及成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_pants.rpy` | Debbie支线；Debbie发现Anon自慰、留下观看并主动调情，随后进入射精与事后清理分支 | Debbie、Anon | 完成 | 通读完整场景；精修偷窥/自慰发现、Debbie主动观看与鼓励、射精到身上、事后安抚及“憋得太久”的支线双关；统一`sweetie`“亲爱的”、中文省略号、喘息表达、英文姓名和成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_pool.rpy` | Debbie支线；泳池边泳装调情、户外性交及邻居撞见风险 | Debbie、Anon、Tammy、Erik、Harold、Helen（被提及） | 完成 | 通读完整场景；精修泳装赞美、泳池边主动调情、邻居与熟人可能撞见的紧张感、性交节奏及 Debbie 的高潮前连续拆句；统一 `sweetie`“亲爱的”、中文省略号、全角括号、英文姓名和成人动作强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_shower.rpy` | Debbie支线；浴室偷窥、淋浴性交、口交与边界重申 | Debbie、Anon、Jenny（被提及） | 完成 | 通读完整场景；精修浴室雾气、偷窥与关系阶段变化；理顺肛门相关双关、口交射精、互相清洗、抚摸/手淫和停止分支；统一 `ma’am`→“夫人”、`landlady`→“房东太太”、`my boy`→“我的好男孩”、中文省略号及女性高潮表达 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_sink.rpy` | Debbie支线；浴室洗澡/自慰、舔阴、洗手台性交与房东房客双关 | Debbie、Anon、Jenny（被提及） | 完成 | 通读完整场景；精修浴室调情、舔阴、女性高潮、洗手台性交、内射/暂缓分支及事后房东房客双关；统一 `ma’am`→“夫人”、`sweetie`→“亲爱的”、`landlady`→“房东太太”、中文省略号和成人表达强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_sleep.rpy` | Debbie支线；Debbie与Anon同床过夜、早晨亲吻及避开Jenny的离开互动 | Debbie、Anon、Jenny（被提及） | 完成 | 通读完整场景；精修同床邀约、拥抱安抚、早晨调情、`good boy`与`ma’am`称呼、避开Jenny的紧张感；修复中文省略号、变量与菜单选项表达 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_utility.rpy` | Debbie线；地下室/公用设施区域短交互；Anon与Debbie的日常碰面及暧昧关系延续 | Debbie、Anon | 完成 | 通读完整短场景；修复地下室方向、日常询问、突然撞见和安慰语气；统一 `sweetie`→“亲爱的”、中文省略号与自然口语，保留英文姓名、变量和 Ren’Py 结构 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA构建通过 |
| `tl/zh_hans/src/plot/deb_visit.rpy` | Debbie线；夜间唤醒、多轮性交、怀孕后性欲与拒绝继续分支 | Debbie、Anon | 完成 | 通读完整场景；理顺 Debbie 的羞愧、内疚、主动欲望和怀孕后激素影响；修复连续拆句、女性高潮表达、内射与拔出分支及 `sweetie`、`ma’am`、`landlady` 称谓；活动译文统一使用中文省略号和中文双引号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/+prologue.rpy` | 序章；父亲葬礼、死亡疑点、债务与开学背景 | Anon、Debbie（叙述中） | 完成 | 重写机翻腔；理顺死亡调查、收留和债务背景；统一叙述语气 | `validate_translations.py --changed` 通过 |
| `tl/zh_hans/src/plot/+tutor.rpy` | 系统教程；HUD、地图、物品栏、手机、时间推进 | tutor、Anon（变量） | 完成 | 统一系统术语；修复 `extend` 连续拆句；改善教程说明的自然度 | `validate_translations.py --changed` 通过 |
| `tl/zh_hans/src/plot/ano01.rpy` | 主线；复学第一天及学校角色集中引入 | Anon、Jenny、Debbie、Erik、Tammy、Mia、Roxxy、Ursula、Kevin、Annie、Judith、Bridget、Rhonda、Viv、Eve | 完成 | 精修 609 个翻译块和 3 组菜单文本；修复答非所问、连续拆句、角色口吻、色情游戏双关、ASCII 省略号和菜单术语不一致 | `validate_translations.py --changed`、`git diff --check`、RPA 构建/校验通过 |
| `tl/zh_hans/src/plot/ano02.rpy` | 主线；警方通报父亲死亡调查、资金失踪与威胁电话 | Anon、Debbie、Harold、Yumi、Frank、Liu Wang | 完成 | 精修 121 个翻译块；修复调查逻辑、连续拆句、职业礼貌、代词指向、`overhear` 误译为“偷听”、金融术语及 `[saga.cast.liu] Wang` 姓名顺序 | `validate_translations.py --changed`、`git diff --check`、RPA 构建/校验通过 |
| `tl/zh_hans/src/plot/ano03.rpy` | 主线；家庭早餐、Dimitri 上门威胁、Yumi 做笔录与安全安排 | Anon、Debbie、Jenny、Dimitri、Yumi、Frank、Harold | 完成 | 通读 253 个翻译块并精修 189 个；修复苹果汁漏译、连续拆句、Dimitri 非母语威胁口吻、Yumi 警务称谓、APB/笔录术语及 Jenny 前期敌对语气 | `validate_translations.py --changed`、`git diff --check`、RPA 构建/校验通过 |
| `tl/zh_hans/src/plot/ano04.rpy` | 主线早期；Tammy 上门慰问、与 Debbie 谈离婚及照顾 Erik、鼓励 Debbie 与 Anon 沟通 | Tammy、Debbie、Anon、Erik（被提及） | 完成 | 通读 43 个翻译块并精修 39 个；修复丧亲慰问翻译腔、`friendly ear`/`come out of his shell` 直译、连续拆句、Tammy 母性化口吻及 Debbie 早期照顾者边界 | `validate_translations.py --changed`、`git diff --check`、RPA 构建/校验通过 |
| `tl/zh_hans/src/plot/ano05.rpy` | 主线；Dimitri 驾车监视、报警与警方留守、Anon 的家庭保护欲及开放探索引导 | Anon、Debbie、Jenny、Yumi、Dimitri（车内） | 完成 | 通读 115 个翻译块并精修 91 个；修复车辆动作误译、警方反讽、连续拆句、Jenny 露骨拒绝比喻、`That's my boy!` 关系误译及 ASCII 省略号 | `validate_translations.py --changed`、`git diff --check` 通过；RPA 已成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano06.rpy` | 主线；Dimitri 与 Igor 街头围堵、Tony 解围、Debbie 抵押房屋支付追债款 | Anon、Dimitri、Igor、Tony、Debbie、Jenny | 完成 | 通读 329 个翻译块并精修 231 处译文；修复块内错配、非母语威胁口吻、成人搜身笑话、Tony 粗俗保护者语气、二十五万美元贷款和房屋抵押逻辑 | `validate_translations.py --changed`、`git diff --check` 通过；RPA 已成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano07.rpy` | 主线；Tony披萨店送餐试送、正式入职及初见 Maria | Anon、Tony、Maria、Gino（被提及） | 完成 | 通读 249 个翻译块并精修 198 处译文；修复送货员短缺错译、自取订单和试送术语、分支衔接、Tony 江湖化雇主口吻、Maria 从警惕到工作指导的态度变化及粗俗比喻强度 | `validate_translations.py --changed`、`git diff --check`、结构映射专项检查通过；RPA 已成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano08.rpy` | 主线占位；Tony 关系线的元叙事自嘲 | Anon、Tony（被提及） | 完成 | 通读 4 个翻译块并精修 3 处译文；修复 `face time` 误译、元叙事逻辑、全角内心独白括号和纯省略号 | `validate_translations.py --changed`、`git diff --check`、结构映射专项检查通过；RPA 已成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano09.rpy` | Tony披萨店；Tina 初见、Luigi 遗属照顾承诺、送餐车辆购买/置换与命名 | Anon、Tony、Maria、Tina、Luigi（被提及） | 完成 | 通读并精修 385 个翻译块；统一 Tony/Maria 的意大利裔美国人口吻、雇佣称谓和车辆分支；固定 `champ`→“冠军”、`babyface`→“小帅哥”、`dollface`→“美人儿”及车辆专名；保留 Luigi 遗属承诺的真实关系 | `validate_translations.py --changed`、重复术语审计、`git diff --check`、结构/BOM/CRLF 专项检查通过；RPA 已成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano10.rpy` | Tony披萨店；披萨教学、cannoli 奖励误导、黑帮往事与不育诊断 | Anon、Tony、Maria、Luigi（被提及） | 完成 | 通读 324 个英文—中文映射并精修 248 余处；统一手抛饼底、深盘披萨、披萨石和意式奶油甜馅卷；修复 `mustache ride` 成人双关、`protégé` 关系定位、连续拆句、Tony/Luigi 兄弟关系、意大利黑手党身份及 Tony 不育比喻到直白说明的情绪递进 | `validate_translations.py --changed` 验证 18 个修改文件；10 组重复术语审计零不一致；`git diff --check` 通过；RPA 成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano11.rpy` | Tony披萨店；领养/精子捐赠争论、搬面粉、Dimitri/Igor 闯店及 Tony 调查 Raz | Anon、Tony、Maria、Tina、Dimitri、Igor、Eddie Four-Fingers（被提及） | 完成 | 通读 324 条对话映射和 2 条 strings，精修 259 条译文；修复生育状态误判、领养与捐精逻辑、俄式食品笑话、持枪冲突节奏、连续拆句及人物旧绰号；固定 `little bunny`、`The Plumber`、`Eddie Four-Fingers` | `validate_translations.py --changed`、重复术语审计、`git diff --check` 通过；BOM/LF/末尾换行保持 |
| `tl/zh_hans/src/plot/ano12.rpy` | Tony/Maria 关系线元叙事占位 | Anon、Tony、Maria（被提及） | 完成 | 通读 4 个对话块和 1 条 strings，精修 5 处；与 `ano08.rpy` 的平行元叙事统一，并将随机奖励显示统一为“好感度中幅提升” | `validate_translations.py --changed`、`git diff --check` 通过；BOM/CRLF/末尾换行保持 |
| `tl/zh_hans/src/plot/ano13.rpy` | Tony/Maria 领养面谈；特殊披萨送餐；Tina 成人关系推进；Becca 撞见；Eddie 调查与领养失败 | Anon、Tony、Maria、Tina、Becca、Missy、Eddie Four-Fingers（被提及） | 完成 | 通读约 540 个翻译块并精修 268 处；修复特殊披萨配料、海滨公寓、成人场景强度、母女冲突、连续拆句、Eddie 英文姓名、十年刑期与探监调查逻辑；固定“冠军/小帅哥/美人儿”；按审查意见补强“额外香肠”的阴茎双关、区分动作义“肏”与感叹义“操”，并改用中文弯引号 | `validate_translations.py --changed` 验证 21 个修改文件；18 组重复术语审计零不一致；`git diff --check` 通过；BOM/LF/末尾换行保持；RPA 成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano14.rpy` | Tony 探监离城；Maria 独守披萨店；第四面墙强制引导 | Anon、Tony、Maria | 完成 | 通读 79 个翻译块并精修 67 处；区分多日条件分支和送餐成败回应，统一 Tony/Maria 老派口吻，修复第三次强制引导的元叙事、海滨公寓302室、好感度提示及全部活动译文 ASCII 省略号 | `validate_translations.py --changed` 验证 22 个修改文件；19 组重复术语审计零不一致；`git diff --check` 通过；BOM/CRLF/末尾换行保持 |
| `tl/zh_hans/src/plot/ano15.rpy` | 俄国人走私窝点情报；自然受孕交易；Tony/Maria/Anon 成人关系分支 | Anon、Tony、Maria、Eddie Four-Fingers（被提及） | 完成 | 通读 754 个翻译块并精修 490 处；修复俄国人情报、自然受孕条件、Maria 婚姻忠诚冲突、成人关系阶段和食物/棒球/性行为双关；固定“冠军”“补水最重要”“卡皮科拉火腿”“锉刀”等术语，并恢复 `Obi-Wan` 英文专名 | `validate_translations.py --changed` 验证 23 个修改文件；22 组重复术语审计零不一致；`git diff --check` 通过；RPA 成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/ano16.rpy` | Maria 怀孕确认；邀请 Anon 当教父；俄国人地址与版本结尾占位 | Anon、Tony、Maria | 完成 | 通读 52 个翻译块并精修 41 处；修复 `I'm ya guy` 反译、`champ` 称呼漂移、教父/黑帮双关、Tony/Maria 家人式关系、版本更新元叙事及活动译文 ASCII 省略号 | `validate_translations.py --changed` 验证 24 个修改文件；23 组重复术语审计零不一致；`git diff --check` 通过；RPA 成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/anon_chair.rpy` | Anon 卧室；检查卡死的椅子脚轮 | Anon | 完成 | 通读 5 个翻译块并精修全部译文；理顺用力、发现脚轮卡死及“没锁就好办”的连续思路 | `validate_translations.py --changed`、`git diff --check`、BOM/CRLF/末尾换行保持检查通过 |
| `tl/zh_hans/src/plot/anon_pc.rpy` | Anon 卧室；电脑故障、零件线索、道具检查、修复与画质升级 | Anon、mono | 完成 | 通读 15 个翻译块并精修 14 处；保留空 `mono` 块、Consum-R 专名、成人用品语境和电脑修复/高分辨率/游戏 BUG 元叙事 | `validate_translations.py --changed`、25 组重复术语审计零不一致、RPA 构建/校验通过 |
| `tl/zh_hans/src/plot/anon_phone.rpy` | 手机 Wi-Fi 设置连续点击彩蛋 | Anon | 完成 | 通读 8 个翻译块并精修 6 处；将八条警告整理为“查看信号—制止点击—识破意图—解锁作弊菜单”的递进序列 | `validate_translations.py --changed`、`git diff --check`、RPA 构建/校验通过 |
| `tl/zh_hans/src/plot/apt_empty.rpy` | 公寓入口；深夜与未受邀访问拦截 | Anon | 完成 | 通读 4 个翻译块并精修 3 处；修复 ASCII 省略号和“不请自来”的翻译腔，保持尴尬递进 | 本批 10 个 Ren’Py 文件格式校验通过 |
| `tl/zh_hans/src/plot/bank_hall.rpy` | 银行后场员工区拦截 | Anon | 完成 | 通读并精修 2 个翻译块；将地点指代改为自然的“后面/员工区”，保留擅入后果 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/bank_lobby.rpy` | 银行闭店、周末营业与禁止逗留提示 | Anon、more | 完成 | 通读 7 个翻译块并精修 5 处；降低 `Dang it` 过度粗俗译法，修复直角引号并理顺“办事后离开”的连续思路 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/bank_vault.rpy` | 银行金库上锁提示 | Anon | 完成 | 通读并精修 2 个翻译块；保留先自嘲“明知故说”再确认上锁的笑点 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/car_garage.rpy` | 车行维修区拦截 | Anon | 完成 | 通读并精修 2 个翻译块；修复“它们修车”的代词错误及 ASCII 省略号 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/car_lounge.rpy` | 车行员工休息区拦截 | Anon | 完成 | 通读并精修 2 个翻译块；自然化 `employee only vibes`，原样保留 `{i}` 标签 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/car_shop.rpy` | 车行闭店与即将闭店提示 | Anon | 完成 | 通读 3 个翻译块并精修全部译文；统一自然简短的闭店提示语气 | `git diff --check`、RPA 打包/校验 328 个文件通过 |
| `tl/zh_hans/src/plot/erik_bed.rpy` | Erik 卧室；检查床底并发现书 | Anon | 完成 | 通读并精修 2 个翻译块；将 `dust bunnies` 自然化为“灰尘团”，保持先检查再发现物品的连续节奏 | 本批 13 个 Ren’Py 文件格式校验通过 |
| `tl/zh_hans/src/plot/erik_drawer.rpy` | Erik 卧室；检查凌乱抽屉 | Anon | 完成 | 通读并精修 3 个翻译块；修正 `dresser` 的“梳妆台”误译，保留对污渍的惊讶和嫌弃但不补写来源 | 本批格式校验、`git diff --check` 通过 |
| `tl/zh_hans/src/plot/tech_gamepad.rpy` | Erik 卧室；旧游戏手柄与童年回忆 | Anon、Erik（变量） | 完成 | 通读并精修 2 个翻译块；修复缺失主语、ASCII 省略号和生硬回忆表述，保留两人如今已很少一起玩的惋惜 | RPA 成功打包并验证 328 个文件 |
| `tl/zh_hans/src/plot/debbie_attic.rpy` | Debbie 家阁楼；借凳子进入与旧物期待 | Anon、Debbie、Dad（叙述中） | 完成 | 通读 4 个翻译块并精修全部译文；自然化进入阁楼与寻找垫脚物的表达，保留明确亲属称谓“爸爸”，修复 ASCII 省略号 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/debbie_bed1.rpy` | Debbie 卧室；进入限制、睡眠与潜入状态提示 | Anon、Debbie（变量） | 完成 | 通读 4 个翻译块并精修全部译文；简化重复主语，统一卧室隐私和保持安静的内心独白语气 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/debbie_canvas.rpy` | Debbie 家旧画布；回忆其绘画爱好 | Anon、Debbie（变量） | 完成 | 通读并精修 1 个翻译块；将生硬的过去时表达改为自然回忆，确认 Debbie 以前很喜欢画农场动物 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/debbie_drawer.rpy` | Debbie 卧室；抽屉与内裤抽屉隐私提示 | Anon、Debbie（变量） | 完成 | 通读 3 个翻译块并精修全部译文；明确 `panty drawer` 为“内裤抽屉”，保留对玩家/自己的共同警告与越界感，不额外扩写 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/debbie_landing.rpy` | Debbie 家楼梯平台；浴室门缝偷看提示 | Anon | 完成 | 通读 4 个翻译块并精修 3 处；修复病句和 ASCII 省略号，理顺发现门缝、好奇与自我开脱的心理递进 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/photo_debbie_diane.rpy` | Debbie/Diane 夏令营旧照片 | Anon、Debbie、Diane（变量） | 完成 | 通读并精修 2 个翻译块；修复女性复数代词误用和ASCII内心独白括号，保留两人年轻时共同参加夏令营的时间与情绪信息 | 本批格式校验通过 |
| `tl/zh_hans/src/plot/pie_stall.rpy` | 商场摊位；Pietro 涂油误会、腹肌自恋与厕所隔间逃跑 | Anon、Pietro、摊位员工 | 完成 | 完整通读28个活动翻译块并结合角色动作参数复原误会：Pietro误以为Anon来帮他涂油，Anon拒绝后又被误解为否定腹肌；统一`Adonis`为“阿多尼斯”、破折号、省略号和全角内心独白，保留自恋喜剧及Anon事后担心员工受牵连的收尾 | 英文原文注释diff通过（无UTF-8 BOM、111个裸LF、0个CRLF、文件末尾LF、28个活动翻译块、0组菜单映射） |
| `tl/zh_hans/src/plot/jen01.rpy` | Jenny线；浴室偷窥、被发现及前期敌对关系 | Jenny、Anon、Debbie（被提及） | 完成 | 通读完整场景并精修 31 个翻译块；将 `You! / Little! / PERVERT!!!` 作为被吹风机击打打断的连续辱骂处理，修复“娃娃脸”误译；保留偷窥事实、Jenny 的尖刻攻击性及 Anon 求情逻辑，统一中文省略号与标点 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过（327 个文件） |
| `tl/zh_hans/src/plot/jen02.rpy` | Jenny线；新衣争执、求职压力、搬家宣言及家庭责任对照 | Jenny、Debbie、Anon | 完成 | 通读完整场景并精修 58 个翻译块；Consum-R现统一为“购乐百货”，理顺 Jenny 的讽刺与负担感、Debbie 的经济压力和安抚、Anon 的挖苦与体谅；统一 `sweetie`“亲爱的”、`good boy`“好男孩”及连续拆句 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过（327 个文件） |
| `tl/zh_hans/src/plot/jen03.rpy` | Jenny线；早餐赌气、借款争执及赚钱计划铺垫 | Jenny、Debbie、Anon、Diane（被提及） | 完成 | 通读完整场景并精修 67 个翻译块；承接 `jen02.rpy` 的家庭争执，理顺 Jenny 拒绝早餐、借六十美元、含糊赚钱计划与学费压力；区分 Jenny 的讽刺、Anon 的反驳和 Debbie 的照顾者语气，统一 `sweetie`“亲爱的”、中文省略号及活动译文标点 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过（327 个文件） |
| `tl/zh_hans/src/plot/jen04.rpy` | Jenny线；夜间色情影片角色扮演、再次偷窥、吹风机反击与勒索 | Jenny、Anon、Debbie（被提及）、影片男声 | 完成 | 通读完整场景并精修 63 个翻译块；理顺 Anon 误以为 Jenny 带男人回家、发现她跟随影片进行角色扮演、暴露后再次挨打及按现金量分支交钱的因果；统一 Jenny 对 Anon 的 `perv/pervert` 为“变态”，将色情角色称谓 `Daddy` 译为“爸爸”并与真实亲属关系区分，保留成人内容强度及中文引号、省略号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过（327 个文件） |
| `tl/zh_hans/src/plot/jen05.rpy` | Jenny线；Sluttygram 赚钱计划、首次合作拍摄性感照片与关系短暂缓和 | Jenny、Anon | 完成 | 通读 129 个翻译块和 7 项拍照选项；理顺粉丝焦虑、社交媒体建议、拒绝回 Consum-R、逐步增加暴露程度及拍完立即赶人的关系变化；保留Sluttygram英文专名；Consum-R现统一为“购乐百货”，统一 `perv`“变态”、本场 `wimp`“窝囊废”、连续拆句、拍摄评价和中文省略号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过（327 个文件） |
| `tl/zh_hans/src/plot/jen06.rpy` | Jenny线；潜入卧室寻找照片、翻看日记、内裤误会及付费看图交易 | Jenny、Anon、Debbie（被提及） | 完成 | 通读 105 个翻译块和 2 项分支选项；理顺潜入卧室、日记与内裤被撞见、六十美元看图交易、还价/央求/拒绝分支及逐张照片评论；修复反译、内心独白括号、ASCII 省略号与连续讽刺，统一本场 `loser`“废柴”、`perv/pervert`“变态”并保留性欲和自慰表达强度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/jen07.rpy` | Jenny线；Sluttygram 收入争执、两百美元看胸/摸胸交易及首次吸吮越界 | Jenny、Anon、Debbie | 完成 | 通读并精修 177 个翻译块；理顺早餐争执、免费色情内容竞争、强迫承认吸引力、付费看胸与摸胸流程，以及 Anon 越界吸吮乳头后 Jenny 有快感但仍叫停的关系推进；修复 `Poor thing`“娃娃脸”等错译，统一 `loser`“废柴”、内心独白括号、中文省略号和连续拆句 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`、RPA 构建通过 |
| `tl/zh_hans/src/plot/jen08.rpy` | Jenny线；情趣玩具差事、Pink退货争执与裸体奖励 | Jenny、Anon、Jane、Ivy | 完成 | 通读完整文件及普通/强势分支；精修电击阴蒂棒代购、Pink店内退货争执、Jane与Ivy成人互动、付款/棒棒糖分支及Jenny裸体履约；统一 `loser`“废柴”、`perv`“变态”、产品名与女性高潮表达 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen09.rpy` | Jenny线；虚构录音转写工作与收入来源质疑 | Jenny、Anon、Debbie | 完成 | 通读完整文件；精修Jenny向家里交钱、以录音转写掩饰收入、Debbie欣慰邀请早餐、Anon看穿谎言并担忧其为钱越界的对质；保持关系仍处于隐瞒与怀疑阶段 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen10.rpy` | Jenny线；商场同行、Grace重逢及Pink情趣用品采购 | Jenny、Anon、Grace、Ivy、Eve/Odette（条件分支） | 完成 | 通读 388 个翻译块；精修索要两百美元与普通/强势同行分支、Grace高中同学重逢、工作与住家自卑、Eve/按摩油条件对话、UltraVibe 2000和大型肛塞采购；恢复 `Sugar Tats` 英文店名，统一 `loser`“废柴”、`perv`“变态”、Ivy的 `cutie`“小帅哥”及活动译文标点 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen11.rpy` | Jenny线；日记揭密、成人直播真相与笔记本潜入计划 | Jenny、Anon | 完成 | 通读完整文件及重复调用块；精修日记调查、自慰直播真相、最喜欢玩具的密码线索、白天潜入险被抓及改为夜间行动的计划；修复新增变量并统一中文引号、省略号和内心独白 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen12.rpy` | Jenny线；夜间潜入笔记本、CAMslut主页、远程访问及视频观看 | Jenny、Anon | 完成 | 通读完整文件；精修潜入时机、密码线索、被抓分支、Alt+F4失败笑点、远程访问重试及自慰/潮吹视频反应；统一 `CAMslut`、`Seddit` 英文专名、中文内心括号与引号，明确“真鸡巴”是Jenny面对观众提出的后续尺度 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen13.rpy` | Jenny线；CAMslut新视频诱因、坏怪物礼物及直播性交计划 | Jenny、Anon、Jane（电话） | 完成 | 通读完整文件；精修主页调查、宣传视频推断、Pink取玩具、Jane电话、日记嫌疑掩饰、礼物反应及新视频回报；统一 `CAMslut` 英文专名和 `Bad Monster`“坏怪物”，修复英文残留、中文引号、省略号和内心独白 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen14.rpy` | Jenny线；Cedric拒绝成人直播、裸体跑腿交易及手指高潮/潮吹 | Jenny、Anon、Debbie、Cedric | 完成 | 通读完整文件及重复调用块；精修早餐冲突、录音转写掩饰、Cedric传话、裸体与全身触摸交易、乳房刺激和手指高潮分支；修复两处严重错位译文、新增斜体标签、中文问号乱码及英文原文注释，统一 `loser`“废柴”、中文双引号和女性潮吹表达 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen15.rpy` | Jenny线；直播被偷看、观众撮合Anon及三倍报价施压 | Jenny、Anon、CAMslut观众 | 完成 | 通读完整场景；精修肛塞与坏怪物直播话题、观众发现背景人物、Jenny拿巨型假阳具驱赶Anon、观众要求两人性交及三倍报价后的动摇与拒绝；修复三处会被Ren’Py误当插值的方括号文本，统一 `pervert`“变态”、`loser`“废柴”、中文省略号和全角内心括号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen16.rpy` | Jenny线；望远镜偷窥Mia、首次查看Anon阴茎及蒙面成人直播提议 | Jenny、Anon、Mia、Lily、Pink Cyclone | 完成 | 通读完整文件；精修偷窥Mia自慰、Jenny主动查看并触摸Anon阴茎、普通/强势谈判、成人直播边界、收益分成、面具任务及错过约定后的冲突；恢复 `Pink Cyclone` 英文专名，统一 `loser`“废柴”、成人直播、面具、中文省略号和全角内心括号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen17.rpy` | Jenny线；Cosmic Cumics摔角游戏活动、Pink Cyclone见面及直播面具取得 | Anon、Erik、Pink Cyclone、Lily、Karl、Justin、Jenny | 完成 | 通读完整文件及重复调用块；精修WPWF战绩争论、World of Orcette公会角色扮演、Justin表白被头锁、Pink Cyclone身份口误、签名海报与附赠面具流程，以及Jenny的直播预热安排；修复多处严重错位、空译文和新增变量/标签问题，保持英文姓名及非地点专名，店名按地名专项规则处理 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen18.rpy` | Jenny线；首次蒙面成人直播、手淫射精及取消/重试分支 | Jenny、Anon、CAMslut观众 | 完成 | 通读完整文件；精修直播确认、镜头控制、打赏吊胃口、勃起失败与主动唤起、手淫和射精的提醒/未提醒分支、报酬结算、临时取消与暴怒重试；统一 `Sam9`、面具、成人直播、打赏和连续笑点“鸡巴替身”，明确男性射精及Jenny被射到身上的失控反应 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen19.rpy` | Jenny线；射精事故后的和解、直播分成与下一场约定 | Jenny、Anon、Debbie | 完成 | 通读完整文件；精修早餐前道歉失败、床单与精液话题、Jenny从愤怒转向承认高收益、支付分成和默认继续合作，以及Debbie出现后的共同掩饰；统一中文省略号、全角内心括号和成人直播语境 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen20.rpy` | Jenny线；客厅自慰被撞见、首次足交与舔脚挑逗 | Jenny、Anon、Debbie（睡眠中被提及） | 完成 | 通读完整文件；精修电视调查、Jenny观看足交影片自慰、被发现后的愤怒与主动转折、足交射精、事后洗脚及舔脚趾挑逗；统一 `loser`“废柴”、`perv`“变态”、男性射精表达、全角内心括号和中文省略号 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen21.rpy` | Jenny线；手铐支配直播、舔屄高潮、首次口交及吞精分支 | Jenny、Anon、CAMslut观众 | 完成 | 完整对照英文原文精翻；修复直播邀请、手铐和“公主/小男宠”支配称谓、强制舔屄、Jenny高潮、观众高额打赏要求吹箫、射进喉咙后的意外/故意吞精分支及错过直播重试；清理英文标点残留和机翻拟声 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen22.rpy` | Jenny线；直播结算、技巧承认与桃子双关 | Jenny、Anon、Debbie | 完成 | 完整对照英文原文精修；理顺直播分成争执、舔屄技巧的险些承认、后续舔屄/吹箫约定，以及Debbie出现后的“桃子、汁水、完事、满脸、头发”连续双关；修复女性高潮误写为射精，统一 `camshow`“成人直播”、`loser`“废柴”和中文标点 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen23.rpy` | Jenny线；望远镜刺激、礼貌请求、坐脸与揉奶高潮分支 | Jenny、Anon、Tammy、Erik | 完成 | 完整通读全部条件分支并对照英文精修；理顺Tammy/Erik舔屄与裸体健身球望远镜场景、Jenny发现Anon与Tammy的性关系、非商业主动索取舔屄、Anon要求礼貌请求、主路线坐脸哼歌高潮，以及替代路线被子报复、揉奶请求和高潮；统一 `loser`“废柴”、`little whipping boy`“出气筒”，修复女性高潮措辞并保留《Kung Fu Fighting》含混歌词的重复一致性 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen24.rpy` | Jenny线；啦啦队制服、首次直播性交与控制权反转 | Jenny、Anon、Debbie、CAMslut观众 | 完成 | 完整通读全部场景和强势／顺从分支并三轮对照精修；理顺早餐索取旧制服、Jenny迁怒Debbie与被迫道歉、阁楼取衣、啦啦队长身份、手铐“公主”支配玩法、首次直播性交、未挣脱路线的骑乘与差十秒高潮、挣脱路线的控制权反转，以及外射／内射和怀孕风险；统一啦啦队术语、`PING`“叮”、`CAMslut`平台名与小写`camslut`泛称 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen25.rpy` | Jenny线；泳池偷窥者、临时男朋友与电影院线索 | Jenny、Anon、Debbie、Zana（尚未揭名） | 完成 | 完整通读文件并结合`jen26.rpy`后续揭示复核；修复晒黑／晒伤严重错译、树篱偷窥者动作、第三次出现、追赶失败及电影院宣传品线索；保留“男朋友”仅为吓退跟踪狂的临时冒认，同时体现首次直播性交后Anon借题调侃的暧昧张力；统一`loser`“废柴”、`boyfriend`“男朋友”、`stalker`“跟踪狂”和中文标点 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`通过 |
| `tl/zh_hans/src/plot/jen26.rpy` | Jenny线；电影院约会、Zana对质、公开影厅高潮与夜间主动性交 | Jenny、Anon、Debbie、Zana、电影院观众 | 完成 | 完整通读全部449个翻译块并多轮对照精修；理顺Zana跟踪与刑事骚扰、免费电影票、否认约会、童年卡通回忆、零食与片名、签名挥拳双关、公共影厅手部刺激、回家真诚感谢、半夜主动骑乘、留宿争执及怀孕状态内射分支；修复串行错译和问号占位，统一成人直播、虫形软糖、电影标题、女性高潮、男朋友误认和中文标点 | `validate_translations.py --changed`验证16个修改文件；重复术语审计零不一致；`git diff --check`、英文注释diff、BOM/CRLF/行数检查通过 |
| `tl/zh_hans/src/plot/jen27.rpy` | Jenny线；暂不搬家、早餐关系摊牌与正式约会拒绝 | Jenny、Anon、Debbie | 完成 | 完整通读64个翻译块并逐块复核；修复家庭开支语义、Anon对搬家的恐慌、谈恋爱与单纯约会的关系差异、做爱和成人直播收益、结婚生子与白色尖桩篱笆意象、失去胃口离席及Anon主观猜测；统一全角内心括号、中文省略号和Jenny的恋爱排斥口吻 | `validate_translations.py --changed`验证17个修改文件；重复术语审计零不一致；`git diff --check`、英文注释diff及BOM/CRLF/行数检查通过 |
| `tl/zh_hans/src/plot/jen28.rpy` | Jenny线；第三次恋爱拒绝、失败送礼与付费女友体验 | Jenny、Anon、Debbie（被提及）、两人的孩子（条件分支） | 完成 | 完整通读161个翻译块和1个菜单映射并逐条复核；理顺怀孕／育儿／成人直播条件开场、“像跟兄弟谈恋爱”的拒绝理由、Anon翻日记与项链送礼、假女朋友提案、甜蜜告白演技骗局、一晚五百美元及次晨条件；修复 `girlfriend the shit out of you` 与 `the real thing` 严重错译，统一成人直播、废柴、爸爸、女友体验及中文标点 | `validate_translations.py --changed`验证19个修改文件；重复术语审计零不一致；`git diff --check`、英文注释diff及BOM/CRLF/块数检查通过 |
| `tl/zh_hans/src/plot/jen_gfe.rpy` | Jenny线；居家付费女友体验、亲密升温与次晨收费界限 | Jenny、Anon、Debbie、Diane、Cedric（被提及），Matt、Courtney（剧中人物） | 完成 | 完整通读365个翻译块和2组菜单映射并逐条复核；理顺五百美元付款、居家约会、牵手冲突与主动修复、共同观看《好友》、接吻和多条性交分支、重复约会夜及次晨离开；明确“假装当女朋友”仍是收费角色扮演，修复女性高潮、内外射、成人直播、Debbie起床与口水指代等严重错译；恢复Matt、Courtney英文姓名并统一中文标点 | `validate_translations.py --changed`验证19个修改文件；重复术语审计零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/365块/2组菜单检查通过 |
| `tl/zh_hans/src/plot/jen_cam.rpy` | Jenny线；重复成人直播、怀孕表演、吹箫、私人舔屄与预约分支 | Jenny、Anon、观众（文字互动） | 完成 | 完整通读195个翻译块并逐条复核；理顺普通直播、怀孕身体展示与泌乳、手铐坐脸、观众打赏要求吹箫、忙碌／无兴致拒绝、私人舔屄、啦啦队制服性交及后续预约；修复手交误译，统一成人直播、打赏、小男宠、出气筒、被人围观、女性高潮和中文标点；明确重复事件不确认正式恋爱关系 | `validate_translations.py --changed`验证20个修改文件；重复术语审计47项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/195块/0组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_baby.rpy` | Jenny线；怀孕、孕期成人直播、生产与共同育儿 | Jenny、Anon、Debbie、Diane、医护人员、直播观众 | 完成 | 完整通读919个翻译块和11组菜单映射；复核首次／再次怀孕、孕期不适与异常食欲、Debbie发现怀孕、两组孕期成人直播、诊所与单胎／双胎生产分支、产后护崽和托儿安排；修复主客体反译、亲属称谓、男朋友口误边界、含混口齿及女性高潮误写，统一成人直播、打赏、小男宠、外婆、护崽母熊和中文标点 | `validate_translations.py --changed`验证21个修改文件；重复术语审计48项零不一致；`git diff --check`、英文注释diff及无BOM/LF/919块/11组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_deal.rpy` | Jenny线；公共区域议价、保密提醒与下午付费安排 | Jenny、Anon、Debbie（被提及） | 完成 | 完整通读7个翻译块并精修6处；结合付费女友体验及稳定性关系阶段，明确 Anon 提议的是私下交易，Jenny 因担心 Debbie 撞见而制止当场讨论，并要求下午再来且带钱；修复“别在这”的指代含混、`catch us` 场景语义和生硬回应，保持 Jenny 粗鲁、直接、商业化的口吻 | `validate_translations.py --changed`验证22个修改文件；重复术语审计48项零不一致；`git diff --check`、英文注释diff及BOM/CRLF/7块/0组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_finger.rpy` | Jenny线；私人前戏、指交高潮与中途停止反制 | Jenny、Anon、Jane（被提及） | 完成 | 完整通读95个翻译块和2组菜单映射并精修51处；明确 Jenny 将亲热默认理解为成人直播、Anon 主动要求前戏、完成分支中 Jenny 高潮潮吹并取消直播、停止分支中 Anon 把她吊在高潮边缘后逃走的控制权反转；修复 `fool around`、`C'mon`、`get down to business`、`cum for me`、内心独白括号和活动译文标点，保持女性高潮与男性射精语义分离 | `validate_translations.py --changed`验证23个修改文件；重复术语审计48项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/95块/2组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_pool.rpy` | Jenny线；泳池性交、溺水笑点、裸泳反悔与支配角色扮演 | Jenny、Anon、Debbie（被提及） | 完成 | 完整通读156个翻译块并精修106处；理顺泳池性交和接近溺水、体外／内射分支、后院乳房照片、裸泳承诺反悔、炸弹入水报复及跳过道歉直接做爱；保留 `Screw you` 的辱骂／性交双关和公主Jenny／殿下／贱民角色扮演，明确稳定性关系延续但未正式确认恋爱 | `validate_translations.py --changed`验证24个修改文件；重复术语审计51项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/156块/0组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_shower.rpy` | Jenny线；前期偷窥、共同淋浴、狗狗支配、淋浴性交与私人吞精承认 | Jenny、Anon、Debbie（被提及）、直播粉丝（被提及） | 完成 | 完整通读326个翻译块和2组菜单映射并精修209处；区分前期偷窥冲突、成人直播合作后的共同淋浴、怀孕身体不安及生气条件分支，理顺狗狗／奖励／乞求玩法与 Anon 明确拒绝羞辱的边界协商；修复淋浴性交、深喉、吞精、女性高潮、体外／内射结果和内心独白括号，明确 Jenny 私下承认喜欢吞精及大鸡巴却仍否认喜欢 Anon | `validate_translations.py --changed`验证25个修改文件；重复术语审计51项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/326块/2组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_sleep.rpy` | Jenny线；夜间同床试探、前戏、外射留宿、内射冲突与次晨斗嘴 | Jenny、Anon、Debbie（被提及） | 完成 | 完整通读133个翻译块和6组菜单映射并精修90处；区分关系早期的越界失败入口与稳定性关系后的成功入口，理顺“只为做爱、不为搂着睡”的边界、前戏承认、中途停止反制、外射后精液清理与同床留宿、内射许可冲突及次晨厨艺斗嘴；统一废柴、巨婴、吊胃口反制、内心独白括号和中文标点，明确共享睡眠推进仍不等于正式恋爱 | `validate_translations.py --changed`验证26个修改文件；重复术语审计51项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/133块/6组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_table.rpy` | Jenny线；餐桌冒险性交、早餐倒计时、咖啡杯体外结果与内射许可冲突 | Jenny、Anon、Debbie | 完成 | 完整通读158个翻译块并精修103处；确认稳定性关系阶段下 Jenny 故意选择 Debbie 在隔壁做早餐时于餐桌性交，并以备餐时间倒计时；理顺高风险挑衅、早餐／性交双关、险些被发现、体外射进咖啡杯导致 Debbie 喝到怪味、Jenny 未高潮抱怨及内射怀孕威胁；统一 `fool around` 为“亲热一下”，修复女性高潮、内射许可和中文标点，明确“别停”不等于允许内射且正式情侣关系仍未确认 | `validate_translations.py --changed`验证27个修改文件；重复术语审计52项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/158块/0组菜单检查通过 |
| `tl/zh_hans/src/plot/jen_tv.rpy` | Jenny线；色情片账号、支配乞求、足交与客厅冒险性交 | Jenny、Anon、Debbie（睡觉／被提及）、Diane（被提及） | 完成 | 完整通读145个翻译块和1组菜单映射并精修96个翻译块及1个菜单；区分拒绝／乞求分支并确认两者汇合为足交，理顺公主支配、自我羞辱、Jenny 主动转为客厅性交、Debbie 隔壁风险刺激、体外射身及高潮夹住导致内射的责任争吵；修复 `let me finish` 严重误译、女性高潮、废柴固定辱称、内心独白括号和中文标点，明确稳定性关系仍需家庭保密且未确认正式恋爱 | `validate_translations.py --changed`验证28个修改文件；重复术语审计53项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/145块/1组菜单检查通过 |

| `tl/zh_hans/src/plot/jen_visit.rpy` | Jenny线；深夜夜访、主动索取、明确拒绝与控制欲反弹 | Jenny、Anon | 完成 | 完整通读37个有活动台词的翻译块、1个空白汇合块和2组菜单映射，并精修26个翻译块及1个菜单；区分接受、好声请求后离开及因拒绝报复下体的分支，明确 Jenny 的私人性需求已脱离直播和付费借口，同时保留身体反应不等于同意、Anon 明确说不和 Jenny 无法接受失去控制的冲突；修复 `I need it`、`y-yes?` 回应误译、连续引述、重复惊讶口吻、中文省略号和标点 | `validate_translations.py --changed`验证29个修改文件；重复术语审计53项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/38块（含1个空白汇合块）/2组菜单检查通过 |

| `tl/zh_hans/src/plot/jenny_laptop.rpy` | Jenny线前置；笔记本调查、Pink Channel 账号与三段早期个人成人直播 | Jenny、Anon、Jane（照片）、sam9／Sam（观众） | 完成 | 完整通读150个翻译块并精修102个翻译块；理顺笔记本密码调查、邮件与家庭照片、Pink Channel 账号、三段个人成人直播中玩具升级、肛塞、订阅墙与打赏递进；修复 `cum all over this toy` 和 `fuck myself silly` 的严重动作误译，统一女性高潮、成人直播 `PING`、`tips`、“性爱女神”、内心独白括号和中文标点；明确这是 Anon 加入直播合作前的早期阶段，不能套用后期稳定性关系 | `validate_translations.py --changed`验证30个修改文件；重复术语审计54项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/150块/0组菜单检查通过 |

| `tl/zh_hans/src/plot/jenny.rpy` | Jenny线公共入口；卧室、餐厅与后院的多阶段互动 | Jenny、Anon、Debbie／Jane（被提及） | 完成 | 完整通读149个活动翻译块和7组菜单映射，精修92个翻译块及4个菜单；区分前期卧室驱赶与泳衣搭话冲突、成人直播合作和休息日、拒播造成的收入争执、餐厅评论区与后期约播、后院从敌意到裸体风险调戏的阶段变化；修复 `loser` 四处漂移、`Hell yeah!`、直播指代、内心独白括号和中文标点，并统一 `camgirl` 为“成人女主播” | `validate_translations.py --changed`验证31个修改文件；重复术语审计55项零不一致；`git diff --check`、英文注释diff及有BOM/LF/149块/7组菜单检查通过 |
| `tl/zh_hans/src/plot/jos01.rpy` | Josie线；车行初见、手机交易、办公室潜入与求开除之吻 | Josie、Anon、Yoshi、Yoo | 完成 | 完整通读391个活动翻译块和2组菜单映射，精修224个活动译文及1个菜单；修复第278–286条整段译文严重错位，理顺Yoo强行推销、父女工作冲突、T字带凉鞋抢购、手机交易、三头猴/墙上剑两个办公室分支，以及Josie利用接吻求开除却开始对Anon产生兴趣的关系边界；统一锅盖头、TPS报告、T字带凉鞋及英文姓名，并保留Freetwood Panhandrer/Fleetwood Panhandler、J-Ro/J-Lo连续笑点 | `validate_translations.py --changed`验证32个修改文件、重复术语审计58项零不一致、`git diff --check`及英文注释diff通过；无BOM、CRLF/391块/2组菜单结构已核验 |
| `tl/zh_hans/src/plot/jos_trade.rpy` | Josie线；旧车折价、三类车型报价与阶段性交易入口 | Josie、Anon | 完成 | 完整通读132个活动翻译块和9组菜单映射，精修109个活动译文及9个菜单；理顺踏板车、迷你外阴、过度补偿者三种旧车状态，404里程笑点，预算／四轮／跑车／离开分支，系统底价、15%促销折扣、旧车折价、首次成交与再次报价；区分锅盖头早期挖苦、姓名变体、讨厌工作与承认喜欢Anon的阶段差异，修复Mini Vulva三处漂移、SL-700 Crotch Rocket两处不一致、Cotton姓名泛化、中文省略号和菜单语气 | `validate_translations.py --changed`验证33个修改文件；重复术语审计60项零不一致；`git diff --check`及英文注释diff通过；无BOM、832个CRLF、833行、132个活动翻译块/9组菜单结构已核验 |
| `tl/zh_hans/src/plot/josie.rpy` | Josie线公共入口；Debbie车辆话题、购车路由与双阶段招呼 | Josie、Anon、Debbie（菜单提及） | 完成 | 完整通读15个活动翻译块和2组菜单映射，精修9个活动译文及1个菜单；确认文件连接`deb13.rpy`车辆保修与`jos_trade.rpy`购车系统，保留早期低头玩手机、冷淡“有事？”和“锅盖头”告别，与后期直呼姓名、主动询问陪伴的平行关系变化；修复ASCII省略号、英文问号、`Later`直译“稍后”及菜单书面腔 | `validate_translations.py --changed`验证36个修改文件；重复术语审计62项零不一致；`git diff --check`、英文注释diff及有BOM/LF/15个活动翻译块/2组菜单结构检查通过 |
| `tl/zh_hans/src/plot/yoshi.rpy` | 车行经理公共入口；办公室询问、手机分支与临近打烊 | Yoshi、Anon、Josie（提及） | 完成 | 完整通读12个活动翻译块和2组菜单映射，精修8个活动译文及2个菜单；保持Yoshi面对顾客的正式销售口吻，统一两个相同离开块，明确`Phone.`专指被扣下的Josie手机、`I’m good.`是婉拒帮助，并保留`tend to your needs`的轻微双关 | `validate_translations.py --changed`验证36个修改文件；重复术语审计62项零不一致；`git diff --check`、英文注释diff及有BOM/CRLF/12个活动翻译块/2组菜单结构检查通过 |
| `tl/zh_hans/src/plot/yoo.rpy` | 车行销售公共入口；月度最佳员工炫耀、贫穷羞辱与投诉冲突 | Yoo、Anon | 完成 | 完整通读44个活动翻译块和3组菜单映射，精修32个活动译文及1个菜单；理顺接管车行、全国连锁、征服全球和车行之神的夸张递进，修复`You stirr tarking?`严重误译、`N-no.`回应、贫穷假哭、投诉与业绩头衔；统一`poor boy`为“穷小子”、`Employee/Emproyee of month`为“月度最佳员工”，并保留破碎语法而不制造中文错字或种族口音 | `validate_translations.py --changed`验证36个修改文件；重复术语审计62项零不一致；`git diff --check`、英文注释diff及无BOM/CRLF/44个活动翻译块/3组菜单结构检查通过 |
| `tl/zh_hans/src/plot/jud01.rpy` | Judith线；共用男生更衣室事件后的感谢、安心与初步暧昧 | Judith、Anon、Annie（提及） | 完成 | 完整通读16个活动翻译块；结合`ano01.rpy`前置事件，理顺Judith感谢陪伴与替她反驳Annie的原因，修复`made me feel safe`、`stood up to`和`do the right thing`的直译；保留她谈到Anon裸体时先脱口“我还挺喜欢——”再慌忙改口的羞怯失言，统一“男生更衣室”术语 | `validate_translations.py --changed`验证39个修改文件；重复术语审计66项零不一致；`git diff --check`、英文注释diff及文件结构检查通过（有BOM、CRLF、16个活动翻译块、0组菜单） |
| `tl/zh_hans/src/plot/jud02.rpy` | Judith线；走廊霸凌、隔间安慰与首次互相触摸 | Judith、Anon、Val、Camila、Annie（提及） | 完成 | 完整通读115个活动对话翻译块和8组菜单映射，精修77处译文与菜单；结合`ano01.rpy`、`jud01.rpy`确认关系阶段，理顺身材羞辱、自我否定、安慰／伤害自尊分支，以及看阴茎、手交、摸胸、中途停止和离开分支；保留Judith害羞迟疑却主动试探的口吻，修复内心独白括号、ASCII省略号、成人动作弱化和`white boy`误译 | `validate_translations.py --changed`验证39个修改文件；重复术语审计66项零不一致；`git diff --check`、英文注释diff及文件结构检查通过（无BOM、LF、115个活动对话翻译块、8组菜单） |
| `tl/zh_hans/src/plot/jud_stall.rpy` | Judith线可重复私下亲热场景；再次邀约、初吻、摸胸与完成手交 | Judith、Anon | 完成 | 完整通读92个活动翻译块，精修70处译文（Git实际69行变更）；承接`jud02.rpy`首次互相触摸，明确有空／拒绝入口、初吻、多次接吻、再次摸胸、手交至射精、弄脏衬衫及改天再来；保留Judith持续结巴、征求确认与可拒绝边界，修复`fool around`误译、内心独白括号、ASCII省略号、男性射精弱化及身体部位机械直译，并恢复三组食物式感叹口癖 | `validate_translations.py --changed`验证39个修改文件；重复术语审计66项零不一致；`git diff --check`、英文注释diff及文件结构检查通过（有BOM、CRLF、92个活动翻译块、0组菜单） |
| `tl/zh_hans/src/plot/judith.rpy` | Judith线公共入口；美术教室自嘲寒暄、走廊低落问候与任务菜单 | Judith、Anon | 完成 | 完整通读19个活动翻译块和3组菜单映射，精修12处译文；结合公共入口的跨阶段用途与实际路由，保留Judith喜欢美术却自嘲画技的轻松笑点，以及走廊中低落、沉默和尴尬告别的社交羞怯；将3处ASCII省略号改为全角省略号，并确认`Specs.`指眼镜、`Bathroom fun.`指向`jud_stall.rpy`亲热事件 | `validate_translations.py --changed`验证45个修改文件；重复术语审计78项零不一致；`git diff --check`及英文注释diff通过（有BOM、LF、19个活动翻译块、3组菜单） |
| `tl/zh_hans/src/plot/june.rpy` | June科技教室公共入口；关系前后问候差异与任务菜单 | June、Anon | 完成 | 完整通读10个活动翻译块和2组菜单映射，精修5处译文；依据`saga.cast.june < 'sex'`分支区分关系发生前的困惑戒备与关系推进后的轻快熟悉，并保留未选择任务时两阶段共用的尴尬告别；确认`Faptic engine.`延续“触觉引擎”术语、`Printer.`保持原菜单“打印机” | `validate_translations.py --changed`验证45个修改文件；重复术语审计78项零不一致；`git diff --check`及英文注释diff通过（有BOM、LF、10个活动翻译块、2组菜单） |
| `tl/zh_hans/src/plot/kassy.rpy` | Cupid商店公共入口；初见接待、再次问候与连衣裙任务菜单 | Kassy、Anon | 完成 | 完整通读11个活动翻译块和2组菜单映射，精修10处活动译文及1个菜单；结合原始路由确认Kassy只是友好专业的店员，区分初见“您”与熟悉后“你”的服务语气；商店专名`Cupid`现统一为“丘比特”，将名词菜单`Dress.`由“穿衣服”修正为“连衣裙”，保留`Just browsing.`为“随便看看” | `validate_translations.py --changed`验证45个修改文件；重复术语审计78项零不一致；`git diff --check`及英文注释diff通过（无BOM、CRLF、11个活动翻译块、2组菜单） |
| `tl/zh_hans/src/plot/kevin.rpy` | Kevin食堂公共入口；受罚帮工、健身阶段问候与杂志任务占用 | Kevin、Anon、Ursula（提及） | 完成 | 完整通读25个活动翻译块，精修23处译文；结合`ano01.rpy`与`bar03.rpy`确认Kevin因科学课成绩受罚、男性健身杂志和后期练臀语境，统一`cafeteria duty`为“食堂帮工”、`gym`为“健身房”，恢复`sucks dick`／`not the cool kind`的口交双关，并将三处内心独白改为全角括号；源文件4个菜单字符串由其他翻译单元提供既有映射 | `validate_translations.py --changed`验证45个修改文件；重复术语审计78项零不一致；`git diff --check`及英文注释diff通过（有BOM、LF、25个活动翻译块、0组本地菜单） |
| `tl/zh_hans/src/plot/key_school.rpy` | Ursula办公室物品互动；确认并擅自借走学校万能钥匙 | Anon、Annie（提及） | 完成 | 完整通读4个活动翻译块并全部精修；承接`ano01.rpy`中Annie透露的万能钥匙线索，理顺Anon从确认物品、判断不易被发现，到停顿后决定冒险的心理递进；统一`master key`为“万能钥匙”，将4处内心独白改为全角括号并恢复全角省略号 | `validate_translations.py --changed`验证45个修改文件；重复术语审计78项零不一致；`git diff --check`及英文注释diff通过（有BOM、CRLF、4个活动翻译块、无文件末尾换行） |
| `tl/zh_hans/src/plot/konty.rpy` | Tori办公室机器人随机入口；八组系统式闲聊、性暗示与人机笑点 | Konty、Anon、Tori（提及） | 完成 | 完整通读36个活动翻译块并精修33处译文；承接`tor01.rpy`首次启动与命名事件，区分八组随机闲聊，恢复底盘／工具和人机关系性暗示、拉丁流行乐标题与西语歌词、Tori需要做爱的直白诊断、灭绝人类假协议、机器人语倒序、`bot/hot`调情及灵魂提问；统一`Friend-Uhh`、`K-bot`、`-san`和机械笑声，并将5处ASCII省略号及1处内心反应改为中文格式 | `validate_translations.py --changed`验证45个修改文件；重复术语审计78项零不一致；`git diff --check`及英文注释diff通过（无BOM、CRLF、36个活动翻译块、0组菜单） |
| `tl/zh_hans/src/plot/library_lobby.rpy` | 图书馆入口时间限制；当天闭馆、当前闭馆与即将闭馆提示 | Anon | 完成 | 完整通读3个活动翻译块并全部精修；区分`closed for the day`、`try again later`与`wait around`的时间含义，将误译的“闲逛”恢复为在原地“干等”，统一图书馆“闭馆”用语，并将3处内心独白全部改为全角括号 | 英文原文注释diff通过（无BOM、CRLF、3个活动翻译块、0组菜单） |
| `tl/zh_hans/src/plot/library_shelf.rpy` | 图书馆办证入口；书架拦截、二十美元办证及接受／拒绝分支 | Jane、Anon | 完成 | 完整通读37个活动翻译块和3组菜单映射，精修26个翻译块及全部菜单；结合首次询问、拒绝后重问与两条付款路径，统一`library card`／`membership card`为“借书证”、`membership`为办证语境、`selections`为馆藏，并恢复Jane热情随和的馆员口吻与Anon无奈付款的玩笑 | 英文原文注释diff通过（无BOM、CRLF、37个活动翻译块、3组菜单；Git numstat为29/29） |
| `tl/zh_hans/src/plot/library_study.rpy` | 图书馆后方目击第三方做爱与摄像头录像；Jane处理并要求保密 | Jane、Anon、未具名男女 | 完成 | 完整通读22个活动翻译块并精修21处译文；明确恢复`having sex`与两处`doing it`的做爱语义、摄像头录像及当事人可能不知情的疑虑，理顺Jane对反复事件的烦躁、无奈和保密请求，并保留Anon最后想常来图书馆的色情笑点；统一“图书管理员／前台”，修复8处内心独白括号及多处ASCII省略号 | 英文原文注释diff通过（无BOM、CRLF、22个活动翻译块、0组菜单；Git numstat为21/21） |
| `tl/zh_hans/src/plot/lily.rpy` | Cosmic Cumics公共互动；主播身份、双关恭维与cosplay商品推荐 | Lily、Anon、Erik（被提及） | 完成 | 完整通读22个活动翻译块和4组菜单映射并精修全部译文；理顺Lily的GooTube主播身份、Erik粉丝关系及“巨大粉丝群”的胸部双关，恢复她以丰满身材和紧身服装进行轻度性暗示的友好推销口吻；保留Cosmic Cumics、GooTube、VirginLily69与Cyclone英文专名，并修复ASCII省略号和生硬商店话术 | 英文原文注释diff通过（有UTF-8 BOM、151个裸LF、0个CRLF、文件末尾LF、22个活动翻译块、4组菜单；Git numstat为26/26） |
| `tl/zh_hans/src/plot/liu.rpy` | Saga Financial大厅公共入口；初次接待、再次认出与账户查询指引 | Liu、Anon、Tina（菜单话题）、Frank（背景） | 完成 | 完整通读15个活动翻译块和2组菜单映射并精修全部译文；结合Liu的银行柜员身份，将初见接待改为正式“您”与办理话术，再次见面保留紧张停顿并自然转为“你”；把`access my account`落实为查询账户，理顺自动取款机在身后对面墙边的连续指引，并保留Saga Financial及所有姓名变量结构 | 英文原文注释diff通过（有UTF-8 BOM、101个裸LF、0个CRLF、文件末尾LF、15个活动翻译块、2组菜单；Git numstat为17/17） |
| `tl/zh_hans/src/plot/mall_booth.rpy` | 商场照相亭阶段提示；拍照需求与Roxxy回忆 | Anon、Roxxy（被想起） | 完成 | 完整通读4个活动翻译块并全部精修；区分Roxxy剧情`photo`状态前后的无需求提示与回忆触发，将4句内心独白统一为全角括号和中文省略号，并以“定格回忆”保留`capturing memories`的摄影／共同经历双关 | 英文原文注释diff通过（有UTF-8 BOM、24个CRLF、0个裸LF、无文件末尾换行、4个活动翻译块、0组菜单；Git numstat为4/4） |
| `tl/zh_hans/src/plot/mall_hall1.rpy` | 商场公共大厅；夜间打烊限制与时间推进／停留选择 | Anon | 完成 | 完整通读1个活动翻译块和2组菜单映射；把夜间独白改为自然的“商场已经打烊，我也该回家”，统一全角括号；明确区分推进时间并离场与继续留在商场两种机制选项，修复`Take it slow`被逐字译成“放慢脚步”的问题 | 英文原文注释diff通过（有UTF-8 BOM、17个CRLF、0个裸LF、文件末尾LF、1个活动翻译块、2组菜单；Git numstat为3/3） |
| `tl/zh_hans/src/plot/mel_office.rpy` | Melody后期办公室重复场景；直接性交、口交与私人舞蹈三分支 | Melody、Anon | 完成 | 完整通读97个活动翻译块和2组现有菜单映射，并结合`mel04.rpy`办公室聚会、`mel06.rpy`讲台口交及首次性交回溯人物关系；精修成熟主动的老师式命令与后戏口吻，明确插入、女性高潮、男性射精和内射诉求，贯通长笛／肉箫、私人演奏、激昂演讲、返场演出与压轴好戏双关；统一Melody的`sugar`“甜心”、`good boy`“真乖”、`Yes, ma’am!`“遵命，老师！”及菜单标点 | `validate_translations.py --changed`验证53个修改文件；重复术语审计81项零不一致；`git diff --check`及英文注释diff通过（无BOM、396个裸LF、0个CRLF、文件末尾LF、97个活动翻译块、2组菜单；Git numstat为73/73） |
| `tl/zh_hans/src/plot/melody.rpy` | Melody跨阶段公共入口；教师休息室提醒、音乐课补进度与办公室事件菜单 | Melody、Anon、Ursula（被提及） | 完成 | 完整通读23个活动翻译块和2组现有菜单映射，并结合`mel01.rpy`缺课补成绩、`mel04.rpy`办公室聚会及`mel06.rpy`后期关系确认入口所跨越的阶段；理顺教师休息室的友善提醒、音乐课补进度与办公室普通问候，恢复`groove`的音乐／学习状态双关，区分通用入口与后期`Fool around.`成人选项；统一`honey`为“亲爱的”、`Dress code.`为“着装规定”，未自行新增中文文件不存在的其他菜单映射 | 英文原文注释diff通过（有UTF-8 BOM、157个裸LF、0个CRLF、文件末尾LF、23个活动翻译块、2组菜单；Git numstat为18/18） |

| `tl/zh_hans/src/plot/mia.rpy` | Mia跨事件学校公共入口；科学教室问候、告别与美术事件菜单 | Mia、Anon、Barbara（相关支线） | 完成 | 完整通读9个活动翻译块和1组现有菜单映射，并结合Barbara美术比赛支线的拼贴、模特、比赛与肖像节点判断关系阶段；修复`How are you?`的健康担忧误读、课堂去向含混及生硬告别，保持Mia友善、拘谨的同学口吻；统一`Art partner.`为“美术搭档”，未自行新增中文文件不存在的其他菜单映射 | 英文原文注释diff通过（有UTF-8 BOM、61个裸LF、0个CRLF、文件末尾LF、9个活动翻译块、1组菜单映射） |

| `tl/zh_hans/src/plot/micoe.rpy` | Micoe医院公共入口；新生儿护理问询与礼貌告别 | Micoe、Anon、当前支线的新生儿（被询问） | 完成 | 完整通读4个活动翻译块和2组菜单映射，并结合`deb_baby.rpy`、`jen_baby.rpy`、`mar_baby.rpy`及`tin_baby.rpy`中Micoe的护理说明确认公共入口用途；修复犹豫语气、单复数代词和对单名工作人员误用“你们”，保持初次问询的专业礼貌；统一`How are they?`为兼容单胎／双胎的“孩子怎么样？” | 英文原文注释diff通过（有UTF-8 BOM、36个CRLF、0个裸LF、文件末尾LF、4个活动翻译块、2组菜单映射） |

| `tl/zh_hans/src/plot/misc_lotion.rpy` | Debbie线物品交互；抽屉中的润肤露香味回忆 | Anon、Debbie（关联人物） | 完成 | 完整通读2个活动翻译块，并结合`deb05.rpy`取润肤露和腿部按摩场景确认早期暧昧阶段；修复ASCII内心独白括号、连续省略号和过度意译，保留Anon对Debbie日常香味的私人迷恋；统一产品名为“巴西 Bum Bum”，同步修正`deb_mall.rpy`旧译并登记重复术语 | 英文原文注释diff通过（有UTF-8 BOM、12个CRLF、0个裸LF、无文件末尾换行、2个活动翻译块、0组菜单映射） |

| `tl/zh_hans/src/plot/misc_tissue.rpy` | Tori线物品交互；Ursula办公室垃圾桶与DNA纸巾样本 | Anon、Tori／Ursula／Annie（剧情关联） | 完成 | 完整通读2个活动翻译块，并结合`tor05.rpy`任务台词及`saga/logic/tor05.pyc`分支逻辑确认点击时序：任务前本能拒绝翻垃圾桶，取得Ursula用过的纸巾后明确不愿再翻；修复ASCII内心独白括号、机械直译和未落实动作对象的问题，以“翻”承接垃圾桶交互；补充Tori、Ursula、Annie的任务关系及`misc_tissue`术语 | 英文原文注释diff通过（有UTF-8 BOM、12个CRLF、0个裸LF、无文件末尾换行、2个活动翻译块、0组菜单映射） |

| `tl/zh_hans/src/plot/misc_toad.rpy` | Tori线血清材料物品交互；森林溪边首次发现发情蟾蜍 | Anon、Tori（任务关联） | 完成 | 完整通读1个活动翻译块，并结合`tor05.rpy`血清任务说明、溪边提示及抓取场景确认时点：此处只是首次观察目标外形，尚未抓取；保留`horny toad`与繁殖季相呼应的“发情”双关，统一为“发情蟾蜍”，不提前加入捕捉结果或关系推进 | 英文原文注释diff通过（有UTF-8 BOM、6个CRLF、0个裸LF、无文件末尾换行、1个活动翻译块、0组菜单映射） |

| `tl/zh_hans/src/plot/misc_towel.rpy` | Debbie家浴室通用物品交互；毛巾与星际搭车客文化彩蛋 | Anon、Debbie（地点关联） | 完成 | 完整通读2个活动翻译块并核对英文源场景、浴室物品位置和演出参数；确认这是不依赖关系进度的通用查看事件，第二句化用《银河系漫游指南》的毛巾经典说法；以“最最有用”保留`most massively useful`的夸张卖弄语气，修复两处ASCII内心独白括号 | 英文原文注释diff通过（有UTF-8 BOM、12个CRLF、0个裸LF、无文件末尾换行、2个活动翻译块、0组菜单映射） |
| `tl/zh_hans/src/plot/note_tori.rpy` | Tori线；学校课桌上再次查看办公室密码纸条的内心反应 | Anon、Tori、Ursula（任务关联） | 完成 | 完整通读3个活动翻译块，并结合`tor01.rpy`偷拿钥匙、寻找密码和进入Tori办公室的任务脉络确认分支；将`kleptomania`处理为夸张的“偷窃癖”，区分持有学校万能钥匙与未持有时的担忧，保留`[saga.cast.ursula]`和`{i}`标签 | 英文原文注释diff通过（有UTF-8 BOM、18个CRLF、0个裸LF、无文件末尾换行、3个活动翻译块、0组菜单映射） |
| `tl/zh_hans/src/plot/oli_stall.rpy` | Olivia线；公共场景首次邂逅与突然中断的成人互动 | Anon、Olivia、Olivia的男朋友（被提及） | 完成 | 完整通读73个活动翻译块并结合动作参数重建场景节奏；精修Anon的惊慌、Olivia的主动挑逗、胸部与生殖器触摸、亲吻及男朋友时间压力；统一成人语境下的“胸”“玩”“大男孩”，将内心独白改为全角括号并修复省略号，不净化成人内容或提前确立恋爱关系 | 英文原文注释diff通过（无UTF-8 BOM、291个裸LF、0个CRLF、文件末尾LF、73个活动翻译块、0组菜单映射） |
| `tl/zh_hans/src/plot/pizza_boxes.rpy` | Tony披萨店；外送结果、顾客反馈与工钱领取 | Anon、Tony、Maria、披萨顾客 | 完成 | 完整通读45个活动翻译块，理顺完美、部分成功和全部失败三类外送反馈及工钱结算；统一 Tony 对 Anon 的“小兄弟／小子／冠军”等称呼，并按 Maria 产后抱婴儿状态准确处理“腾不开手”和晚上结清工钱 | 本批 `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；无BOM、272个CRLF、文件末尾LF、45个活动翻译块 |
| `tl/zh_hans/src/plot/pizza_kitchen.rpy` | Tony披萨店；后厨受限入口 | Anon | 完成 | 完整通读2个活动翻译块，将“后厨危险”到“最好别随便闯进去”整理为自然递进；统一全角内心独白，并避免把 `wander in there` 误写成已经进入后厨闲逛 | 本批 `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、12个CRLF、无末尾换行、2个活动翻译块 |
| `tl/zh_hans/src/plot/pizza_main.rpy` | Tony披萨店；入口介绍与自定义店名笑点 | Anon、Tony（店名） | 完成 | 完整通读3个活动翻译块；以“首屈一指”保留故作正式的地点介绍，结合改名条件补足英文缺失的疑似 `sound` 谓语，将 `authentic` 明确为店名“听起来没那么正宗”，并收紧“还真讽刺”的笑点 | 本批 `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；无BOM、20个CRLF、文件末尾LF、3个活动翻译块 |
| `tl/zh_hans/src/plot/pizza_shop.rpy` | Tony披萨店；夜间、医院、临近打烊与星期日关闭提示 | Anon、Tony（被提及） | 完成 | 完整通读8个活动翻译块；理顺“不全天候营业”的学生噩梦式夸张、`clinic_baby` 医院承接、临近打烊限制及星期日“老掉牙的地方法规”荒诞笑话，统一内心独白与中文标点 | 本批 `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、48个CRLF、无末尾换行、8个活动翻译块 |
| `tl/zh_hans/src/plot/roxxy.rpy` | Roxxy线公共入口；法语教室跨阶段问候、事件菜单与后期亲密关系 | Roxxy、Anon、Dexter、Becca、Missy | 完成 | 完整通读45个活动翻译块和2组菜单映射；按敌对、顾及公众形象、关系缓和、担心Dexter冲突、后期主动亲密五阶段校准口吻；统一后期 `my man` 为“我男人”、`Pom-poms.` 为“啦啦球”，并保留 Roxxy 强势、自信、活泼的性格 | 本批 `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、275个裸LF、文件末尾LF、45个活动翻译块、2组菜单映射 |

| `tl/zh_hans/src/plot/sam_stall.rpy` | 商场更衣隔间；误入、内裤砸脸与物品栏自嘲 | Sammy、Anon | 完成 | 完整通读27个活动翻译块并精修25处；按“意外闯入—结巴解释—继续偷看—被内裤砸脸—夺回内裤”理顺连续动作，明确 Sammy 的愤怒拒斥与陌生人边界；统一 `{i}*Hurk*{/i}` 为“呃唔”、`MILF` 为“性感熟女”，修复两次 `It burns` 递进、全角内心独白和物品栏笑点 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；无BOM、47个裸LF、文件末尾LF、27个活动翻译块 |

| `tl/zh_hans/src/plot/school_boiler.rpy` | 学校公共区域；上锁的杂物间提示 | Anon | 完成 | 完整通读1个活动翻译块；结合 `mel05.rpy` 的同设施用法，将 `utility closet` 从错误的“杂货间”统一为“杂物间”，保留简短内心独白并明确文件标签 `boiler` 不等于玩家可见的锅炉房 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、6个CRLF、无末尾换行、1个活动翻译块 |
| `tl/zh_hans/src/plot/school_girls.rpy` | 学校公共区域；关闭维修的女生更衣室与地板破洞 | Anon；Judith（前情提及） | 完成 | 完整通读3个活动翻译块；承接 `ano01.rpy` 的水管爆裂前情，将室内 `ground` 明确为“地板”，并把 `this locker room` 按当前地点译为“女生更衣室”；统一全角内心独白与中文省略号 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、18个CRLF、无末尾换行、3个活动翻译块 |
| `tl/zh_hans/src/plot/school_hall1.rpy` | 学校公共入口；夜间锁门、周末关闭与结束当日校园活动 | Anon；Annie（被提及） | 完成 | 完整通读4个活动翻译块和2组菜单映射；承接 Annie 提供万能钥匙线索及 Anon 擅自“借用”钥匙的剧情，修复“主钥匙”和错乱语序，区分非开放时段提示与离校确认菜单，并统一全角内心独白 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、36个CRLF、文件末尾LF、4个活动翻译块、2组菜单映射 |
| `tl/zh_hans/src/plot/school_locker.rpy` | 学校走廊储物柜；万能钥匙提示与避开柜主 | Anon；Annie（被提及） | 完成 | 完整通读4个活动翻译块；承接万能钥匙道具线，明确 `locker` 为“储物柜”，并将有人在场分支理顺为等待柜主走远后再偷翻，保留 Anon 对不光彩行为的自嘲口吻与全角内心独白 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、24个CRLF、无末尾换行、4个活动翻译块 |
| `tl/zh_hans/src/plot/school_office1.rpy` | 校长办公室；Ursula 在场时识破借口并驱赶 Anon | Ursula、Anon | 完成 | 完整通读17个活动翻译块和2条随机分支；按“找洗手间”与尴尬寒暄两套借口校准 Anon 的慌乱，强化 Ursula 简短、权威、不耐烦的训斥口吻，区分 `[saga.cast.ursula.clan]夫人` 与学生服从语境中的“校长”，并统一中文省略号与全角内心独白 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、102个CRLF、无末尾换行、17个活动翻译块、2条随机分支 |
| `tl/zh_hans/src/plot/school_office2.rpy` | Tori 办公室门外；电子密码锁与门禁密码提示 | Anon；Tori（被提及） | 完成 | 完整通读3个活动翻译块并核对 `tor01.rpy` 潜入任务前情；将生硬的“自动密码锁”校准为“电子密码锁”，明确 `key code` 是门禁密码，并统一三句全角内心独白与中文省略号 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、18个CRLF、无末尾换行、3个活动翻译块 |
| `tl/zh_hans/src/plot/school_pa.rpy` | 学校公共区域；23组随机校内广播 | 广播员、Anon；Ursula、Bridget、Dexter、Melody、Tori、Barb、Viv（被提及） | 完成 | 完整通读23组广播、102个活动翻译块并逐条重译；统一正式播报腔，修复“夏日大学”、车型音译、辣椒菜品、主办公室、田径队名额、公开亲热、性教育DVD及护裆等误译，保留食物中毒、0胜12负、打印机、失窃内裤、啦啦队与天台日漫宅等反差笑点 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；无BOM、614个CRLF、文件末尾LF、102个活动翻译块、23组随机广播 |
| `tl/zh_hans/src/plot/specs_judith.rpy` | Judith 眼镜任务；储物柜中的备用眼镜锁定提示 | Anon；Judith、Tori（任务关联） | 完成 | 完整通读2个活动翻译块，并结合 `tor02.rpy` 中 Tori 寻找渐进镜片、Judith 以假装情侣拍照交换备用眼镜的完整任务脉络；将生硬的“某种怪物”改为带道德自责的内心反问，明确 Anon 在获得同意前拒绝偷走 Judith 的私人眼镜，不提前写成已取物或关系推进；统一全角内心独白与“眼镜”术语 | `validate_translations.py --changed`、重复术语审计、`git diff --check` 及英文注释diff通过；有BOM、12个CRLF、无末尾换行、2个活动翻译块 |

| `tl/zh_hans/src/plot/tammy_lobby.rpy` | Tammy／Erik 家门厅；夜间与临睡前离开提示 | Anon、Tammy／Erik（被提及） | 完成 | 通读并精修 4 个翻译块；将 `making a move` 按场景还原为动身离开，统一全角内心独白与中文省略号 | 最终校验见本批测试记录 |
| `tl/zh_hans/src/plot/tammy_yard_scope.rpy` | Tammy 家后院；望远镜瑜伽观察 | Anon、Tammy（变量） | 完成 | 通读并精修 10 个翻译块；区分空后院、柔韧度、保持身材和特定姿势性吸引，明确 `turned on` 的成人含义并保持偷窥关系边界 | 最终校验见本批测试记录 |
| `tl/zh_hans/src/plot/ten_stall.rpy` | 商场更衣隔间；Tenzin 看书与格言式赶人 | Anon、Tenzin | 完成 | 通读并精修 31 个翻译块；复原 Tenzin 故作高深的格言口吻、更衣隔间用途争执和 `Shoo` 赶人笑点，修复全角内心独白及中文省略号 | 最终校验见本批测试记录 |
| `tl/zh_hans/src/plot/titomi.rpy` | Ara Ara 公共互动；亚裔刻板印象玩笑、菜单抬杠与 Omaha 误会 | Anon、Titomi、Hana（被提及） | 完成 | 完整通读 59 个活动翻译块和 2 个菜单映射；修复 `Excuse me`、`Oh-maha`、`hospitality stick`、`wear a helmet`、`charmed` 等语义，恢复 Ara Ara 英文专名并保持 Titomi 的反讽刻薄口吻 | 最终校验见本批测试记录 |

| `tl/zh_hans/src/plot/ton_baby.rpy` | Tony／Maria生育后续；怀孕反应、待产准备、生产后返店、抱婴儿黑帮故事与后厨三人关系 | Tony、Maria、Anon、婴儿；Luigi（往事提及） | 完成 | 完整通读151个活动翻译块和1组菜单映射；按怀孕早期、临产前、生产后返店、抱婴儿值店和更晚恢复五阶段校准口吻；修复五组动作片／黑帮引用、Luigi姓名、`champ`“冠军”、`capisce`、有声书反转、外送订单及后厨成人暗示，并用不显数量的“小家伙”规避源代码单复数分支疑似颠倒 | 英文原文注释diff通过；无BOM、883个裸LF、文件末尾LF、151个活动翻译块、1组菜单映射 |
| `tl/zh_hans/src/plot/tony.rpy` | Tony／Maria公共入口；客厅看球、后厨日常、披萨店阶段问候与剧情菜单 | Tony、Maria、Anon | 完成 | 完整通读58个活动翻译块和4组菜单映射；精修37个活动翻译块和2组菜单映射；按初次来店、牛奶任务、Tony解围、试送入职及后期家人式信任校准店主／长辈／老板口吻；修复两处旧块中英错位，统一`champ`“冠军”、外送订单、试送、车子及“她可真是个宝” | 英文原文注释diff通过；无BOM、400个裸LF、0个CRLF、文件末尾LF、58个活动翻译块、4组菜单映射 |
| `tl/zh_hans/src/plot/tool_drill.rpy` | Debbie家车库物品；父亲旧电钻与后续制作任务道具 | Anon；已故父亲（提及） | 完成 | 完整通读2个活动翻译块，并对照`bar04.rpy`画架制作与`mel01.rpy`木笛制作的相关剧情；精修2个活动翻译块，统一全角内心括号、父亲遗物语气和“旧电钻”物品名 | 英文原文注释diff通过；无BOM、14个CRLF、0个裸LF、文件末尾LF、2个活动翻译块、0组菜单映射 |
| `tl/zh_hans/src/plot/tool_shovel.rpy` | Debbie家车库物品；Diane菜园铲子任务与Jenny电池插曲 | Anon、Jenny；Diane、Debbie（提及） | 完成 | 完整通读43个活动翻译块，并对照`dia01.rpy`中Diane旧铲子断裂及暑期菜园工作的任务起点；精修35个活动翻译块，区分尚未见Diane的游戏式取物分支与已接受工作的任务分支，保持Jenny前期敌对辱称、未知电池用途、全角内心括号和中文省略号 | 英文原文注释diff通过；有BOM、258个CRLF、0个裸LF、无文件末尾换行、43个活动翻译块、0组菜单映射 |
| `tl/zh_hans/src/plot/tv.rpy` | 电视短节目；Ronald竞选、被捕与监狱新闻链，Yoo牢房结局及普通频道切换 | Anon；Ronald、Yoo（电视画面） | 完成 | 完整通读14个活动翻译块，并结合8张电视节目画面复核新闻和视觉笑点；精修14个活动翻译块，修复`perp walk`误译、监狱发布会连续反问、Yoo去向、市长徒弟调侃、自然频道和女子沙滩排球观看兴趣，统一全角内心括号与中文省略号 | 英文原文注释diff通过；无BOM、86个CRLF、0个裸LF、文件末尾LF、14个活动翻译块、0组菜单映射 |
| `tl/zh_hans/src/plot/tym_stall.rpy` | 商场更衣隔间；Tyme 偷偷涂写、被撞见后的掩饰与逃离 | Anon、Tyme | 完成 | 完整通读7个活动翻译块，并结合商场更衣隔间文件簇及Tyme的记号笔动作资源确认涂鸦场景；精修7个活动翻译块，补足被打断的道歉、还原陌生同龄人的“哥们儿”口吻与结巴告别，统一中文省略号、全角内心括号和Anon不以为意的收尾 | 英文原文注释diff通过；无BOM、28个裸LF、0个CRLF、文件末尾LF、7个活动翻译块、0组菜单映射；Git numstat为7/7 |
| `tl/zh_hans/src/plot/ursula.rpy` | 学校教师休息室；违规闯入、当场喝止与开除威胁 | Ursula、Anon | 完成 | 完整通读8个活动翻译块，并对照`school_office1.rpy`的校长办公室拒绝事件与Ursula角色档案；精修6个活动翻译块，恢复Ursula短促强硬的校长训斥、Anon被打断后的结巴服从，统一`teachers' lounge`“教师休息室”、`ma'am`“校长”、全角内心括号、中文省略号和问号 | `validate_translations.py --changed`验证96个修改文件；重复术语审计零不一致；`git diff --check`及英文注释diff通过；有BOM、48个CRLF、0个裸LF、无文件末尾换行、8个活动翻译块、0组菜单；Git numstat为6/6 |
| `tl/zh_hans/src/plot/vee.rpy` | Consum-R 货架通道；店员接待、销售范围追问与蔬菜高汤任务入口 | Vee、Anon | 完成 | 完整通读25个活动翻译块和2组已有菜单映射，并对照`tor05.rpy`的蔬菜高汤采购场景；精修14个活动翻译块和1组菜单映射，恢复欢迎口号中的`aisle`语义、Vee随和店员口吻与逐类追问笑点，统一`vegetable stock`“蔬菜高汤”、BMX车型名及Consum-R中文店名“购乐百货” | `validate_translations.py --changed`验证97个修改文件；重复术语审计零不一致；`git diff --check`及英文注释diff通过；有BOM、0个CRLF、160个裸LF、无文件末尾换行、25个活动翻译块、2组菜单映射；Git numstat为15/15 |
| `tl/zh_hans/src/plot/viv.rpy` | Viv法语教室／办公室公共入口；课后辅导事件菜单与关系解锁后的“补课”双关 | Viv、Anon；Roxxy（菜单变量） | 完成 | 完整通读23个活动翻译块和4组已有菜单映射，并对照`ano01.rpy`、`viv01-05.rpy`与`viv_office.rpy`确认关系阶段；精修14个活动翻译块和2组菜单映射，恢复缺课进度语义、教师询问与告别的自然回应，并在性关系解锁后补出`more {i}tutoring{/i}`的“又来补课”双关；未为4个缺失菜单擅自新增映射 | `validate_translations.py --changed`验证98个修改文件；重复术语审计零不一致；`git diff --check`及英文注释diff通过；有BOM、0个CRLF、157个裸LF、文件末尾LF、23个活动翻译块、4组菜单映射；Git numstat为16/16 |
| `tl/zh_hans/src/plot/viv_office.rpy` | Viv线后期；法语教室“补课”预约、办公室重复性爱与复用入口 | Viv、Anon | 完成 | 完整通读14个活动翻译块并对照`viv05.rpy`首次性爱奖励及`viv.rpy`后期办公室问候；精修10个活动翻译块，明确“补课”性爱双关、双方熟稔预约和Viv主动欲望，将`Ravage me!`准确译为“狠狠地肏我吧”，并统一`mon bel homme`“我的帅哥” | `validate_translations.py --changed`验证99个修改文件；重复术语审计及`viv_mon_bel_homme`专项审计零不一致；`git diff --check`及英文注释diff通过；有BOM、84个CRLF、0个裸LF、无文件末尾换行、14个活动翻译块、0组菜单映射；Git numstat为10/10 |
| `tl/zh_hans/src/plot/viv01.rpy` | Viv线开端；一对一辅导报名、缺页法英词典、Judith借书、June复印机与首次课后辅导 | Viv、Anon、Judith、Jane、June | 完成 | 完整通读219个活动翻译块和3组已有字符串映射，结合动作演出与STR分支精修约134行；恢复“特殊奖励”的早期暧昧、词典缺页任务逻辑、`PC LOAD LETTER`复印机笑点、法语发音互动和Judith羞怯好感；统一`mon bel homme`为“我的帅哥”，未倒灌后期性关系 | `validate_translations.py --changed`验证100个修改文件；重复术语审计零不一致；`git diff --check`及英文注释diff通过；无BOM、1322行、CRLF、文件末尾LF、219个活动翻译块、3组字符串映射；Git numstat为134/134 |

| `tl/zh_hans/src/plot/viv02.rpy` | Viv线第二阶段；逾期图书任务、奶酪作文、首次摸胸奖励与 Ursula 办公室训斥 | Viv、Anon、Jane、Camila、Val、Dexter、Erik、Ursula、Annie | 完成 | 完整通读275个活动翻译块和3组字符串映射；修复“借书”误成“出书”、三本逾期书任务逻辑、Chola与Oedipuss双关、Quick mafs笑点、`fromage`法语用词及 Ursula/Viv 权力关系；统一“我的帅哥”“我的小兔子”“白人小子”“特殊奖励”，明确关系仅推进到摸胸 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`及英文注释diff通过；无BOM、1663个CRLF、文件末尾LF、275个活动翻译块、3组字符串映射 |
| `tl/zh_hans/src/plot/viv03.rpy` | Viv线第三阶段；浪漫诗任务、Roxxy课堂朗诵、法式接吻奖励与 Ursula 打屁股惩罚 | Viv、Anon、Mia、Judith、Jane、Roxxy、Ursula、Annie | 完成 | 完整通读354个解析块并逐句对照复读；修复露骨爱情书与自慰暗示、Roxxy发音羞辱及暴怒、Debbie关系决定的接吻经验分支、Ursula工作会议与权力惩罚；统一“我的帅哥”“特殊奖励”“法式接吻”及中文省略号，明确关系只推进到接吻 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`及英文注释diff通过；无BOM、2137个CRLF、文件末尾LF、354个解析块 |
| `tl/zh_hans/src/plot/viv04.rpy` | Viv线第四阶段；考试危机、Roxxy啦啦球任务、Jenny编排动作与两人初次会面 | Viv、Anon、Roxxy、Jenny、Bridget、Debbie | 完成 | 完整通读625个活动翻译块和2组主要菜单映射并逐句对照复读；修复Viv面临解雇的考试危机、Roxxy非女友与女友／性关系分支、Bridget办公室换衣和自夸、Jenny收取500美元编排州冠军赛动作及两人比较胸部的互动；统一“我的帅哥”“特殊奖励”“啦啦球”“啦啦队长”，明确本阶段奖励尚未兑现 | `validate_translations.py --changed`、`audit_recurring_terms.py --changed --fail-on-mismatch`、`git diff --check`及英文注释diff通过；无BOM、3770个CRLF、文件末尾LF、625个活动翻译块、2组主要菜单映射 |
| `tl/zh_hans/src/plot/viv05.rpy` | Viv线终章；正式法语考试、法国葡萄酒、特殊奖励兑现与办公室首次性交 | Viv、Anon、Roxxy、Ursula | 完成 | 完整通读143个活动英文—中文对应和2组菜单映射；区分考试失败／成功、首次性交／既有关系以及书桌／椅子分支，修复醉酒打嗝、身体指代、女性高潮和内心独白格式；统一“我的帅哥”“特殊奖励”“法国人是怎么做爱的”，确认本文件结束后关系达到`sex`阶段 | `validate_translations.py --changed`通过104个修改文件；`audit_recurring_terms.py --changed --fail-on-mismatch`零不一致；`git diff --check`及英文注释diff通过；无BOM、870个CRLF、0个裸LF、文件末尾LF、144个translate块、2组菜单映射、0个替换字符 |
| `tl/zh_hans/src/plot/ang.rpy` | 教堂公共入口；Angela迎接、告解暗示、离开分支与亚麻布任务菜单 | Angela、Anon | 完成 | 完整通读6个活动翻译块和2组菜单映射；将宗教欢迎语、`unburden yourself`告解暗示及Anon局促复述译得连贯，统一中文省略号和双引号，并确认`Linens.`承接`bar05.rpy`白色旧洗礼袍任务 | `validate_translations.py --changed`通过105个修改文件；重复术语审计中`church_art_linens`零不一致；`git diff --check`及英文注释diff通过；有BOM、48个CRLF、无文件末尾换行、7个translate块、2组菜单映射、0个替换字符 |
| `tl/zh_hans/src/plot/annie.rpy` | Annie公共入口；走廊巡查、音乐教室专注与美术模特事件菜单 | Annie、Anon | 完成 | 完整通读12个活动翻译块和2组菜单映射；强化Annie短促、纪律化且易怒的口吻，修复`concentrate`误译、连续打断、省略号和菜单动作语义；确认公共入口没有暧昧或关系推进 | `validate_translations.py --changed`通过106个修改文件；重复术语审计零不一致；`git diff --check`及英文注释diff通过；有BOM、87个裸LF、无文件末尾换行、14个translate块、2组菜单映射、0个替换字符 |
| `tl/zh_hans/src/plot/ari_stall.rpy` | 泳池更衣隔间初遇；误闯、裸胸、Ariane发怒与Anon失败搭讪 | Ariane、Anon | 完成 | 完整通读31个活动翻译块；明确Anon误闯隐私空间、Ariane拒绝免费展示身体及付费追问未构成交易，修复成人指代、连续怒骂、内心独白全角括号、中文省略号，并保留`Batman`、`Sherlock`英文专名 | `validate_translations.py --changed`通过47个修改文件；重复术语审计零不一致；`git diff --check`及英文注释diff通过；无BOM、123个裸LF、文件末尾LF、31个translate块、0组菜单映射、0个替换字符 |

## 已完成的规则修复（剧情未全面精修）

| 文件 | 修复内容 | 后续要求 |
|---|---|---|
| `tl/zh_hans/base_box/sets.rpy` | “托尼披萨店”恢复为 `Tony披萨店` | 后续结合资源调用统一地点名称 |
| `tl/zh_hans/bytecode_strings.rpy` | 四处手机任务提示将字面 `Anon` 按玩家视角改为“你”；玩家可见标签统一为 `{dom=强势}`、`{sub=顺从}`；恢复 `Sluttygram` 英文专名，并补译 Debbie 的洗衣篮手机留言；其他姓名/变量保持原状 | 后续完整复核资源字符串 |
| `tl/zh_hans/res/meta/prop.rpy` | “凯文”恢复为 `Kevin`；按界面文本使用中文双引号：“光膀子的壮汉！” | 后续完整复核资源字符串 |
| `tl/zh_hans/res/meta/step.rpy` | “朱迪丝”恢复为 `Judith` | 后续完整复核资源字符串 |
| `tl/zh_hans/src/game.rpy` | `anon`、`Anon` 保持英文原拼写和大小写 | 后续完整复核全局字符串 |
| `tl/zh_hans/src/plot/ano01.rpy` | 将 12 处英文纯省略号误写的 `??` 全部恢复为中文省略号 `……` | 已随完整文件精修复核 |
| `tl/zh_hans/src/plot/tor05.rpy` | 定向统一7处血清材料`horny toad`／`horny toad extract`为“发情蟾蜍”／“发情蟾蜍提取物”，补修`boys' locker room`为“男生更衣室”、`Consum-R`英文店名及相关中文省略号 | 后续仍须按文件名顺序完整通读全文件，本次仅完成与`misc_toad.rpy`直接相关的连续性修复 |

## 全仓校验待修复队列

运行 `python tools/validate_translations.py --no-compare` 后，当前报告 **26 个既有问题**。这些问题先登记，按完整场景阅读结果逐项修复；明显程序格式错误可作为独立安全批次处理，但不得据此将剧情文件标记为完成。

### 变量、标签或占位符不一致

- `tl/zh_hans/res/meta/cast.rpy:97`：`[saga.cast.frank]` 数量多 1。
- `tl/zh_hans/src/plot/ano13.rpy:2577`：译文新增 `[saga.cast.becca]`。
- `tl/zh_hans/src/plot/cedric.rpy:50,57,190`：`[saga.cast.anon]` 或 `[saga.cast.cedric]` 增删不一致。
- `tl/zh_hans/src/plot/deb26.rpy:4201`：译文新增 `[saga.cast.debbie]`。
- `tl/zh_hans/src/plot/deb26.rpy:5198`：`{nw=.3}` 被改成 `{nw=2}`。
- `tl/zh_hans/src/plot/jen11.rpy:104`：译文新增 `[saga.cast.jenny]`。
- `tl/zh_hans/src/plot/jen14.rpy:904`：译文新增斜体标签。
- `tl/zh_hans/src/plot/jen17.rpy:97,1428`：译文新增 `[saga.cast.erik]`。
- `tl/zh_hans/src/plot/maria.rpy:151`：译文新增 `[saga.cast.anon]`。
- `tl/zh_hans/src/plot/mel03.rpy:374,678,902`：`Eve`/`Melody` 变量增删不一致。
- `tl/zh_hans/src/plot/tin02.rpy:930`：漏掉 `[saga.cast.tina]`。
- `tl/zh_hans/src/plot/tin_dusk.rpy:943`：译文新增 `[saga.cast.becca]`。
- `tl/zh_hans/src/plot/tony.rpy:22`：漏掉 `[saga.cast.tony]`。

### 错误插值或空译文

- `tl/zh_hans/src/plot/jen15.rpy:295,301,307`：普通内心独白被写成 `['中文']`，会被 Ren’Py 当作插值。
- `tl/zh_hans/src/plot/mel02.rpy:1856,1863,1870`：普通文本被写成 `['中文']`，会被 Ren’Py 当作插值。
- `tl/zh_hans/src/plot/deb26.rpy:5488`：非空英文对应空译文。
- `tl/zh_hans/src/plot/jen17.rpy:319`：非空英文对应空译文。

## 上下文与术语更新

- 已建立 `characters.md`、`terminology.md`、`storylines.md`、`style_guide.md`、`file_inventory.md`、`recurring_terms.md` 和机器可读的 `recurring_terms.json`。
- 固定强制规则：角色姓名、昵称、姓氏和特殊拼写按英文原文保留，不建立中文音译姓名；手机任务提示中用作玩家占位的字面 `Anon` 可按 UI 视角译为“你”。
- 已确认 `{dom=...}`、`{sub=...}` 的标签名必须保留，等号后的玩家可见文字必须汉化，统一为“强势/顺从”。
- 已补充 Dimitri 的危险、戏谑、非母语化语气档案，以及 `ano03.rpy` 的威胁和警务上下文。
- 已补充 Tammy 在离婚后通过照顾 Erik 获得被需要感的背景，并确认 `ano04.rpy` 中 Debbie 与 Anon 仍处于早期家庭适应阶段。
- 已补充 `ano05.rpy` 的驾车监视、警方留守、Anon 保护欲和 Debbie 责任边界；固定 `That's my boy!` 在本场译为“这才对嘛”，不得误建母子关系。
- 已补充 Igor 与 Tony 的角色档案，以及 `ano06.rpy` 的街头围堵、工作邀请、二十五万美元贷款和房屋抵押危机；固定 `Russkies`／`Russians`、`collateral`、`take his medicine` 等语境处理。
- 已补充 Maria 的经营核心、强势务实和粗俗比喻档案，并补全 Tony 在 `ano07.rpy` 中作为照顾型雇主的语气；固定“到店自取订单”“试送”“后厨”“贴身衣物”等场景术语。
- 已记录 `ano08.rpy` 的第四面墙式元叙事占位；`face time` 按当面相处处理，不使用“刷存在感”等偏离原意的网络化表达。
- 已补充 `ano09.rpy` 的 Tina 初见、Luigi 遗属承诺、车辆购买/置换分支和 Tony/Maria 意大利裔美国人口吻；固定 `champ`／`babyface`／`dollface` 及三组车辆名称。
- 已补充 `ano10.rpy` 的披萨教学、cannoli 奖励误导、Tony/Luigi 黑帮兄弟关系和不育诊断；固定 `protégé`→“徒弟”、`cannoli`→“意式奶油甜馅卷”、`mustache ride`→“骑胡子”及披萨制作术语。
- 已补充 `ano11.rpy` 的领养/精子捐赠分歧、俄式食品笑话、持枪闯店与 Raz 调查承接；固定 `little bunny`→“小兔子”，并确认 `The Plumber`、`Eddie Four-Fingers`／`Four-Fingers` 保持英文。
- 已记录 `ano12.rpy` 与 `ano08.rpy` 平行的元叙事占位；`moderate affection points` 与 `ano14.rpy` 统一为“好感度中幅提升”。
- 已补充 `ano13.rpy` 的特殊披萨送餐、Tina 成人关系推进、Becca 母女冲突、Eddie 服刑与探监调查、领养失败及捐精方案承接；固定 `prosciutto`→“意式风干火腿”、`gorgonzola`→“戈贡佐拉奶酪”、`calzone`→“意式烤饺”、`Beachside Apartments`→“海滨公寓”。
- 已补充 `ano14.rpy` 的探监离城、多日店务条件分支和第三次强制引导元叙事；固定“海滨公寓302室”，并保持动作RPG、更新版本和玩家选择座驾等第四面墙笑点。
- 已补充 `ano15.rpy` 的俄国人走私窝点情报、自然受孕条件、Maria 的婚姻忠诚冲突及 Tony/Maria/Anon 成人关系分支；固定“补水最重要”“卡皮科拉火腿”“锉刀”“骑胡子”和“意式烤饺”。`ano16.rpy` 进一步确认 Maria 怀孕、Anon 的教父身份和三人家人关系，并保留版本结尾元叙事。
- 审查反馈复核：`ano14.rpy` 的内部引述改用弯引号“……”；已处理的修改文件同步清除活动译文中的 `「……」`。`ano15.rpy` 的 `workplace seminar` 结合员工/老板场景确定为“职场性骚扰培训”，不是 Tony/Maria 的性交暗语。
- 已建立“短距离重复 2 次即触发”的跨文件复查机制；当前登记 93 组称呼、口癖、关系身份、连续笑点、专名、食品术语、地点、亲属称谓和成人双关，并记录未处理文件中的既有不一致队列。
- 已固定首批系统术语：存档、读档、设置、物品栏、任务、城镇地图、时间段。
- 地点暂定统一为“夏日镇”；`Tony's Pizza` 按语境使用“Tony披萨店”。
- 已补充 Anon 卧室设备交互：椅子脚轮检查、电脑零件/修复/画质升级及手机 Wi-Fi 连点彩蛋；固定 `Consum-R` 统一译“购乐百货”、`cheat menu`→“作弊菜单”、游戏故障 `bugs`→“BUG”，并把手机八条提示作为连续递进场景处理。
- 已补充公寓、银行与车行的地点进入限制：统一使用简短内心独白表达深夜/未受邀访问、员工区、营业时间、禁止逗留和闭店逻辑，并修复代词、ASCII 省略号及活动译文直角引号。
- 已补充 Erik 卧室物品检查：床底灰尘与书、凌乱抽屉及旧游戏手柄回忆；保持 Anon/Erik 童年好友语气，不擅自解释抽屉污渍来源。
- 已补充 Debbie 家中短交互：阁楼旧物、卧室进入限制、绘画爱好、内裤抽屉隐私、浴室门缝与 Debbie/Diane 夏令营旧照片；修复女性复数代词，并补建 Diane 的英文姓名档案。
- 已补充 `jen_baby.rpy` 的首次／再次怀孕、孕期身体变化、成人直播、单胎／双胎生产和共同育儿阶段；明确 Debbie 是“外婆”，Jenny 的男朋友口误不构成正式关系确认，产后称 Anon 为 Daddy 则确认真实父亲身份与共同育儿。

- 已补充 `jen_deal.rpy` 的公共区域议价入口：Anon 主动提出交易，Jenny 为避开 Debbie 将讨论转移到下午并要求带钱，确认付费安排、家庭保密和非正式情侣边界继续存在。

- 已补充 `jen_finger.rpy` 的私人前戏、指交高潮和中途停止分支；明确 Jenny 会因私人快感取消成人直播，Anon 也开始反过来掌握节奏并用她过去的吊胃口手段戏弄她，但这一控制权反转不等于正式恋爱确认。

- 已补充 `jen_pool.rpy` 的泳池性交、溺水走马灯、体外／内射结果、裸泳反悔、炸弹入水报复和公主支配角色；明确危险场所与互相戏弄体现稳定性关系和控制权拉扯，不等于正式恋爱确认。

- 已补充 `jen_shower.rpy` 的前期偷窥边界、成人直播合作后的共同淋浴、狗狗与乞求支配玩法、淋浴性交、深喉吞精及怀孕身体不安分支；明确 Anon 会拒绝羞辱，Jenny 的私人吞精偏好承认也不等于正式恋爱确认。

- 已补充 `jen_sleep.rpy` 的关系阶段分支、做爱与搂着睡的边界、前戏后拒绝做爱的反制、外射后留宿、内射许可冲突和次晨斗嘴；明确同床过夜是非性亲密边界推进，仍不等于正式情侣确认。

- 已补充 `jen_table.rpy` 的餐桌冒险性交、早餐倒计时、炒蛋双关、咖啡杯体外射精和内射许可冲突；明确 Jenny 主动追求被 Debbie 撞见的风险刺激，但仍需家庭保密，也不构成正式情侣确认。
- 已补充 `jen_tv.rpy` 的色情片账号、拒绝／乞求分支、公主式自我羞辱、足交、客厅风险性交及体外／内射结果；明确高潮时夹住导致无法退出不等于事先许可内射，并登记 `Pink Channel` 与 `Princess [saga.cast.jenny]` 固定处理。
- 已补充 `jen_visit.rpy` 的深夜主动索取、接受／拒绝分支与控制欲反弹；明确身体反应不等于同意，Anon 当次明确说不仍必须被保留，Jenny 的报复不是默认调情。
- 已补充 `jenny_laptop.rpy` 的笔记本密码调查、家庭照片、Pink Channel 账号和三段早期个人成人直播；明确 Jenny 在 Anon 加入合作前已熟练运用订阅墙、打赏、玩具升级、肛塞和“性爱女神”角色刺激付费，并为后续真人性交直播埋下伏笔。
- 已补充 `jenny.rpy` 的卧室、餐厅和后院多阶段公共入口；明确前期敌意、成人直播合作、收入依赖、评论区讨论与后期风险调戏必须按剧情阶段区分，并统一 `camgirl` 为“成人女主播”及 Jenny 对 Anon 的 `loser` 为“废柴”。
- 已补充 `jos01.rpy` 的车行初见、父女工作冲突、手机交易、两个办公室潜入分支与求开除之吻；明确 Josie 初见时主要利用 Anon，但已经出现身体兴趣，不能提前写成正式情侣，并统一 TPS报告、T字带凉鞋、锅盖头与相关英文姓名。
- 已补充 `jos_trade.rpy` 的旧车折价、三类车型与重复报价接口；明确文件横跨早期挖苦和后期性调侃等多个关系节点，并统一迷你外阴、SL-700 胯下火箭、过度补偿者、踏板车和旧车折价。
- 已补充 `mel_office.rpy` 的后期办公室成人关系、直接性交／口交／私人舞蹈三分支及 `mel06.rpy` 讲台口交回扣；统一 Melody 的 `sugar`“甜心”、肉箫、私人演奏、激昂演讲、返场演出、压轴好戏和老师式服从称呼。
- 已补充 `melody.rpy` 的教师休息室、音乐教室和办公室跨阶段公共入口；明确普通师生问候与后期成人菜单并存，统一课堂 `groove` 的“玩音乐／找回节奏”处理及 `honey`“亲爱的”。
- 已补充 `mia.rpy` 的科学教室公共入口与 Barbara 美术比赛事件菜单；明确 Mia 当前仍是友好、略拘谨的同学／美术搭档，统一 `Art partner.`“美术搭档”。
- 已补充 `micoe.rpy` 的新生儿护理公共入口；明确 Micoe 的专业护理人员口吻，并用“孩子怎么样？”兼容单胎、双胎和婴儿性别分支。
- 已补充 `misc_lotion.rpy` 的 Debbie 润肤露香味回忆；统一 `Brazilian Bum Bum` 产品名、内心独白括号与跨句省略号，并同步修正 `deb_mall.rpy` 旧译。
- 已补充 `misc_tissue.rpy` 的 Tori 血清任务物品交互；确认 Anon 在 Ursula 办公室垃圾桶取得用过纸巾的前后分支，统一全角内心独白与“翻垃圾桶”的动作语义。
- 已补充 `misc_toad.rpy` 的 Tori 血清材料物品交互；确认森林溪边首次点击只是在抓取前观察外形，统一 `horny toad`／`horny toad extract` 为“发情蟾蜍”／“发情蟾蜍提取物”，并定向修正 `tor05.rpy` 的同任务术语。
- 已补充 `misc_towel.rpy` 的 Debbie 家浴室通用物品交互；确认 Anon 的得意内心独白是《银河系漫游指南》毛巾彩蛋，统一“星际搭车客”及全角内心独白格式，不擅自加入关系阶段或拿取动作。
- 已补充 `note_tori.rpy` 的 Tori 办公室密码纸条交互；区分学校万能钥匙分支与未持有钥匙分支，保留 Anon 对连续偷窃的自嘲及对 Ursula 发现失物的担忧。
- 已补充 `oli_stall.rpy` 的 Olivia 陌生人邂逅；确认本场从意外撞见、Olivia 主动调情和成人触摸推进到因男朋友等待而中断，保留双方首次见面、没有交换姓名及未确立恋爱关系的边界。
- 已补充 `pie_stall.rpy` 的 Pietro 涂油误会；确认 Anon 是误入场景后被误解，Pietro 的自称“阿多尼斯”是腹肌自恋笑点，逃入厕所后的两句内心独白分别是庆幸与担心员工受牵连。
- 已补充 `pizza_boxes.rpy` 的披萨外送结果与工钱领取交互；区分 Tony／Maria 的完美、部分成功和全部失败反馈，统一 Tony 的 `buddy`“小兄弟”、`smalls`“小子”、`champ`“冠军”，并明确产后抱婴儿状态下“腾不开手／晚上结清工钱”的画面语义。
- 已补充 `pizza_kitchen.rpy` 的厨房受限入口；将两句内心独白整理为“后厨危险”到“最好别随便闯进去”的递进，统一全角括号，并避免把 `wander in there` 错写成已经进门后的闲逛。
- 已补充 `tammy_bed2_scope.rpy` 的 Erik 卧室望远镜观察；区分通宵游戏、Jenny 成人内容、润肤露自慰暗示、兽人成人玩具及 Tammy 关系升级分支，并保留 Anon 对新关系发展的惊讶。

- 已补充 `tammy_lobby.rpy` 与 `tammy_yard_scope.rpy` 的时段限制、后院瑜伽观察、偷窥关系边界及 `turned on` 成人语义。
- 已补充 Tenzin 的陌生人定位、格言式书面口吻、`Shoo` 赶人语义，以及服装店单独 `changing room` 统一译“更衣隔间”。
- 已补充 Titomi 的 Omaha／Nebraska 背景、Ara Ara 英文专名、反讽抬杠口吻，以及 `hospitality stick in her ass` 与 `wear a helmet` 两处连续笑点。

- 已补充 `ton_baby.rpy` 的怀孕早期、临产准备、生产后返店、抱婴儿黑帮故事与更晚恢复阶段；统一 Tony 的 `champ`“冠军”、五组动作片引用、Luigi 英文姓名、外送订单及 Tony 知情鼓励的后厨成人关系，并登记源代码单复数疑似颠倒的中性处理。
- 已补充 `tony.rpy` 的客厅、后厨和披萨店跨阶段公共入口；明确初次来店、牛奶任务、街头解围、试送入职与后期家人式信任不能混成同一口吻，并登记 `Trial.`“试送”、`Vehicle.`“车子”、`there's my guy`“我的好小子来了”及 `She's a peach`“她可真是个宝”。
- 已补充 `tool_drill.rpy` 的父亲旧电钻物品交互；确认该工具位于 Debbie 家车库并承接 `bar04.rpy` 画架、`mel01.rpy` 木笛制作任务，统一“旧电钻”及克制的遗物怀念语气。

- 已补充 `tool_shovel.rpy` 的双阶段取铲子入口、Diane菜园任务承接与Jenny车库电池插曲；固定该任务中的 `shovel` 为“铲子”、`One shovel: acquired!` 为“铲子一把，入手！”，并明确文件未揭示大量电池的用途，不能擅自补成成人道具。

- 已补充 `tv.rpy` 的电视频道浏览与Ronald政治讽刺链；确认竞选、腐败被捕、囚服发布会和与Yoo同牢的画面连续性，固定 `perp walk` 为“被押走时的样子／押解示众”，并明确女子沙滩排球中的 `get into` 表示观看兴趣而非亲自参赛。

- 已补充 `ursula.rpy` 的教师休息室违规闯入事件；明确 Ursula 当场打断辩解、以开除相威胁并命令 Anon 回去上课，统一 `teachers' lounge`“教师休息室”与学生对校长的 `ma'am`“校长”。

- 已补充 `vee.rpy` 的 Consum-R 店员接待与全品类销售笑点；明确 Vee 与 Anon 只是店员和顾客，统一 `vegetable stock`“蔬菜高汤”，并按宣传口号与通道编号分别自然处理 `aisle`。

## 测试与校验状态

- `python -m py_compile tools/validate_translations.py tools/audit_recurring_terms.py`：通过。
- `python -X utf8 tools/validate_translations.py --changed`：本批通过，验证 99 个修改过的 Ren’Py 翻译文件；变量、标签、占位符、代码结构和活动译文标点均无异常。
- `jenny_laptop.rpy`：英文原文注释 diff 无变化；无 BOM，902 个 CRLF、0 个裸 LF、903 行、150 个翻译块、0 组菜单映射、0 个替换字符。
- `jenny.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，925 个裸 LF、0 个 CRLF、926 行、149 个活动翻译块、7 组菜单映射、0 个替换字符。
- `jos01.rpy`：英文原文注释 diff 无变化；无 BOM，2358 个 CRLF、0 个裸 LF、2359 行、391 个活动翻译块、2 组菜单映射、0 个替换字符；Git numstat 为 224/224。
- `jos_trade.rpy`：英文原文注释 diff 无变化；无 BOM，832 个 CRLF、0 个裸 LF、833 行、132 个活动翻译块、9 组菜单映射、0 个替换字符；Git numstat 为 118/118。
- `judith.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，123 个裸 LF、0 个 CRLF、文件末尾 LF、19 个活动翻译块、3 组菜单映射、0 个替换字符。
- `june.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，71 个裸 LF、0 个 CRLF、文件末尾 LF、10 个活动翻译块、2 组菜单映射、0 个替换字符。
- `kassy.rpy`：英文原文注释 diff 无变化；无 BOM，78 个 CRLF、0 个裸 LF、文件末尾换行、11 个活动翻译块、2 组菜单映射、0 个替换字符。
- `kevin.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，151 个裸 LF、0 个 CRLF、文件末尾 LF、25 个活动翻译块、0 组本地菜单映射、0 个替换字符。
- `key_school.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，24 个 CRLF、0 个裸 LF、无文件末尾换行、4 个活动翻译块、0 组菜单映射、0 个替换字符。
- `konty.rpy`：英文原文注释 diff 无变化；无 BOM，218 个 CRLF、0 个裸 LF、文件末尾换行、36 个活动翻译块、0 组菜单映射、0 个替换字符；Git numstat 为 33/33。
- `mel_office.rpy`：英文原文注释 diff 无变化；无 BOM，396 个裸 LF、0 个 CRLF、文件末尾 LF、97 个活动翻译块、2 组菜单映射、0 个替换字符；Git numstat 为 73/73。
- `melody.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，157 个裸 LF、0 个 CRLF、文件末尾 LF、23 个活动翻译块、2 组菜单映射、0 个替换字符；Git numstat 为 18/18。
- `mia.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，61 个裸 LF、0 个 CRLF、文件末尾 LF、9 个活动翻译块、1 组菜单映射、0 个替换字符；Git numstat 为 9/9。
- `micoe.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，36 个 CRLF、0 个裸 LF、文件末尾 LF、4 个活动翻译块、2 组菜单映射、0 个替换字符；Git numstat 为 4/4。
- `misc_lotion.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，12 个 CRLF、0 个裸 LF、无文件末尾换行、2 个活动翻译块、0 组菜单映射、0 个替换字符。
- `misc_tissue.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，12 个 CRLF、0 个裸 LF、无文件末尾换行、2 个活动翻译块、0 组菜单映射、0 个替换字符。
- `misc_toad.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，6 个 CRLF、0 个裸 LF、无文件末尾换行、1 个活动翻译块、0 组菜单映射、0 个替换字符。
- `tor05.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，2726 个 CRLF、0 个裸 LF、文件末尾 LF、0 个替换字符；本次仅完成发情蟾蜍、男生更衣室与 `Consum-R` 的定向连续性修复。
- `misc_towel.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，12 个 CRLF、0 个裸 LF、无文件末尾换行、2 个活动翻译块、0 组菜单映射、0 个替换字符。
- `note_tori.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，18 个 CRLF、0 个裸 LF、无文件末尾换行、3 个活动翻译块、0 组菜单映射、0 个替换字符。
- `oli_stall.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，291 个裸 LF、0 个 CRLF、文件末尾 LF、73 个活动翻译块、0 组菜单映射、0 个替换字符。
- `pie_stall.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，111 个裸 LF、0 个 CRLF、文件末尾 LF、28 个活动翻译块、0 组菜单映射、0 个替换字符。
- `pizza_boxes.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，272 个 CRLF、0 个裸 LF、文件末尾 LF、45 个活动翻译块、0 组菜单映射、0 个替换字符。
- `pizza_kitchen.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，12 个 CRLF、0 个裸 LF、无文件末尾换行、2 个活动翻译块、0 组菜单映射、0 个替换字符。
- `sue_stall.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，39 个裸 LF、0 个 CRLF、文件末尾 LF、10 个活动翻译块、0 组菜单映射、0 个替换字符。
- `sushi_shop.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，12 个 CRLF、0 个裸 LF、无文件末尾换行、2 个活动翻译块、0 组菜单映射、0 个替换字符。
- `tammy_bed1_scope.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，102 个 CRLF、0 个裸 LF、无文件末尾换行、17 个活动翻译块、0 组菜单映射、0 个替换字符。
- `tammy_bed2_scope.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，164 个 CRLF、0 个裸 LF、文件末尾 LF、27 个活动翻译块、0 组菜单映射、0 个替换字符。
- `tammy_lobby.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，24 个 CRLF、0 个裸 LF、无文件末尾换行、4 个活动翻译块、0 个替换字符。
- `tammy_yard_scope.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，60 个 CRLF、0 个裸 LF、无文件末尾换行、10 个活动翻译块、0 个替换字符。
- `tech_gamepad.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，12 个 CRLF、0 个裸 LF、无文件末尾换行、2 个活动翻译块、0 个替换字符。
- `ten_stall.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，123 个裸 LF、0 个 CRLF、文件末尾 LF、31 个活动翻译块、0 个替换字符。
- `titomi.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，366 个 CRLF、0 个裸 LF、文件末尾 LF、59 个活动翻译块、2 个菜单映射、0 个替换字符。
- `tym_stall.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，28 个裸 LF、0 个 CRLF、文件末尾 LF、7 个活动翻译块、0 组菜单映射、0 个替换字符；Git numstat 为 7/7。
- `viv.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，157 个裸 LF、0 个 CRLF、文件末尾 LF、23 个活动翻译块、4 组菜单映射、0 个替换字符；Git numstat 为 16/16。
- `viv_office.rpy`：英文原文注释 diff 无变化；有 UTF-8 BOM，84 个 CRLF、0 个裸 LF、无文件末尾换行、14 个活动翻译块、0 组菜单映射、0 个替换字符；Git numstat 为 10/10。
- `viv01.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，1322 行、CRLF、文件末尾 LF、219 个活动翻译块、3 组字符串映射、0 个替换字符；Git numstat 为 134/134。
- `viv02.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，1663 个 CRLF、0 个裸 LF、文件末尾 LF、275 个活动翻译块、3 组字符串映射、0 个替换字符。
- `viv03.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，2137 个 CRLF、0 个裸 LF、文件末尾 LF、354 个解析块、0 个替换字符；完整精修浪漫诗、图书馆露骨书、Roxxy 课堂朗诵、法式接吻及 Ursula 打屁股惩罚。
- `viv04.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，3770 个 CRLF、0 个裸 LF、文件末尾 LF、625 个活动翻译块、2 组主要菜单映射、0 个替换字符；完整精修考试危机、啦啦球任务、Bridget办公室换衣、Jenny编排动作及Jenny／Roxxy初次会面。
- `viv05.rpy`：英文原文注释 diff 无变化；无 UTF-8 BOM，870 个 CRLF、0 个裸 LF、文件末尾 LF、144 个 translate 块、143 个活动英文—中文对应、2 组菜单映射、0 个替换字符；完整精修正式考试、法国葡萄酒、首次／重复性交分支、书桌／椅子场景及 Ursula 结尾双关。
- `python -X utf8 tools/audit_recurring_terms.py --changed --fail-on-mismatch`：全部已登记重复称呼、口癖、关系身份、连续笑点、专名和术语通过，0 mismatch。
- `git diff --check`：通过。
- `python tools/validate_translations.py --no-compare`：报告 26 个仓库既有问题，已登记于上方队列。
- GitHub Actions 使用 Ren’Py 8.5.3 编译并运行 `tools/build_rpa.py`。
- 本机 PATH 中未发现 Ren’Py SDK；Ren’Py compile/lint 尚未运行。
- `python -X utf8 tools/build_rpa.py`：成功打包并校验 327 个文件（`dist/zh_hans.rpa`，42,313,279 字节；构建产物由 `.gitignore` 忽略）。

- `bar01.rpy`：已完整精修美术线开端、陶土课堂、长颈鹿成人双关、Ursula削减预算与Ronald美术比赛约定；统一课堂称谓“老师”、材料“一块陶土”、内心独白全角括号和中文省略号。

- `bar02.rpy`：已完整精修美术搭档招募、Mia魅力门槛、Eve背包与画板任务、Chad自画像交易／Eve武力取回分支、Barbara与Starchild往事及首次互画肖像；统一“画板”“小可爱”和英文专名。

- `bar03.rpy`：已完整精修旧杂志收集、图书馆多功能室、Kevin男性健身杂志、Melody长笛问答与特制布朗尼、拼贴画／大学误听、Barbara对Mia的成人谈话边界、香蕉桃子双关及密宗性爱经历；统一“拼贴画”“多功能室”“小可爱”“藜麦”及课堂称谓“老师”。

## 收尾阶段记录

- 已完成剩余剧情队列的逐文件复核与本轮明显错译修正，覆盖 Debbie、Diane、Hana、Ivy、Eve、Ella、Zana 等文件；重点处理了园艺双关、角色性别与称谓、英文昵称、成人场景语气和中文自然度。
- 已统一并登记 Cuntech、才艺表演、触觉引擎、门禁密码、啦啦队制服、迷你外阴钥匙、SL-700 胯下火箭钥匙等术语；`jenny_boyfriend` 审计规则保留“男女朋友”的自然成对语境。
- 已补充 Tori 两种血清的故事阶段、Melody 才艺表演线、Debbie 复杂关系、Diane 园艺双关、Hana 女性身份与 Bubbles 英文姓名说明。
- 已完成全仓活动译文括号、中文标点、占位符间空格和英文原文注释完整性检查；不得改动 Ren’Py 变量、标签、说话人标识及英文原文注释。
- 已将翻译语言目录统一为 `tl/zh_hans/`，同步更新工具、README、GitHub Actions 和术语文档中的路径，并生成 `dist/zh_hans.rpa`。

## 最终校验记录

已完成最终校验：`python -X utf8 tools/validate_translations.py --no-compare` 通过（322 个 Ren’Py 翻译文件）；`python -X utf8 tools/audit_recurring_terms.py --fail-on-mismatch` 通过（全部登记术语 0 mismatch）；`git diff --check` 通过；`python -X utf8 tools/build_rpa.py` 及 `--verify-only` 均通过，生成并验证 `dist/zh_hans.rpa`（327 个文件，42,333,816 字节）。
| `tl/zh_hans/bytecode_strings.rpy`、`tl/zh_hans/sms_fix.rpy` | 补充字符串与短信运行时修复文件重命名并系统性精修 | Anon、Debbie、Jenny、Maria、Daisy、Odette 等 | 完成 | 去除 `renpybox` 前缀；精修成人直播、直播间观众、孕期任务、分娩短信、冷落条件、Bad Monster、Electro Clit、月相、Outlood Express、cookie jar 和姿势/UI 文本；同步短信映射加载路径及术语表 | 完整翻译校验、重复术语审计、RPA 构建与验证通过后归档 |

### 2026-08-06：跨行断句衔接专项复核

- 对 tl/zh_hans/src/plot/**/*.rpy 中英文原文跨翻译条目断句进行系统筛查，重点复核上一条以 ... 结尾、下一条以 ... 开头的连续对白。
- 精修 ano03.rpy、deb_tv.rpy、deb_visit.rpy、deb23.rpy、mar_couch.rpy、tin_vault.rpy、tin_dusk.rpy；修正语序、重复指代、中文名词结构、成人场景语气及 `at the end` 误译。
- 另修复 ano01.rpy 中 Mrs. [saga.cast.tammy.clan.name[0]]... 被错误断成“太……太”的问题，恢复为自然的“太太……”。
- 未改动任何英文原文注释、Ren'Py 标签、说话人、变量或占位符；本轮无新增专名术语，相关固定表达已登记在 translation_context/terminology.md 。

### 2026-08-06：Vivienne 法语第三语言显示复核

- 对 `viv03.rpy`、`viv04.rpy` 的法语菜单和带 `show_lang` 的对白进行复核，修复此前因 UTF-8 编码问题产生的 `?` 乱码。
- 按 `show_lang` 规则整理第三语言显示：无 `show_lang` 时保留法语并追加中文释义；有 `show_lang` 时主对白只显示自然中文，同时保留法语小字；同步修复 `Merci`、`Magnifique` 等菜单字符串中的占位符 `[saga.cast.anon]`。
- 结合 Vivienne 与 Anon 的关系阶段，复核亲昵称呼与 `Truly?!` 等表达的语气，避免提前强化或弱化关系；统一带 `show_lang` 的法语对白处理。
- 将 Vivienne 法语相关固定表达与第三语言显示规则补充记录到 `translation_context/terminology.md`。


## 2026-09-12 重复句式与相似分支收敛

按用户调整后的范围执行分组复查，不要求全仓逐句重译。新增122处修改，涉及23个文件；113条已确认句式纳入回归基准。候选分组规模、语境例外和源文对应待查项见 `recurring_terms.md`，工具与规则见 `style_guide.md`。上一轮123处修改继续保留。

发包对比基线为 `v21.0.0-wip.7944` 的实际 `zh_hans.rpa` 附件（2026-09-02更新），不能直接用指向旧目录的标签代替。附件 SHA-256：`b7c7976c1f74d205f2794512e34adf991919a33d96ba1755a1f46a2d839924bf`。本轮开始 HEAD 为 `09a055c`；开始时相对附件有335条差异，分布于75个文件。

未运行游戏内场景验证、Ren’Py compile/lint，未构建或发布新RPA。日记抽取字符串的整页拼接仍需运行时验证；`tin_baby_*` 开发占位继续按 `english_residuals.md` 登记待查。

本轮验证：全仓323个翻译文件结构检查通过，累计45个修改文件相对HEAD结构检查通过；113条句式基准、全部登记术语、中英文间距均为0 mismatch；`git diff --check`通过。新工具已验证重复分组、高相似检索、译文偏离／原文缺失检测和只读行为。

## 2026-09-12 ano10上下文遗漏修正

此前清理孤立块时未检查替代块的extend衔接，导致有效39869a88保留“哦。”，与后续“的。天哪。”不连贯。本次将其修正为“我。”，保留7944有效ID和动作参数。对171个已删除块按原文文本在对应7944剧情文件检索，并筛查命中附近的extend，候选均落在此处同一连续表达；该筛查不等于所有分支已完整人工审校。清理要求已补入style_guide.md，具体句链归入recurring_terms.md。

## 2026-09-12 翻译块顺序及源码行号归位

从7944引擎读取有效ID的源码路径与行号，对47个文件进行完整块归位或注释修正，共补齐／修正5265条位置注释。按ID比对确认对白和动作参数未被改写；所有34841个有效中文对白块的源码位置与顺序核对通过。ano10的39869a88归回原文299行，deb_lobby的66773ff1归回101行。Python翻译块不参与对白排序，字符串表保留原状。README不改，不构建RPA，不进行场景游玩验证。

## 2026-09-12 非露骨前后对白第一批（未完成全角色全场景审校）

- 实际修改9个文件、67处译文：deb_lobby、deb_mall、deb_visit、jen_gfe、jud_stall、mar_door、mel_office、tin_dusk、viv_office。只改译文，保留原文注释、行号、ID、动作参数与源码顺序。
- jud_stall、mar_door、mel_office、tin_dusk、viv_office、deb_lobby已读取全文英中对照；仅修改其中非露骨的邀请、拒绝、问候、收尾等内容。deb_mall、deb_visit、jen_gfe本批核对了相关入口、购物陪伴、次晨和告别段落，不能据此标记整文件完成。jen_shower的收尾已查看，本批未修改。
- 修复书面化和直译句式、Jenny挖苦口吻、Tina预约确认重复、Debbie日常关照及Rebecca姓名误译。角色规则归入characters.md，重复表达归入recurring_terms.md，回归基准总计204条。
- 9个变更文件结构校验、204条句式回归、混排间距及变更范围术语检查通过。未构建RPA、未改README、未进行场景游玩验证。
- 未完成范围：其他初次／重复关系场景，以及本批大型文件中未覆盖的非露骨前后对白，仍需按实际分支逐场景检查。320条启发式候选仅用于定位，不能当作全部场景覆盖率；本记录不宣称完成“所有主角与其他角色”的全面润色。

## 2026-09-12 全角色、全场景非露骨前后对白专项收尾

在上一批67处修改之后继续完成本轮系统复核，基线HEAD为357713f。本轮实际新增243处译文修改，涉及44个剧情文件；上一批已提交的修改继续保留，不重复计入。覆盖与人工阅读口径见file_inventory.md；没有把关键词候选数量当作全部场景覆盖率，也不宣称全部对白逐句精修。

主要完成：角色口吻与重复分支统一，初次／再次／忙碌拒绝及孕育后续核对，主客体和单复数纠错，预约星期、收尾指代及短句否定极性修正；修复deb13的9处`[when[1]！l]`格式转换损坏。仅修改RPY译文载荷，保留源注释、ID、源行号、动作、顺序、BOM与换行方式。补强变量转换审计，已有规则分别归入characters、storylines、style_guide、recurring_terms及english_residuals，句式回归增至433条。

验证：全库323个翻译文件通过结构检查；433条句式回归、全库登记术语、中英文混排间距均0偏差；34818条可核实原文注释0差异；34841个有效对白块位置和顺序0问题；嵌套变量转换回归4项通过。7944隔离环境Lint未报告翻译错误，保留引擎建议开启config.check_conflicting_properties的通用提示。

未改README，未构建或发布zh_hans.rpa，未进行场景游玩验证，未提交或推送。review_2026-09-12.md保持删除。实际游戏中的视觉呈现、日记动态拼接，以及当前版本源脚本的开发占位仍不在本次静态验证的保证范围内。

## 2026-09-12 分段对白连贯性专项

本轮基线HEAD为8a141d7，开始时工作区干净。新增62处译文修改，涉及22个剧情文件。修复分段语序、重复原因句架、分支共用关联词、回应中的too、关系从句误译、工具与时间指代，并保留原文的口吃、打断和有意重启。没有增删或移动翻译块；源注释、位置、ID、动作、变量、标签、BOM及换行均保留。

覆盖口径：以7944引擎初始化后的节点关系建立静态路径，映射34827个源剧情对白节点，提取35089对相邻对白。人工连读1592对核心分段候选和1531对补充停顿／跨说话人候选，共3123对；其中包含全部26处extend衔接（21处有文本或计时内容，5处为空），并对疑点回查完整英中句组及源分支。亲吻、沉默等中间节点也参与上下文判断。候选对存在共享句和重叠，不代表3123个独立场景，也不等于所有34827条对白逐句重译。

静态路径保守枚举if／menu及可解析call／return、jump，不执行条件求值。konty和school_pa两处动态跳转的8个／23个目标label已作为独立入口纳入遍历，但没有验证运行时随机值、seed或自定义语句的所有行为。没有进行场景游玩，不能把本次结果称为全部实际分支的游戏内验证；无分段标记的其他隐含衔接仍可能需要后续语境复核。

规则分别归入style_guide.md、recurring_terms.md、storylines.md；句式回归增至494条，并支持按翻译ID限定语境。补齐校验器对nvl clear后7条教程文本的识别，新增6项测试，覆盖清屏后配对、控制流隔离、同源句ID限定、缺失／错误ID及旧规则兼容。

验证完成：全库323个翻译文件通过结构检查；62处修改与逐文件备份逐行核对，仅译文载荷改变；494条句式基准、混排间距和登记术语0偏差；34818条源注释0差异；34841个有效块的位置及顺序0问题。6项工具测试通过。最终7944隔离Lint未报告翻译错误，仅保留config.check_conflicting_properties的引擎通用建议。

README未改，不构建zh_hans.rpa，不进行场景游玩验证，不提交或推送。review_2026-09-12.md保持删除。

## 2026-09-12 既有露骨对白忠实性、语义及衔接复核

本轮基线HEAD为a23b5b2，开始时工作区干净。在已完成的连贯性专项之上，新增51处译文修改，涉及16个剧情文件；上一轮已提交的修正不重复计入本轮数量，未扩写场景。主要修复施受关系、动作含义与阶段、分段位置重复、缺失的姿势／地点／持续状态、力度擅自增强和喘息误作笑声。

阅读口径：逐条查看1122条核心关键词英中候选（含非性含义，需排除），另从655条动作／姿势补充候选中筛查相关项，并补查came／coming、swallow等词形。候选用于发现问题，不等于1122个独立场景。疑点回查源注释、说话人、动作和连续句组；修改后再沿7944节点关系连读前后。未声称所有对白已逐句重译，也没有用关键词数量作为全场景覆盖率。

规则归入style_guide、characters、storylines、recurring_terms及english_residuals；句式回归累计545条。保留源文的停止／拒绝、疼痛、内外射及条件区别，不把短句或部位词全局强化。

验证：323个翻译文件通过结构检查；51处变更与修改前副本逐行核对，仅译文载荷变化，原注释、ID、行号、动作、变量、格式、BOM和换行保留；545条定译回归、混排间距和登记术语0偏差；34818条源注释0差异；34841个有效翻译块位置与顺序0问题。7944隔离环境Lint未报告翻译错误，仅保留config.check_conflicting_properties的引擎通用建议；git diff --check通过。

遵照用户限制，README未改，不构建zh_hans.rpa，不进行场景游玩验证，不提交或推送；review_2026-09-12.md继续保持删除。静态检查不替代实际画面和动态分支验证。

用户反馈修正：上一轮对Tina的pound处理削弱了原有口吻，已恢复tin_dusk_lounge_2f51d8bc及tin_vault_vault_merge1_ad6e7bb6原译，并更新两条回归及风格规则。上一轮51处修改中这2处撤回，当前保留49处译文修改；不撤回已核实的语义纠错。

## 2026-09-12 全面筛查后复核

基线HEAD为01e285f，开始时工作区干净。本轮净修正100处译文、16个翻译文件，主要补上此前漏检的Jenny日记多片段语序、词义和指代问题；同时复核重复句与前轮改动，纠正把身体反应写成动心、把当下体验泛化为关系表白等偏移，保留用户认可的粗口力度。覆盖口径见file_inventory.md，规则归入style_guide、storylines、recurring_terms，句式回归累计638条。

与修改前副本逐行核对，100处均仅改译文载荷，未增删或移动翻译块；源注释、ID、源行号、动作、变量、标签、BOM及本地换行保留。工作过程中出现jen24、jen26各一处外部修改，保留，未计入上述100处。

验证：323个文件结构检查、638条句式回归、登记术语和混排间距检查通过；34818条源注释无差异，34841个有效翻译块位置与顺序无问题。7944隔离Lint未报告翻译错误，仅保留config.check_conflicting_properties通用建议。

README未改，review_2026-09-12.md保持删除；不构建RPA，不进行场景游玩验证，不提交或推送。日记已静态整页连读，但实际字体布局、旁注位置和动态选页未作游戏内验证；源文已有开发占位及异常格式没有以改译文掩盖。静态校验与疑点复核通过，不等于所有文本已无可改进。

## 2026-09-12 称谓、叙事分类及含混对白复核

本轮修改7个翻译文件、15处译文：10处Jenny姓名后置公主称谓（含斜体）、2处Narrative孕期分类、1组直播收入与介意事项的问答、1处拉长粗口误译。全库扫描同类称谓、Narrative及短粗口候选，保留语义正确的“去你的”等表达。规则归入style_guide、terminology、storylines，句式回归累计653条。保留翻译块、原文注释、源码行号、动作、变量及标签；README不改，不构建RPA，不进行场景游玩验证。

## 2026-09-12 继续润色自然度

本轮修正3个文件19处译文：Jenny日记16处、ano13领养问答2处、viv03诗歌回应1处。按已有7944日记页序连读，筛查口头填充词、指代、评价对象和英语句架残留；保留标签、旁注、变量、原文注释、ID、源行号与动作。规则归入style_guide和storylines，句式回归累计672条。此次是明确候选的语境润色，不代表全部对白逐句精修；README不改，不构建RPA，不进行场景游玩验证。

## 2026-09-12 口头语、指代与语气继续优化

本轮修改9个剧情文件、18处译文；复核短回应的肯定、勉强接受及不以为然差别，明确问人、调频、真假吉他等对象，调整日常劳动及住院问候的书面句架。保留语境合适的既有译法，没有全局统一所有If you say so。规则归入style_guide、storylines，回归累计690条；不改README，不构建RPA，不进行场景游玩验证。

## 2026-09-13 角色连续审读与反查

基线HEAD为0af0b87，开始时工作区干净。本轮连续读取31个文件、2121对原译文本，覆盖主要人物的日常互动、角色初始任务，以及若干完整关系场景和结果分支；实际修改20个翻译文件、138处译文。详细文件清单见file_inventory.md。本轮不是重新宣称全库37947对文本全部逐句定稿，也不把31个文件等同于31个独立场景。

主要修复：菜单与寒暄误译、施受关系、未完句提前补全、喘息误作笑声、开工误译吃饭、设备／工作对象不明、措辞削弱或额外解释，以及同角色近似分支的语气差异。反查前轮Debbie的Yeah, I bet，撤回重述上一整句的冗长回应。保留Tina用户认可的粗口、Tori科学风格、Judith食物叹词、Jenny付费女友边界及原有拒绝。

修改后复核重点句组，并与逐文件修改前副本逐行比对：138处均只改译文载荷；原文注释、ID、源行号、动作、变量、标签、BOM及本地换行方式保持不变。827条句式回归通过；源注释34818条无差异，有效翻译块34841个位置与顺序无问题。其余最终验证结果接本节末尾。

README未改，不构建zh_hans.rpa，不进行场景游玩验证，不提交或推送；review_2026-09-12.md保持删除。实际画面、字号、旁注位置与动态分支仍未做游戏内验证，源脚本开发占位继续单独看待。

最终验证：全库323个文件结构检查通过；827条句式回归、混排间距及全库登记术语0偏差。7944隔离Lint无翻译错误，仅保留config.check_conflicting_properties引擎通用建议。git diff --check通过。

## 2026-09-13 全量人工路径审校目标启动

目标保持为全部对白按实际场景与分支连续读完。新增manual_review.json作为持久台账，纳入323个文件、37947对原译；历史筛查、候选阅读和修改数量不自动折算成路径完成。当前重新对照7944原脚本完整读取+prologue、annie、ang的43条；序章线性路径完成，后两者局部路径已读，Model／Linens跨任务事件仍待交叉核对。全文目标未完成，继续按台账推进。

台账逐条保存翻译ID、位置、原译摘要，逐文件记录译文及原脚本指纹、实际阅读路径和未完成事件；tools/audit_manual_coverage.py只验证当前译文是否匹配记录，不授予人工完成状态。任何后续译文变更使对应文件的已读记录失效，需重新复核。未改README、不构建RPA、不进行游玩验证。

## 2026-09-13 首日及取货路径继续审校

本次在既有138处修改上新增4个文件21处译文修正，未覆盖或撤回已有改动。人工台账新增804条，累计847/37947条；新增阅读范围与未完成边界见file_inventory.md及manual_review.json。ano01本地文本已完整读至放学，尚未把外围任务调度标为完成；bar04、bar05仅登记实际读完的局部路径。全文目标继续保持未完成。

规则归入style_guide和storylines，句式回归累计848条。台账检查补充逐项ID、行号、原译指纹、重复记录及原脚本指纹校验，工具只检查记录有效性，不授予人工覆盖。24个已修改翻译文件通过结构检查，848条定译回归0偏差，847条记录有效且无过期文件。

README未改，不构建RPA，不进行游玩验证，不提交或推送；本次未重跑引擎Lint。

补充验证：本批21处与修改前字节副本核对，仅译文载荷变化，前后结构及换行不变；混排间距、登记术语均0偏差，git diff --check通过。README无差异，review_2026-09-12.md不存在。

## 2026-09-13 美术比赛与获奖后连续审读

本批新增569条记录，累计1416/37947条；本批修改5个翻译文件35处译文，句式回归累计883条。保留之前工作区改动，README未改，不构建RPA、不进行场景游玩验证、不提交或推送。

主要修正：发言权限误作称呼、遗漏回家睡觉指令、物品和画作指代、工作安全感、数量与次数、分段强调，以及画布和调色提示。规则已归入style_guide与storylines，实际覆盖和待审边界记在manual_review.json。台账增加已读逻辑依赖指纹；依赖失效时校验不再计入有效记录。全文目标未完成。

本批验证：27个已修改翻译文件结构检查通过；883条句式回归、混排间距与登记术语0偏差；1416条人工记录及其原脚本/登记依赖指纹有效。35处改动与各自修改前副本逐行核对，仅译文载荷变化，结构、ID、注释、BOM及换行保留；git diff --check通过。本批未重跑引擎Lint。

## 2026-09-13 美术前半段继续连读

新增756条人工记录，累计2172/37947条；本批在既有改动基础上修改3个文件29处译文，句式回归累计912条。修正展示对象、重复安慰、物品指代、寒暄、未完句与Chad口头语。规则归入style_guide和storylines。

bar02关键返回路径出现eve1真值后调用eve2的情况，已留待结合call框架核实；未删除、移动或跳过相应译文，不以猜测掩盖可能的原脚本重复。其余完整事件触发与bar04继续待审，全文目标未完成。README未改，不构建RPA、不进行游玩验证、不提交或推送。

本批验证：29个已修改翻译文件结构检查、912条句式回归、间距和2172条台账记录均通过；29处新增改动与修改前字节副本核对，仅译文载荷变化，结构、注释、ID、BOM及换行保留；git diff --check通过。本批未重跑引擎Lint。
