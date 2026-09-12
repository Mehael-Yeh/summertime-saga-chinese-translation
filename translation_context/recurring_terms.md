# 重复称呼、口癖与专名复查记录

更新时间：2026-09-12

## 非地名英文残留专项

新增电击阴蒂棒、轻量版、LARPer、mesmerizing共4条审计规则；10条目标字符串的修复、外语排除项与开发占位待查见 `english_residuals.md`。

## Debbie 的 mister 称呼

Debbie 对 Anon 的句尾 mister 是熟人间的嗔怪、提醒或警告，不是礼貌尊称“先生”。调侃可译“小坏蛋”，轻斥可译“你这小子”，严肃拒绝可省略称呼，以“想都别想”“我可没跟你开玩笑”等整句语气承载；不强制每次使用同一中文称呼，不把认真划界一律写成调情。deb01.rpy 电话中的 mister 指威胁者，不套用亲昵称呼；其他说话人单独判断。

## 触发规则

处理完整文件时，只要英文原文中的同一名词、组合词、称呼或固定表达在短距离内出现 **2 次及以上**，就先把它视为潜在的专名、人物口癖或关系称呼，不在当前几行内孤立定译。

必须依次执行：

1. 在当前完整文件中确认说话人、指代对象、关系阶段和重复方式。
2. 使用仓库级搜索或 `python -X utf8 tools/audit_recurring_terms.py --query "英文短语"` 查找跨文件出现位置。
3. 判断其属于人物姓名、描述性称呼、口癖、地点/物品/车辆专名，还是普通重复用词。
4. 确认稳定译法后，同时登记到 `terminology.md`、`recurring_terms.json` 和本文件；涉及人物时同步更新 `characters.md`。
5. 未通读的后续文件只登记为复查队列，不直接做无上下文的全局替换。
6. 后续每处理一个文件，运行 `python -X utf8 tools/audit_recurring_terms.py --changed --fail-on-mismatch`，确保已登记表达没有再次漂移。

> `recurring_terms.json` 是机器可读的审计规则；`tools/audit_recurring_terms.py` 只检查和报告，不自动改写译文。

## 2026-09-12 地名专项复查

地名无需等待重复两次：首次出现即参照 UI。正式映射及歧义例外见 `terminology.md`；机器规则新增 16 个 `location_*` 条目，沿用已有的夏日学院和 Consum-R 规则。

已修复 Cosmic Cumics、Cupid、Saga Financial、Ara Ara、Sugar Tats、Pink 的英文残留及不同译法，覆盖对话、任务提示、物品说明和字节码提取文本；同时纠正把 Pink 商店后屋称为“粉红酒吧的密室”的地点误认。Raven Hill 的现有 11 处完整名称均为“渡鸦山”，登记规则防止再次出现“鸦山／鸦丘”等漂移。

新增复核：Pink 按用户意见定为“粉色诱惑”；Retro Strike 改为“复古全中”，保留保龄球全中的含义；CineSaga 统一为 UI 的“传说影院”。

本次以 sets.rpy 所列 18 个地点专名为核对范围；一般房间名、颜色、人物与频道名称不机械套用店名规则。审计通过只说明已登记规则一致，不等同于游戏内逐场景验收。

## 已确认条目

| 条目 | 类型 | 固定处理 | 仓库出现范围 | 当前结论 |
|---|---|---|---|---|
| Tony 的 `champ` | 人物专属称呼 | 冠军 | 173 处 / 13 个文件 | `ano09.rpy`、`pizza_boxes.rpy`、`ton_baby.rpy` 与 `tony.rpy` 已统一；当前已复核文件中无旧译残留 |
| Tina 的 `babyface` | 人物专属称呼 | 小帅哥 | 42 处 / 10 个文件 | `ano09.rpy`、`ano11.rpy`、`ano13.rpy` 的称呼已统一；非称呼用法按具体指代自然翻译，不机械使用“娃娃脸” |
| Maria/Tony 的 `dollface` | 老派亲昵称呼 | 美人儿 | 3 处 / 3 个文件 | `ano09.rpy`、`ano11.rpy`、`ano13.rpy` 已全部统一 |
| `The Blue Falcon` | 车辆专名 | 蓝色猎鹰号 | 6 处 / 1 个文件 | `ano09.rpy` 全部一致 |
| `The Sapphire Stallion` | 车辆候选名 | 蓝宝石种马号 | 2 处 / 1 个文件 | `ano09.rpy` 全部一致 |
| `The Overcompensator` | 车辆专名/笑点 | 过度补偿者 | 4 处 / 2 个文件 | `ano09.rpy`、`jos_trade.rpy` 当前核心译名一致 |
| `Mini Vulva` | 车辆专名/色情双关 | 迷你外阴 | `jos_trade.rpy` 3 处 | 车型名三处统一；不漂移为“迷你小穴／迷你小阴唇” |
| `SL-700 Crotch Rocket` | 车辆专名/色情双关 | SL-700 胯下火箭 | `jos_trade.rpy` 2 处 | 纯电动踏板车车型名；保留胯下／高速摩托双关 |
| Tony 的 `capisce` | 人物口癖 | 懂了没？／明白吗？ | 25 处 / 10 个文件 | 允许按威胁、催促、确认语气微调，但必须保留 Tony 的固定语用功能 |
| Tony 对 Anon 的 `protégé` | 关系定位 | 徒弟 | 5 处 / 3 个文件 | `ano10.rpy`、`ano11.rpy` 已统一；只剩 `tin_vault.rpy` 待随完整场景复核 |
| `cannoli`（食品） | 食品术语 | 意式奶油甜馅卷 | 4 处食品用法 / 4 个文件 | `ano10.rpy`、`mar_cook.rpy`、`mar_baby.rpy`、`mar_dark.rpy` 已复核；`Holy cannoli` 感叹语排除 |
| `mustache ride` | 成人双关 | 骑胡子 | 4 处 / 2 个文件 | `ano10.rpy`、`ano15.rpy` 已全部复核并统一，保留早期 Anon 不懂含义的笑点 |
| Tony 的 `The Plumber` | 人物旧绰号 | 保持 `The Plumber` | 1 处 / 1 个文件 | `ano11.rpy` 已确认是旧黑帮专名，不翻译、不音译 |
| `Eddie Four-Fingers` / `Four-Fingers` | 人物姓名/绰号 | 保持英文原形 | 3 处 / 2 个文件 | `ano11.rpy`、`ano13.rpy` 已统一，中文音译/混合写法已清除 |
| Dimitri 的 `little bunny` | 戏谑性固定称呼 | 小兔子 | 11 处 / 4 个文件 | `ano03.rpy`、`ano06.rpy`、`ano11.rpy` 已确认；`deb18.rpy` 3 处列入后续队列 |
| `borscht` | 俄式食品 | 罗宋汤 | 2 处 / 1 个文件 | `ano11.rpy` 两处已统一，并登记防止后续漂移 |
| `prosciutto` | 食品术语 | 意式风干火腿 | 4 处 / 1 个文件 | `ano13.rpy` 四处连续配料台词已统一 |
| `gorgonzola` | 食品术语 | 戈贡佐拉奶酪 | 4 处 / 1 个文件 | `ano13.rpy` 四处连续配料台词已统一 |
| `calzone` | 食品术语 | 意式烤饺 | 3 处 / 3 个文件 | `ano09.rpy`、`ano13.rpy`、`ano15.rpy` 已全部复核并统一 |
| `Beachside Apartments` | 地点专名 | 海滨公寓 | 3 处 / 3 个文件 | 资源表、`ano13.rpy`、`ano14.rpy` 当前核心译名一致 |
| `moderate affection points` | 系统提示 | 好感度中幅提升 | 2 处 / 2 个文件 | `ano12.rpy`、`ano14.rpy` 已统一，角色变量和随机数表达式保持原样 |
| `hydration is key` | 固定口号 | 补水最重要 | 2 处 / 2 个文件 | `ano13.rpy`、`ano15.rpy` 已统一 |
| `capicola` | 食品术语 | 卡皮科拉火腿 | `ano15.rpy` | Tony 的意大利式熟食比喻，已复核 |
| `Boy, boy, boy... very tall boy.` | 暗号/重复句 | 男孩，男孩，男孩……长得高高的男孩。 | `ano15.rpy` | 保留 Tony 的拙劣暗号和重复节奏 |
| `godfather` | 关系身份/黑帮笑点 | 教父 | 8 处 / 2 个文件 | `ano16.rpy` 与 `mar_baby.rpy` 已复核；保留《教父》笑点，不改成“干爹” |
| `pump another baby in me` / `put another baby in me` | 生育与性交双关 | 再让我怀上一个孩子 | `mar01.rpy` | 保留 Maria 主动要求受孕的成人含义，不弱化为普通“再要个孩子”。 |
| `rang my bell` | Maria 的成人双关 | 把我弄得够爽 | `mar01.rpy` | 结合高潮后的语境处理，不译成“刮目相看”等普通赞美。 |
| `workplace seminar` / `the seminar` | 连续笑点 | 职场性骚扰培训／培训 | 2 处 / 1 个文件 | `ano15.rpy` 已结合员工场景复核；不是 Tony/Maria 性行为暗语 |
| `The Falsettos` | 电视节目名 | 《假声》 | `mar_couch.rpy` | 保持节目标题格式，不按普通复数名词直译 |
| `horizontal pizzica` | 成人双关 | 横着做披萨 | `mar_couch.rpy` | 保留披萨店人物的性行为双关 |
| `lampredotto` | 意大利食品 | 灯笼牛肚 | `mar_couch.rpy` | Tony 的食物比喻，保持食品指代 |
| `primed pussy` | 成人起哄 | 水润润、正等着开干的骚屄 | `mar_couch.rpy` | 保留 Tony 粗俗起哄；不得误写为“骚屌” |
| `tap that` | 性行为动作 | 肏她一顿 | `mar_couch.rpy` | 明确动作含义，不弱化成普通“碰她” |
| `work that big cock` | 成人起哄 | 好好使唤那根大鸡巴 | `mar_couch.rpy` | 保留 Tony 粗俗、鼓动式口吻 |
| `strike` / `bases loaded` / `hit` / `knuckleball` | 棒球与性行为连续双关 | 按击球、满垒、安打、蝴蝶球语境连贯处理 | `mar_couch.rpy` | 必须把电视球赛解说与沙发性交作为连续双关整体复核 |
| `Devil's Threeway` | 三人性行为招式名 | 恶魔三人行 | `mar_dark.rpy` | 保留 Tony 夸张粗俗的命名方式 |
| `The Kidney Shifter` | 性行为招式名 | 移肾术 | `mar_dark.rpy` | 保留 Tony 夸张粗俗的命名方式 |
| `batter` / `little guys` / `cannoli` | 造人与食物连续双关 | 面糊／小家伙们／意式奶油甜馅卷 | `mar_dark.rpy` | 三组表达共同服务受孕与食物双关，需整体理解 |
| Debbie 的 `sweetie` | 高频亲昵称呼 | 亲爱的；歌曲/明确母性语境可译“宝贝” | 639 处 / 66 个文件 | 普通对话保持“亲爱的”，关系阶段由整句语气体现；`deb22.rpy`、`deb26.rpy`、`deb_lobby.rpy`、`deb_visit.rpy`、`jen11.rpy` 的 5 处异常列入后续完整场景复核 |
| Anon 对 Debbie 的 `ma’am` | 关系称谓 | 夫人 | Debbie 线多个文件 | 体现房东与房客之间带亲近感的礼貌；已统一明确命中，不与“女士”“长官”交替 |
| `bowl cut` / `bowl-` | Josie 对 Anon 的固定挖苦称呼 | 锅盖头／锅盖—— | `deb13.rpy`、`jos01.rpy`、`jos_trade.rpy`、`josie.rpy` | 已通读相关车行文件并统一；完整称呼与被打断形式必须区分 |
| `poor boy` | Yoo 对 Anon 的固定贫穷羞辱 | 穷小子 | `jos01.rpy`、`yoo.rpy` | 不按字面漂移为“可怜的小子／可怜的孩子”，保持对经济状况的攻击 |
| `Employee of the month` / `Emproyee of month` | Yoo 的车行业绩头衔 | 月度最佳员工 | `yoo.rpy` | 正确拼写、故意错拼和菜单提问指向同一头衔，三处统一 |
| `TPS report(s)` | 车行文书工作笑点 | TPS报告 | `jos01.rpy` | 与后面的普通费用报表区分，不泛化为所有报告 |
| `T-straps` | Josie 抢购的鞋款 | T字带凉鞋 | `jos01.rpy` | 同一场景四次重复，保持一致 |
| `Hattori Hanzō` | 人物姓名 | 保持 `Hattori Hanzō` | `jos01.rpy` | 英文姓名保持原状，不写“服部半藏” |
| `Consum-R` | 商店专名 | 购乐百货 | 跨多个剧情与资源文件 | UI、购物任务、工作地点引用统一中文品牌名 |

| Diane 对 Anon 的 `stud` | 人物调侃称呼 | 帅哥 | Diane 相关文件 | `deb26.rpy` 两处已统一；只在 Diane 直接称呼 Anon 时采用，普通名词含义按场景处理 |
| `Ara Ara` | 餐厅专名／店员招呼 | 啊啦啊啦 | `deb26.rpy` 及相关地点文件 | 与 UI 一致，保留店名与招呼语的俏皮呼应 |
| `Cowabunga` / `Heroes in a half-shell` | 连续文化笑点 | 卡瓦邦嘎／身披半壳的英雄 | `deb27.rpy` | 前者的喊叫与 Debbie 复述必须一致，后者承接忍者神龟笑点 |
| Jenny 的 `perv` / `pervert` | 人物固定辱称 | 变态 | `jen01.rpy`、`jen04.rpy` 及后续 Jenny 文件 | 已处理文件统一；后续出现时按关系阶段复核整句语气，不机械全局替换 |
| Jenny 的 `loser` | 人物固定辱称 | 废柴 | `jen06.rpy` 至 `jen08.rpy` 及后续 Jenny 文件 | 已处理文件统一；只约束 Jenny 对 Anon 的辱称，不套用其他角色或普通名词用法 |
| `The Electro Clit` | 情趣玩具产品名 | 电击阴蒂棒 | `jen08.rpy` 及后续相关文件 | 与轻量版区分；产品名在同场复述时保持一致 |
| `Electro Clit Light` | 情趣玩具产品名 | 电击阴蒂棒轻量版 | `jen08.rpy` 及后续相关文件 | 原版缺货时出现的低功率版本 |
| `Pink` | 商店专名 | 粉色诱惑 | 商场情趣用品店相关文件 | 用户确认的意译；UI 与全仓引用同步，排除颜色、人物和频道名称 |
| `Sluttygram` | 成人照片订阅网站专名 | 保持 `Sluttygram` | 字节码提示、`jen05.rpy`、后续 Jenny 文件 | 保持英文拼写和大小写；已恢复“浪荡格莱姆”“偷情网”等错误汉化 |
| `peaches / my peaches` | Jenny 线连续成人双关 | 桃子／我的桃子 | `jen22.rpy` | Jenny 用水果掩饰成人直播；后续“汁水、完事、满脸、头发沾到”同时承接舔屄与高潮场景，必须保留桃子这一核心双关 |
| `little whipping boy` | Jenny 线关系动态 | 出气筒 | `jen23.rpy`、`jen_cam.rpy` | Anon 拒绝继续任 Jenny 发泄和使唤；两处保持一致，不按字面翻成“挨鞭子的男孩” |
| `Errmyyoony orhz unnng eeewww iiiiiting.` | 含混歌曲复述 | 人人嗯嗯都在功夫格斗 | `jen23.rpy` | Anon 被 Jenny 坐脸时哼唱《Kung Fu Fighting》第一句；两次复述必须完全一致 |
| `Ooh nunks errr, assst aahh iiiiitning.` | 含混歌曲复述 | 那些家伙快得就像闪电 | `jen23.rpy` | 同一首歌第二句；两次复述必须完全一致 |
| Jenny 的 `wimp` | 人物挖苦称呼 | 窝囊废 | `jen05.rpy` 及后续 Jenny 文件 | 本场两次保持一致；其他角色也使用普通词义，不建立无说话人范围的全仓替换 |
| `head cheerleader` | Jenny 过去身份 | 啦啦队长 | `jen24.rpy`、`viv04.rpy` 及后续复述 | Jenny 在大学当过啦啦队长；与普通 `cheerleader`“啦啦队员”区分 |
| `cheerleading uniform / cheer uniform` | Jenny 旧服装 | 啦啦队制服 | `jen24.rpy` 及后续相关文件 | 两种英文说法统一，不缩成含混的“制服” |
| `PING`（成人直播） | 打赏提示音 | 叮 | `jen18.rpy`、`jen21.rpy`、`jen24.rpy` 及后续直播文件 | 保留星号、停顿标签和重复次数，只统一拟声译法 |
| `CAMslut` | 成人直播平台专名 | 保持 `CAMslut` | `jen12.rpy`、`jen13.rpy` 及后续相关文件 | 严格保持大小写；与小写泛称 `camslut` 区分 |
| `camslut` | 成人直播从业者泛称 | 成人直播骚货 | `jen24.rpy` 及后续复述 | 小写不是平台名；按句法自然处理，本场为 Anon 自嘲 |
| `boyfriend`（非 `ex-boyfriend`） | 关系身份／调侃 | 男朋友 | `jen10.rpy`、`jen25.rpy` 及后续复述 | `jen25.rpy` 中只是 Jenny 为吓退跟踪狂临时冒认，Anon 随后借题调侃；固定核心译法但不擅自坐实恋爱关系 |
| `stalker` | 人物定性 | 跟踪狂 | `jen25.rpy`、`jen26.rpy` 及后续相关文件 | 指反复尾随、躲在树篱中用望远镜偷窥 Jenny 的人；与动作 `stalking`“跟踪”区分 |

| `gummy worms` | 重复零食名称 | 虫形软糖 | `jen26.rpy` | 邀约、确认约会和电影院购买时多次出现，保持同一名称 |
| `lovey-dovey bullshit` | Jenny 线恋爱排斥口吻 | 卿卿我我的屁话 | `jen27.rpy`、`jen_gfe.rpy` | Jenny 用粗俗语气贬低恋爱式亲密；两处已按关系阶段统一 |
| `girlfriend experience` | Jenny 线付费关系安排 | 女友体验 | `jen_gfe.rpy`（概念始于 `jen28.rpy`） | `jen28.rpy` 建立一晚五百美元的假女朋友服务，`jen_gfe.rpy` 正式命名；不得写成真实女友身份 |
| `Pals` | 虚构电视节目专名 | 《好友》 | `jen_gfe.rpy` | Jenny 与 Debbie 童年常看的老情景喜剧；两次提及保持一致，Matt、Courtney 等剧中人物姓名保持英文 |
| `gawked at` | Jenny 成人直播边界 | 被人围观 | `jen_cam.rpy` | Jenny 拒绝的是面对观众表演；与仍愿意私下让 Anon 舔屄形成对比 |

| `grandmother / nana / grandma` | Jenny 线母系亲属称谓 | 外婆 | `jen_baby.rpy` | Debbie 是 Jenny 的母亲，对 Jenny 的孩子必须按母系关系称“外婆”；不得译为“奶奶” |

| `life was flashing before my eyes` | Jenny 泳池溺水笑点 | 看见人生走马灯 | `jen_pool.rpy` | Anon 两次因被压入水中、接近溺水而看见人生走马灯；不是因高潮“爽死了” |
| `cannonball` | 裸泳跳水连续动作 | 炸弹入水 | `jen_pool.rpy` | Anon 的跳水喊声与 Jenny 后续复述保持一致 |
| `skinny dipping` | 裸泳活动 | 裸泳 | `deb23.rpy`、`jen_pool.rpy` | 指不穿泳衣游泳，两条剧情线保持同一核心译法 |

| `Wanna fool around?` / `You wanna fool around?` | 私人性邀约 | 亲热一下 | 8 处 / 5 个文件 | Jenny 线、`deb_sink.rpy` 与 `jud_stall.rpy` 已按完整场景统一；按句法使用“想不想／还想不想亲热一下” |
| `wowie waffles` / `Magnificent muffins` / `Holy honey buns` | Judith 的食物式感叹 | 哇哦，华夫饼！／妙极了，松饼！／老天，蜂蜜面包！ | `jud02.rpy`、`jud_stall.rpy` | 保留幼稚、押头韵又古怪的角色口癖，不抹平成普通感叹 |
| `Specs.` / `spectacles` | Judith 眼镜任务入口与物品称呼 | 眼镜 | `judith.rpy`、`specs_judith.rpy` | 菜单 `Specs.` 与储物柜中的私人备用眼镜均译“眼镜”，不按“规格”或“护目镜”处理 |
| `Bathroom fun.` | Judith 私下亲热任务入口 | 浴室亲热 | `judith.rpy`、`jud_stall.rpy` | `choice='stall'` 指向更衣室隔间亲热事件；菜单保持简短明确 |
| `faptic engine` / `Faptic Engine` | Tori／June 任务中的虚构触觉振动部件 | 触觉引擎 | `june.rpy`、`tori.rpy`、`tor03.rpy` | 菜单、询问、拆取和交付场景统一；后续完整通读相关文件时复核句法 |
| `key code` / `code`（Tori办公室门锁） | Tori 办公室电子密码锁的门禁信息 | 门禁密码 | `school_office2.rpy`、`tor01.rpy`、`note_tori.rpy` | 当前公共门锁提示统一为“门禁密码”；`tor01.rpy` 的旧译“钥匙密码／关键密码”待完整通读该文件时统一 |
| `Dress.`（Kassy／Cupid 菜单） | 女装店商品／任务话题 | 连衣裙 | `kassy.rpy` | 名词形式，指要找的裙装；不得译成动作“穿衣服” |
| `cafeteria duty` | Kevin 因科学课成绩不佳受到的食堂处罚 | 食堂帮工 | `ano01.rpy`、`kevin.rpy` | 固定差事称呼；不漂移为“食堂值日” |
| `master key` | 校内门锁／储物柜通用钥匙 | 万能钥匙 | `ano01.rpy`、`key_school.rpy`、`school_hall1.rpy`、`school_locker.rpy` 及相关文件 | 保留“万能”功能含义；不得漂移为“主钥匙”；斜体 `borrowed`／`borrow` 保留 Anon 对擅自拿钥匙的自我淡化 |
| `Mrs. [saga.cast.ursula.clan]` | Ursula 的姓氏敬称 | `[saga.cast.ursula.clan]夫人` | `school_office1.rpy` 及 Ursula 相关文件 | 保留变量并采用中文“姓氏＋夫人”语序；学生直接服从她时的 `ma'am` 按身份译“校长” |
| `Summerville College` | 学校正式名称 | 夏日学院 | `+prologue.rpy`、`school_pa.rpy` 及学校相关文件 | 沿用项目既有译名，不漂移为“夏日大学” |
| `Conda Hivic` | 校内广播中的虚构车型 | 保持 `Conda Hivic` | `school_pa.rpy` | 影射 Honda Civic；英文专名不音译，两次重复播报保持完全一致 |
| `main office`（学校） | 校务与失物处理地点 | 校务办公室 | `school_pa.rpy` 及学校相关文件 | 与 Ursula 的私人校长办公室区分 |
| `Friend-Uhh` / `Friend-uhh` | Konty 对 Anon 的错误称号 | 按原文保持 `Friend-Uhh` / `Friend-uhh` | `konty.rpy`、`tor01.rpy` | 来自启动时误把 `Uhh...` 识别成称号；大小写逐句服从英文原文，`tor01.rpy` 旧译待完整通读时统一 |
| `K-bot` | Anon 给 Konty 取的昵称 | `K-bot` | `konty.rpy`、`tor01.rpy` | 保持英文、连字符和大小写，不写成 `KBot` 或中文名 |
| `Processing laughter...` | Konty 模拟笑声的系统提示 | 正在处理笑声…… | `konty.rpy`、`tor01.rpy` | 与下一句机械假笑构成连续笑点；`tor01.rpy` 待完整通读时统一 |
| `Ack ack ack!` | Konty 的机械假笑 | 啊咔、啊咔、啊咔！ | `konty.rpy`、`tor01.rpy` | 不按正常人类笑声抹平成“哈哈哈”；保留生硬机器感 |
| `BEEP BOOP!` | Konty 机器人提示音 | 哔——啵！ | `konty.rpy`、`tor01.rpy` | 与 Anon 反向回应的 `BOOP BEEP!` 区分并保持顺序 |
| `BOOP BEEP!` | Anon 模仿机器人语的反向回应 | 啵——哔！ | `konty.rpy` | 必须与前一句 `BEEP BOOP!` 形成音节倒序 |

| `Princess [saga.cast.jenny]` | Jenny 支配角色称谓 | 公主[saga.cast.jenny] | 9 处 / 5 个文件 | `jen21.rpy`、`jen24.rpy`、`jen_pool.rpy`、`jen_shower.rpy`、`jen_tv.rpy` 已统一；姓名变量保持原样，内部复述使用中文双引号 |

| `sex goddess` | Jenny 成人角色称谓 | 性爱女神 | `jenny_laptop.rpy`、`jen20.rpy`、`jen26.rpy`、`jen_cam.rpy`、`jen_baby.rpy` 等 | 从早期个人成人直播到后续共同直播、性交自夸和孕期表演均保持同一角色称谓 |
| `camgirl` | 成人直播从业者 | 成人女主播 | `jen15.rpy`、`jenny.rpy` | 指女性成人直播从业者；与平台专名 `CAMslut` 及泛称 `camslut` 区分 |
| `Boys' Locker Room` / `boys' locker room` / `guys' locker room` | 学校地点／普通指代 | 男生更衣室 | `ano01.rpy`、`jud01.rpy` 及相关文件 | 地点名称与普通指代统一；`tor05.rpy` 的旧译“男更衣室”留待完整通读时复核 |
| `Girls' Locker Room` / `girls' locker room` | 学校地点／普通指代 | 女生更衣室 | `ano01.rpy`、`jud02.rpy`、`school_girls.rpy` 及相关文件 | 地点名称与普通指代统一；不缩写为“女更衣室”；`school_girls.rpy` 的 `this locker room` 按场景明确为女生更衣室 |
| `white boy` | Val/Camila 对 Anon 的种族化辱称 | 白人小子 | `jud02.rpy` | 不译成表示外貌讨好的“小白脸”；`viv02.rpy` 已统一 |

| `sugar`（Melody 对 Anon） | Melody 专属亲昵称呼 | 甜心 | `mel01-06.rpy`、`mel_office.rpy`、`melody.rpy` | `mel_office.rpy` 已统一；旧文件中的“亲爱的”等译法待随完整剧情逐文件统一，不在未通读前批量替换 |
| `skin flute` | Melody 的长笛／口交双关 | 肉箫 | `mel_office.rpy` | 与 `play/blow/master an instrument/private performance` 连续成组处理 |
| `finale`（Melody 线） | 才艺表演或私人舞蹈的最后环节 | 压轴（按句法扩展） | `mel02.rpy`、`mel03.rpy`、`mel06.rpy`、`mel_office.rpy` | 使用“压轴环节／压轴戏／压轴好戏”等自然句法；不译成普通“结局” |
| `pom-pom` / `pom-poms` | 啦啦队手持道具 | 啦啦球 | `roxxy.rpy`、`viv04.rpy`、`res/meta/prop.rpy`、`res/meta/step.rpy` | `roxxy.rpy` 与 `viv04.rpy` 已按完整场景统一；资源文件待完整通读时复核，不漂移为“拉拉球／绒球／彩球” |

| `{i}*Hurk*{/i}` | 重复受击／受压闷哼 | `{i}*呃唔*{/i}` | `ano01.rpy`、`sam_stall.rpy` | 两处统一；保留 `{i}` 标签与星号，不因具体受击物不同改成咳嗽或惨叫 |

| `utility closet` | 学校设施名称 | 杂物间 | `mel05.rpy`、`school_boiler.rpy` | 两处统一；指学校走廊内的小型储物／设备房，不译成售卖杂货的“杂货间” |

| `bouncing ball` / `exercise ball`（Tammy） | 带假阳具的成人健身道具 | 健身球 | `tammy_bed1_scope.rpy`、`jen23.rpy` | 两处指同一件道具；不得在“弹力球／健身球”之间漂移 |

| `shovel`（Diane 菜园任务） | 剧情道具／园艺工具 | 铲子 | 19 处 / 5 个文件 | `tool_shovel.rpy`、`dia01.rpy`、`diane.rpy` 及相关资源文本当前统一；指替换 Diane 断掉旧铲子的完整园艺工具，不漂移为“铁锹” |

| Anon 父亲的 `Dad's old drill` / `old drill of Dad's` | 剧情道具／父亲遗物 | 旧电钻 | 6 处 / 3 个文件 | `tool_drill.rpy` 已统一；`bar04.rpy`、`mel01.rpy` 待随完整文件复核，完整工具不得误译成“钻头” |

## 当前跨文件复查队列

- `Dad's old drill` / `old drill of Dad's`：`tool_drill.rpy` 已统一为“旧电钻”；`bar04.rpy`、`mel01.rpy` 中相关旧译待随完整剧情复核，禁止把完整电钻写成“钻头”。

- `champ`：`ano15.rpy`、`ano16.rpy`、`mar02.rpy`、`mar_baby.rpy`、`mar_dark.rpy`、`pizza_boxes.rpy`、`ton_baby.rpy` 与 `tony.rpy` 已统一；当前已复核文件中无旧译残留。
- `babyface`：已处理的 `ano09.rpy`、`ano11.rpy`、`ano13.rpy` 统一为“小帅哥”；其余 Tina 剧情文件中的旧译待逐文件复核。非称呼用法按具体指代自然翻译，不机械使用“娃娃脸”。
- `protégé`：`ano11.rpy` 已统一为“徒弟”；`tin_vault.rpy` 仍有 1 处旧译待复核。
- `cannoli`：`ano10.rpy`、`mar_cook.rpy`、`mar_baby.rpy`、`mar_dark.rpy` 已统一为“意式奶油甜馅卷”；`Holy cannoli` 属感叹语，不机械替换。
- `little bunny`：`deb18.rpy` 3 处待在完整剧情中复核，核心译法保持“小兔子”。
- `godfather`：`ano16.rpy` 与 `mar_baby.rpy` 已统一为“教父”，并保留与 Tony 黑帮背景相关的《教父》笑点。
- `bowl cut`：Josie 对 Anon 的固定挖苦称呼统一为“锅盖头”，截断形式译为“锅盖——”；`jos01.rpy`、`jos_trade.rpy`、`josie.rpy` 与 `deb13.rpy` 的当前命中均已按完整场景复核。
- `perv/pervert`：Jenny 对 Anon 的固定辱称核心译为“变态”；`jen01.rpy`、`jen04.rpy` 至 `jen08.rpy` 已随完整剧情统一，后续文件继续按关系阶段复核整句语气。
- `Wanna fool around? / You wanna fool around?`：核心性邀约译法为“亲热一下”；Jenny 线、`deb_sink.rpy` 与 `jud_stall.rpy` 已按完整场景统一，后续仍按关系阶段复核整句。
- `white boy`：Val/Camila 对 Anon 的种族化辱称统一译为“白人小子”；`jud02.rpy` 与 `viv02.rpy` 已完成复核。
- `sugar`（Melody）：核心译法定为“甜心”；`mel_office.rpy` 已统一，`mel01-06.rpy` 与 `melody.rpy` 的旧译待随完整剧情逐文件复核。
- `finale`（Melody线）：核心使用“压轴”；`mel03.rpy` 的旧译“终曲”待完整通读时统一。
- `pom-poms`：核心译法定为“啦啦球”；`roxxy.rpy` 已修复，`viv04.rpy`、`res/meta/prop.rpy`、`res/meta/step.rpy` 中的“啦啦队彩球／彩球／拉拉球／绒球”等旧译待逐文件完整复核。
- 上述条目只登记，不在未通读完整文件前批量替换；进入对应文件时结合关系阶段完成统一。

## 审计命令

```powershell
# 检查全部已登记条目，只显示不一致项
python -X utf8 tools/audit_recurring_terms.py

# 查看某个条目的全部英文—中文对应
python -X utf8 tools/audit_recurring_terms.py --term vehicle_blue_falcon --show-all

# 临时搜索刚发现的重复短语
python -X utf8 tools/audit_recurring_terms.py --query "Blue Falcon"

# 每批必须运行：只检查本批修改过的 Ren'Py 文件，并在不一致时返回失败
python -X utf8 tools/audit_recurring_terms.py --changed --fail-on-mismatch
```
- `TPS report(s)`：Yoshi 与 Josie 关于车行文书工作的重复笑点统一为“TPS报告”，与后面的普通费用报表区分。
- `T-straps`：Josie 在半价促销中反复寻找的露趾鞋款统一为“T字带凉鞋”。
- `Hattori Hanzō`：人物姓名保持英文原状，不翻译为“服部半藏”。
- `Mini Vulva`：小型汽车的色情双关车型名统一为“迷你外阴”，三处保持一致。
- `SL-700 Crotch Rocket`：纯电动踏板车车型名统一为“SL-700 胯下火箭”，保留 `crotch rocket` 的双关。
- `poor boy`：Yoo 针对 Anon 贫穷身份的固定辱称统一为“穷小子”，不写成表示同情的“可怜的小子”。
- `Employee of the month`／`Emproyee of month`：统一为“月度最佳员工”；原文拼写差异只体现 Yoo 的破碎英语，不另造中文错字。
| `Brazilian Bum Bum` / `Brazilian Bum Bum Cream` | Debbie 线润肤露产品名 | 巴西Bum Bum／巴西Bum Bum润肤霜 | `deb06.rpy`、`deb07.rpy`、`deb_mall.rpy`、`misc_lotion.rpy` | 保留产品名中的英文 `Bum Bum`；省略 `Cream` 时不擅自补产品类型，也不得直译成“巴西翘臀” |
| `horny toad` / `horny toad extract` | Tori 线血清任务材料 | 发情蟾蜍／发情蟾蜍提取物 | `tor05.rpy`、`misc_toad.rpy` | `horny` 与繁殖季相呼应，统一保留“发情”笑点；普通 `toad` 仍译“蟾蜍”，不得漂移为“角蟾／角蛙／色蛤蟆／发情的蛤蟆” |
| `vegetable stock` | Tori 线血清任务基底 | 蔬菜高汤 | `tor05.rpy`、`vee.rpy` | 作为温和血清基底及 Consum-R 购物选项统一，不漂移为“蔬菜汤底”；`chicken stock` 暂按既有剧情译“鸡汤”，不在未通读其他文件前批量改动 |
| `linens`（教堂艺术任务） | 画布材料任务名 | 亚麻布／白色亚麻布 | `ang.rpy`、`bar05.rpy` | `ang.rpy` 菜单使用“亚麻布”；`bar05.rpy` 完整场景需统一“白色亚麻布”，并说明 Angela 实际交付旧洗礼袍，不漂移为普通“床单” |
| `mon bel homme` | Viv 对 Anon 的法语昵称 | 我的帅哥 | `viv01-05.rpy`、`viv_office.rpy` | `viv01-05.rpy` 与 `viv_office.rpy` 已按完整场景统一；保持成熟、主动的法式调情口吻 |
| `special reward` | Viv 对一对一辅导奖励的递进承诺 | 特殊奖励 | `viv01-05.rpy` | `viv01.rpy` 为暧昧承诺，`viv02.rpy` 兑现为摸胸，`viv03.rpy` 兑现为法式接吻，`viv04.rpy` 再次许诺；`viv05.rpy` 最终兑现为首次性交，并解锁后续重复关系 |
| French kiss / French kissing | Viv 第三次辅导中的接吻教学与奖励 | 法式接吻 | `viv03.rpy` | 保持接吻行为的标准称呼，不漂移为额外增强性意味的“法式热吻” |

| `slab of clay` | Barbara 美术课材料 | 一块陶土 | `bar01.rpy` 及后续美术课文件 | 指学生拿来塑形的整块陶土，不漂移为“黏土板／泥板” |

| `art pad` / `artpad` | Barbara 美术线工具 | 画板 | `bar02.rpy` 及后续美术课文件 | 指夹纸绘画用的便携画板，不在“画板／画册”之间漂移 |

| `cutie pie`（Barbara 对 Mia） | 角色亲昵称呼 | 小可爱 | `bar02.rpy` 及 Barbara 美术线后续文件 | 保持 Barbara 热情、欣赏又略带调情的口吻；不提前建立稳定成人关系 |

| `collage` / `collages` | Barbara 美术线作品类型 | 拼贴画 | `bar03.rpy`、`barb.rpy` 及后续美术课文件 | Anon 将 `collage` 听成 `college` 时用“拼贴画／大学”保留误听笑点；普通任务名固定译“拼贴画” |

| `easel` / `easels` | 美术课绘画设备 | 画架 | `bar04.rpy` 及美术线 | 旧画架与 Anon 制作的新画架统一，不漂移为“支架” |

## 本轮新增全仓审计项

| ID | 英文匹配 | 统一中文 | 适用范围与备注 |
|---|---|---|---|
| cuntech_name | Cuntech | Cuntech | 虚构公司专名保持英文原状，不音译、不汉化。 |
| talent_show | talent show | 才艺表演 | 学校活动名称全仓统一。 |
| jenny_boyfriend | boyfriend；成对语境中的 boyfriend and girlfriend | 男朋友；男女朋友 | 单独关系标签使用“男朋友”；成对表达允许自然译为“男女朋友”，避免破坏中文成对称谓。 |
| jenny_cheer_uniform | cheer uniform / cheerleading uniform | 啦啦队制服 | 资源名和剧情道具统一使用“啦啦队制服”。 |
| vehicle_mini_vulva | Mini Vulva key | 迷你外阴钥匙 | 保留道具的“钥匙”功能，不简化为仅“迷你外阴”。 |
| vehicle_crotch_rocket | SL-700 Crotch Rocket key | SL-700 胯下火箭钥匙 | 保留车型编号和钥匙功能，统一双关译法。 |

## 补充字符串统一项

| ?? | 类别 | 统一中文 | 适用范围与备注 |
|---|---|---|---|
| camming career | 成人直播 | 直播事业 | Jenny 直播副业相关内心独白。 |
| camshow / camshows | 成人直播 | 成人直播 | 任务名和直播场景统一；不使用“摄像头表演”。 |
| on stream | 成人直播 | 在直播中 | 直播进行时的固定表达。 |
| chat（直播语境） | 成人直播 | 直播间观众 | 不直译为“聊天”。 |
| deprive ... of attention | 任务条件 | 冷落…… | 表示暂时不理会角色。 |
| foul play | 调查 | 人为犯罪／他杀迹象 | 调查死亡原因时使用。 |
| Outlood Express | 专名 | Outlood快递 | 保留恶搞专名的英文部分。 |
| cookie jar | UI | 角色图鉴 | 解锁角色变体或场景。 |
| Third Quarter | 月相 | 下弦月 | 与 `First Quarter`“上弦月”配对。 |
| Waning Crescent / Waxing Crescent | 月相 | 残月／娥眉月 | 月相 UI 固定译法。 |
