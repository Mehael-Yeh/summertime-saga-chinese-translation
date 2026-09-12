# 术语与称谓规范

更新时间：2026-09-12

## 角色姓名（强制）

- 不建立中文音译姓名表。英文姓名、姓氏、全名和作为人物专名使用的昵称按原文原样保留。
- `babyface`、`dollface`、`champ` 这类本身带有明确语义、用于称呼对方的描述性亲昵称呼，不视为人物专名；应结合人物关系建立稳定中文，不能因形式像昵称就机械保留英文。
- 已确认必须恢复的形式：`Anon`（剧情对话、叙述和姓名字段不得写“匿名/你”）、`Tony`（不得写“托尼”）、`Tammy`（不得写“塔米”）、`Kevin`（不得写“凯文”）、`Judith`（不得写“朱迪丝/朱迪思”）。
- **UI 玩家占位例外**：手机任务提示等界面文本若把字面 `Anon` 当作玩家占位，并因此绕过玩家自定义姓名，可按界面视角译为“你”；该例外不得扩展到剧情对话、叙述或普通姓名。
- 原文使用变量时保留变量，例如 `[saga.cast.debbie]`、`[saga.cast.jenny]`。不得把字面姓名改成变量，也不得把变量改成字面姓名。
- 身份称谓可翻译，姓名部分不变：`Bissette老师`、`Johnson太太`、`Bridget教练`、`Smith校长`、`Harris医生`。

## 重复术语复查机制

- 同一英文名词、组合词、称呼或固定表达在短距离内出现 2 次及以上时，先视为潜在专名、人物口癖或专属称呼，必须执行全仓复查。
- 人工记录见 `recurring_terms.md`，机器可读规则见 `recurring_terms.json`；使用 `tools/audit_recurring_terms.py` 查询全仓对应和检查本批一致性。
- 确认稳定译法后才写入本术语表。未通读的跨文件命中只加入复查队列，不进行无上下文批量替换。

## 地名与 UI 一致性（强制）

- 定译须兼顾信达雅：先确认地点功能、品牌语气与双关，再选自然且易辨认的中文店名；UI 是一致性基准，不是禁止纠正旧译。UI 旧译不合设定时，须与全仓引用同步修改。
- `Pink` 采用用户确认的“粉色诱惑”，而非颜色直译或单纯堆叠类别词。`Retro Strike` 位于街机与保龄球区域，`Strike` 按保龄球术语译“全中”，整体为“复古全中”。“丰满星球”保留健身品牌的身材谐趣，“甜蜜纹身”保留纹身店风格，“传说影院”明确影院身份。没有足够剧情证据的品牌不凭字面臆造背景。

- 地名基准是 `tl/zh_hans/base_box/sets.rpy` 中实际的 `old` / `new` 对；同时检查 `tl/zh_hans/res/meta/sets.rpy` 的补充条目，不能只看其中一个文件。
- 对话、旁白、选项、任务提示、物品说明和 `bytecode_strings.rpy` 中提到同一地点时，必须沿用 UI 的核心译名。即使只出现一次，也要核对；人物姓名保留英文的规则不适用于店名、地名。
- 可以按句意增加“店／商店／餐厅”等类别词，例如“宇宙漫画店”“丘比特商店”；不得换用另一套音译或意译，也不得一处保留英文、一处译中文。原文只说“那家店／商场／山上”时可保留自然指代，无须强行补全名称。
- `Raven Hill` 固定为“渡鸦山”，不得使用“鸦山／鸦丘／渡鸦丘”等旧译。当前源码的 11 处完整名称已一致，本次未发现需要改写的旧译。
- 先按英文原文定位，再核对前后文和中文旧译；只改目标译文，不改 `old`、英文注释、标签、变量、资源路径或程序标识符。店名 `Pink` 为“粉色诱惑”，不得误改颜色、人物 `Pink Cyclone`、频道 `Pink Channel` 或 `{pen=pink}`；`Ara Ara` 在欢迎词中也是餐厅名称，统一“啊啦啊啦”。
- 新增或调整 UI 地名时，同步复查所有文本并更新本表、`recurring_terms.md` 和 `recurring_terms.json`，运行全仓 `python -X utf8 tools/audit_recurring_terms.py --fail-on-mismatch`。机器规则用于筛查，歧义词和普通场所词仍需人工确认指代。

| UI 英文名 | 统一核心译名 |
|---|---|
| Retro Strike | 复古全中 |
| Saga Financial | 传说金融 |
| Rusty Angus | 拉斯蒂安格斯 |
| Sandbar Island | 沙洲岛 |
| Cosmic Cumics | 宇宙漫画 |
| Glazies | 格拉齐斯 |
| Cupid | 丘比特 |
| Planet Thiccness | 丰满星球 |
| Raven Hill | 渡鸦山 |
| Hillside Mall | 希尔赛德商场 |
| Tony's Pizza | Tony披萨店 |
| Summerville College | 夏日学院 |
| Consum-R | Consum-R |
| Ara Ara | 啊啦啊啦 |
| Sugar Tats | 甜蜜纹身 |
| Pink | 粉色诱惑 |
| CineSaga / CineSaga Theater | 传说影院 |
| Beachside Apartments | 海滨公寓 |

## 当前已确认地点与活动

| 英文 | 统一中文 | 说明 |
|---|---|---|
| Summerville | 夏日镇 | 当前项目既有译法；后续逐文件复核一致性 |
| Summerville College | 夏日学院 | 当前项目既有译法；学校语境统一使用 |
| Tony’s Pizza / Tony's Pizza | Tony披萨店 | Tony 保持英文，不得写“托尼披萨店” |
| Sorority Ball | 姐妹会舞会 | 序章目标文本采用此译法 |
| Boys' Locker Room / boys' locker room / guys' locker room | 男生更衣室 | 学校地点与普通指代统一；不缩写为“男更衣室” |
| Girls' Locker Room / girls' locker room | 女生更衣室 | 学校地点与普通指代统一；不缩写为“女更衣室”；`ano01.rpy` 交代水管爆裂后关闭维修，`school_girls.rpy` 展示地板破洞 |
| `changing stall` / `changing room` / `stall`（服装店语境） | 更衣隔间 | 商场服装店内单独换衣的小隔间；`ten_stall.rpy` 虽使用 `changing room`，但画面仍是单独隔间，因此按具体场景译“更衣隔间”；与厕所／浴室隔间及售货用 `booth`“摊位”区分 |
| `security gate`（店铺门面） | 防盗门 | `sushi_shop.rpy` 中 Ara Ara 清晨闭店时挡住入口的竹制防盗门；指防盗设施，不译成安全检查用的“安全门” |
| `bouncing ball` / `exercise ball`（Tammy 场景） | 健身球 | `tammy_bed1_scope.rpy` 与 `jen23.rpy` 指同一件带假阳具的成人健身球道具；不得在“弹力球／健身球”之间漂移 |
| `blinds`（住宅窗户） | 百叶窗 | Tammy／Erik 家的望远镜观察场景中指可开合遮挡视线的百叶窗；不泛化成布质“窗帘” |
| `dildo`（Tammy 健身球） | 假阳具 | 直接指安装在健身球上的成人用品；不弱化成含混的“玩具” |
| white boy | 白人小子 | Val/Camila 针对 Anon 肤色的种族化辱称；不是讨好外貌的“小白脸” |

## 系统与界面文本

| 英文 | 统一中文 |
|---|---|
| save | 存档 |
| load | 读档 |
| settings | 设置 |
| inventory | 物品栏 |
| satchel icon | 背包图标 |
| quest | 任务 |
| morning | 早晨（自然口语中可用“早上”） |
| afternoon | 下午 |
| evening | 傍晚 |
| night | 夜晚 |
| moderate affection points +[...] | 好感度中幅提升 +[...] |

## 关系与亲属称谓

- 英文原文使用 `Mom`、`Dad`、`Sis`、`Aunt` 等明确关系称谓时，可按角色口吻翻译。
- 英文原文使用姓名时，不得替换成关系称谓。
- 同一角色对另一角色的称呼变化必须有剧情依据，并记录在 `characters.md` 或对应剧情线档案中。
- `my man`（Roxxy 后期对 Anon）统一译为“我男人”，体现已经确立亲密关系后的自信、占有式恋爱口吻；不得提前用于早期敌对或普通同学阶段。

## 成人内容用词层级

- 原文委婉则保持委婉；原文明确则明确；原文粗俗则保留粗俗感。
- `fuck`、`cock`、`pussy`、`dick` 等不得脱离场景机械统一；需按愤怒、强调、调情、性行为、辱骂等功能选择中文。
- “操/肏/鸡巴/屄/骚货”等词没有自动禁用规则，但不得为了刺激擅自升级原文。女性角色明确要求与对方发生性行为，且中文使用“操某人／操屄”一类动作结构时，优先写作“肏”；感叹、惊讶、生气和辱骂中的“操”不变。双关语按语境可使用“干”。
- 呻吟和喘息需按惊讶、疼痛、快感、迟疑、愤怒等情绪区分，不让所有角色使用同一套拟声词。

### 日常护理、私人物品与自慰表达

| 英文 | 统一中文 | 说明 |
|---|---|---|
| `lotion` | 润肤露 | 日常身体护理语境；具体产品为膏霜质地时可按产品名写“润肤霜”；`tammy_bed2_scope.rpy` 中 Erik 关上百叶窗后“又在用润肤露”是自慰暗示，需保留原文委婉说法，不直接增译为“自慰” |
| `Brazilian Bum Bum` / `Brazilian Bum Bum Cream` | 巴西Bum Bum／巴西Bum Bum润肤霜 | 产品名省略 `Cream` 时保留“巴西Bum Bum”，完整名称按膏霜质地补“润肤霜”；不得直译成“巴西翘臀” |
| `solid`（电影暧昧场景） | 挺得住 | 同时保留“能承受情色画面”和勃起坚挺的双关；后句可用“应付得来”解释表层含义 |
| `masturbation` / `masturbate` | 自慰 | 直接、中性地表达行为，不净化为“解决需求”等含糊说法 |
| `panties` / `underwear` | 内裤 | 按单复数和指代自然组织中文；`mom panties` 可译“妈妈穿的内裤”，不使用生硬的“妈妈内裤” |
| `ma’am`（Anon 对 Debbie） | 夫人 | 体现房东与房客之间带亲近感的礼貌；不得在“夫人”“女士”“长官”之间漂移 |
| `landlady`（色情片房东房客设定） | 房东太太 | `deb16.rpy` 色情片及其现实映照中的固定称呼；不同于 Anon 对 Debbie 的 `ma’am`“夫人” |
| `British Baking` | 英国烘焙节目 | 剧中电视节目；同一场景反复出现时保持一致，不擅自补成现实节目全名 |
| `banoffee pie` | 太妃香蕉派 | 香蕉、打发奶油、焦糖酱和饼干底组成的甜点 |
| `That's my good boy!`（后期成人语境） | 这才乖嘛！ | Debbie 的照顾者式亲昵称呼进入成人场景后的表达；不译成母子关系 |
| `Scouts honor` | 童子军发誓 | 年轻人口吻的郑重保证，不直译成生硬的“童子军荣誉担保” |
| `good boy`（Debbie 内心照顾者语境） | 很乖 | 保留 Debbie 的照顾者习惯，但不据此把 Anon 写成其儿子 |
| `interstellar hitchhiker`（毛巾彩蛋） | 星际搭车客 | `misc_towel.rpy` 化用《银河系漫游指南》的毛巾经典句式；保留“搭车客”以承接 `hitchhiker`，并用“最最有用”体现 `most massively useful` 的夸张卖弄语气 |

## Debbie 线商场专名与调侃

| 英文 | 统一中文 | 说明 |
|---|---|---|
| Cupid | 丘比特 | 商场女装精品店，以爱神意象呼应服饰与浪漫；与 UI 一致 |
| Raven Hill | 渡鸦山 | 俯瞰小镇的偏僻山丘；Debbie 与 Anon 私下谈话地点 |
| Sugar Basin | 糖谷 | Debbie 与 Diane 青春期共同度过夏天、裸泳并发生亲密互动的地点 |
| FunBiz Pizzeria Pub | FunBiz披萨酒吧 | Debbie 十六岁时第一份工作的地点；`FunBiz` 保持英文 |
| Billy-bear | Billy-bear | FunBiz 舞台吉祥物名称，保持英文拼写和连字符 |
| Ara Ara | 啊啦啊啦 | 用户确认译名；保留日式音韵、重复节奏和俏皮招呼语的呼应。UI／招呼用“啊啦啊啦”，指路可称“啊啦啊啦餐厅”，不另造店名 |
| `hospitality stick in her ass`（Titomi） | 待客时屁股里跟夹了根棍子似的 | Titomi 用粗俗比喻嘲笑 Hana 服务过度正式、姿态僵硬；Anon 随后把“棍子”当真。不得译成真实存在的普通“接待棒” |
| `wear a helmet`（Titomi 对 Anon） | 还得戴防撞头盔 | 暗讽 Anon 迟钝、可能需要保护性头盔，不是普通交通安全询问 |
| `Cowabunga` | 卡瓦邦嘎 | Anon 裸体跳入泳池时引用忍者神龟口号；Debbie 随后复述时必须保持同一译法 |
| `Heroes in a half-shell` | 身披半壳的英雄 | 承接 `Cowabunga` 的忍者神龟主题歌词笑点 |
| `stud`（Diane 称呼 Anon） | 帅哥 | Diane 的大胆调侃称呼，不保留英文，也不机械套用于普通“种马”含义 |
| `nyotaimori` / body sushi | 女体盛／人体寿司 | 菜名用“女体盛”，解释其形式时用“人体寿司”；承载食物的人可按演出称“托盘” |
| Rock-a-Billy Pants Explosion | Rock-a-Billy Pants Explosion | FunBiz 的拟人动物乐队名称，保持英文原名 |
| Casanova（Kassy 调侃 Anon） | 情圣 | 泛称式调侃，不使用中文音译“卡萨诺瓦” |

## 怀孕与育儿术语

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `little one` / `little guy` / `little ones`（婴儿） | 小家伙／小家伙们 | 指新生儿时不得译“娃娃脸”；女孩可按语境译“小姑娘” |
| `pregnancy cravings` | 孕期怪口味／孕期口味 | 指怀孕造成的特殊饮食欲望，不机械译成笼统的“孕期反应” |
| `daycare` | 托儿所 | 指婴幼儿日间照护机构 |
| `nipple stimulation` | 刺激乳头 | 产后哺乳与成人双关并存，不弱化或净化 |
| `sweetie`（母婴连续双关） | 宝贝／大宝贝／小宝贝 | Debbie 同时称呼 Anon 与孩子时用于区分；普通对 Anon 的称呼仍通常译“亲爱的” |

## Ren’Py 特殊内容

- `[变量]`、`{标签}`、`%(变量)s`、`%s`、`%d`、转义字符和文本标签必须与英文源字符串保持同一集合和拼写。
- `{dom=...}`、`{sub=...}` 是自定义显示标签：标签名 `dom`/`sub` 必须保留，等号后的内容会显示给玩家，必须汉化。当前统一写作 `{dom=强势}`、`{sub=顺从}`。
- 不得把内心独白的普通圆括号改成方括号；Ren’Py 会把 `[...]` 识别为插值表达式。
- 台词内引述优先使用中文弯引号 `“……”`，避免 `「……」`；不得把外层 Ren’Py 字符串的 ASCII 双引号误改进文本。

## 学校与开局主线术语

| 英文 | 统一中文 | 说明 |
|---|---|---|
| Athletics class | 体育课 | 不机械译作“田径课”；具体赛事另行区分 |
| locker combination | 储物柜密码 | `combination` 在该场景指密码组合 |
| locker（学校走廊） | 储物柜 | 学生存放物品的带锁柜子；`school_locker.rpy` 中 Anon 会用万能钥匙偷翻，不译成更衣室 |
| master key | 万能钥匙 | 可打开校内门锁／储物柜；`key_school.rpy`、`school_hall1.rpy` 与 `school_locker.rpy` 中相关念头都承接 Annie 提供的线索；`borrow` 是把未经允许拿走钥匙自我淡化成“借用”，不代表正规借用 |
| `Mrs. [saga.cast.ursula.clan]` | `[saga.cast.ursula.clan]夫人` | 保留姓氏变量；这是姓氏加敬称，不把变量挪到“夫人”之后，也不擅自改写姓名 |
| `ma'am`（Anon 对 Ursula） | 校长 | 按 Ursula 的校长身份和学生服从语境处理；与对其他成年女性的 `ma'am` 区分 |
| `teachers' lounge` | 教师休息室 | 校内教职员工使用的休息空间；与 `main office`“校务办公室”、Ursula 的私人校长办公室区分 |
| Student Union President | 学生会主席 | Annie 身份 |
| hallway monitor | 走廊风纪委员 | Annie 身份；不要译成成人社会职务 |
| hall monitoring duty | 走廊巡查／巡查走廊 | `annie.rpy` 中 Annie 当下正在执行的职责；按动作自然翻译，不写成僵硬的“走廊监控值班” |
| cafeteria duty | 食堂帮工 | Kevin 因科学课成绩不佳受罚的固定差事；不译成普通轮值“食堂值日” |
| `sucks dick` / `not the cool kind`（Kevin 食堂双关） | 烂透了，简直像在含鸡巴／还不是让人爽的那种 | 前句同时使用“很糟”和口交字面义，后句继续暗示“爽的含法”；不得只译成普通“恶心／糟糕”而切断笑点 |
| tutoring sessions / private / one-on-one tutoring | 课后辅导／一对一辅导 | Viv 的普通课程入口菜单统一写“课后辅导”；强调私人教学时写“一对一辅导”。性关系解锁后带斜体的 `{i}tutoring{/i}` 是性爱双关，按语境写 `{i}补课{/i}`，不能还原成纯学业含义 |
| `mon bel homme`（Viv 对 Anon） | 我的帅哥 | Viv 逐步升温后的法语昵称；保持成熟调情口吻，不写成生硬的“我的俊男／我英俊的男人” |
| `special reward`（Viv 线） | 特殊奖励 | Viv 从首次一对一辅导开始给出的递进暧昧承诺：`viv02.rpy` 兑现为袒胸摸胸，`viv03.rpy` 兑现为法式接吻，`viv04.rpy` 再次许诺，最终在 `viv05.rpy` 通过办公室饮酒和首次性交完整兑现，并解锁后续重复亲密关系 |
| French kiss / French kissing | 法式接吻 | `viv03.rpy` 中 Viv 以法语和浪漫诗为由推进的接吻教学／奖励；不用“法式热吻”制造额外强度 |
| French lovemaking | 法国人是怎么做爱的／法国人的做爱方式 | `viv05.rpy` 中 Viv 借教师身份包装性交教学的双关；台词按句法自然展开，不弱化为普通恋爱或接吻 |
| `mon petit lapin`（Viv 对 Anon） | 我的小兔子 | `viv02.rpy` 起出现的法语昵称；既是亲昵称呼，也借 `lapin` 暗指 Anon 的勃起，译文需保留“小兔子”的双关承接 |
| French-to-English dictionary / French dictionary | 法英词典 | `viv01.rpy` 的任务物品；按具体缺页方向可写“法译英部分”，其余叙述统一简写“法英词典” |
| `PC LOAD LETTER` | `PC LOAD LETTER` | 复印机界面错误信息及《Office Space》式笑点，保留英文大写，不直译成“PC装信纸”；角色复述时也保持原文 |
| Muay Thai | 泰拳 | `kickboxing` 另译“踢拳” |
| GPA | GPA | 保留英文缩写 |
| Whorecraft | Whorecraft | 游戏内作品名，暂保留英文 |
| Consum-R | Consum-R | 商场店名，保留原拼写和连字符 |
| `vegetable stock` | 蔬菜高汤 | Tori 血清任务使用的温和基底；`tor05.rpy` 与 `vee.rpy` 的任务对话和菜单统一，不漂移为“蔬菜汤底” |
| `aisle`（Consum-R） | 货架通道／通道 | 商店货架之间的通道；欢迎口号按中文句法写“转过一条通道就能找到”，具体编号写“12号通道”，不把店名擅自补成“超市” |

## `ano01.rpy` 游戏双关

- `carrot hole` → “胡萝卜洞”。
- `bunny hole` → “兔子洞”。
- `bunny bum-bum` → “兔兔屁屁”。
- 以上是 Erik 所玩色情游戏里的幼稚双关，仅在该游戏语境保持一致，不作为全项目身体部位通用术语。

## `ano02.rpy` 调查与金融术语

| 英文 | 统一中文 | 说明 |
|---|---|---|
| Saga Financial Bank | 传说金融 | 沿用仓库既有机构名；对话中无需机械补“银行” |
| autopsy report | 尸检报告 | 警方调查语境 |
| asphyxiation | 窒息 | 保持死因信息，不弱化成“呼吸困难” |
| bank teller | 银行柜员 | Liu Wang 的职务 |
| ATM / atm machine | 自动取款机 | 银行内用于查询账户和取款的机器；菜单或界面空间有限时可按既有资源写“ATM机”，正文优先用完整中文 |
| `My account.`（银行菜单） | 查询账户 | 指通过大厅自动取款机操作或查询账户，不译成生硬的所有格名词“我的账户” |
| offshore account | 境外账户 | 当前场景指电子转账的资金去向 |
| launder money | 洗钱 | 明确犯罪含义，不委婉化 |
| 10-62 | 10-62 | 警务代码保留原数字与连字符，不自行扩写含义 |
| Bedtime Bandit | “晚安大盗” | 本地窃贼的戏称；保留昵称式引号，后续出现时复核一致性 |
## `ano03.rpy` 威胁与警务术语

| 英文 | 统一中文 | 说明 |
|---|---|---|
| APB | 协查通报 | 警方向巡逻警员发布车辆/人员查找信息的语境 |
| get/take a statement | 做笔录 | 询问并记录证人陈述；不机械译作“拿声明” |
| criminal organization | 犯罪组织 | 保持组织犯罪含义 |
| squad car | 警车 | 日常剧情无需展开车型 |
| patrol / monitor the neighborhood | 巡逻 / 留意周边 | 按具体句式处理，不机械统一 |
| assertive route | 强势路线 / `{dom=强势}` | 界面标签值必须中文显示 |
| submissive route | 顺从路线 / `{sub=顺从}` | 界面标签值必须中文显示 |

## `ano04.rpy` 丧亲慰问与生活语境

| 英文 | 统一中文 | 说明 |
|---|---|---|
| give/offer condolences | 表示慰问 / 说声节哀 | 根据人物亲疏调整，不机械译作“给予哀悼” |
| sublet | 转租 | 当前场景指 Tammy 将自己的房子转租出去 |
| come out of one’s shell | 慢慢开朗起来 / 不再封闭自己 | 按角色口吻处理，避免直译“走出壳” |

## `ano05.rpy` 监视、家庭安全与语用

| 英文 | 当前处理 | 说明 |
|---|---|---|
| keep on driving | 没停车，直接开走 | 当前场景强调车辆未停下，不译成“一直开着车” |
| a lot of good that's doing us | 可真是帮了我们大忙 | 反讽警方迟迟没有进展，不能按正面陈述翻译 |
| bond / bonding | 增进感情 | Debbie 希望 Jenny 与 Anon 改善同住关系，不擅自写成恋爱或亲属关系 |
| labia | 阴唇 | Jenny 的露骨厌恶比喻；保持身体部位准确，不净化，也不额外升级 |
| That's my boy! | 这才对嘛！ | 鼓励性习语；本场不能译成“这才是我儿子” |
| a cute girl down the street | 街那头那个可爱的女孩 | `down the street` 表示附近方位，不译成随机的“街上女孩” |

## `ano06.rpy` 追债、黑帮与房贷术语

| 英文 | 当前处理 | 说明 |
|---|---|---|
| Tony's Pizza / Tony’s Pizza | Tony披萨店 | Tony 为英文姓名，不写作“托尼披萨店” |
| little bunny | 小兔子 | Dimitri 对 Anon 的固定嘲弄；与 Frank 生前的求饶呼应 |
| break both hands | 两只手都打断 | 明确的暴力威胁，不弱化成笼统“教训” |
| hand sanitizer | 洗手液 | Igor 搜身误抓阴茎后的洁癖笑点，必须保留场景因果 |
| put the screws on | 施压／逼迫／把矛头转向 | 按主宾关系处理，不直译成“上螺丝” |
| take his medicine | 认罚／承受后果 | 指接受犯罪组织惩罚，不按字面译“吃药” |
| snuff out your entire family | 灭门／杀光全家 | Tony 对犯罪组织手段的警告，暴力强度不得弱化 |
| Russkies | 俄国佬 | Tony 的贬义粗俗说法；与普通 `Russians` 区分 |
| Russians | 俄国人 | 中性识别国籍，不机械套用“俄国佬” |
| Das vidania | 达斯维达尼亚 | Tony 故意装腔的俄语告别梗，保留异国语感和挑衅口吻 |
| loan | 贷款 | Debbie 为支付二十五万美元而借款 |
| collateral | 抵押物／拿房子作抵押 | `used the house as collateral` 译“拿房子作了抵押” |
| put up the house | 拿房子作抵押 | 与 `collateral` 统一，不误译成出售房屋 |


## `ano07.rpy` 披萨店雇佣与送餐术语

| 英文 | 当前处理 | 说明 |
|---|---|---|
| dine in | 堂食 | 与到店自取、外送并列的经营方式 |
| pick up / collection order | 到店自取／到店自取订单 | 指顾客自行到店领取，不译成“收款订单”或普通取货 |
| delivery boy | 送餐员／送餐小子 | Tony披萨店的披萨外送岗位；正式描述用“送餐员”，Tony／Maria 口语中可说“送餐小子” |
| trial run | 试送／试送一趟 | 指正式录用前的送餐测试，不译成泛化的“试运行” |
| perfect run | 完美完成的一趟送餐 | Tony 因全部订单正确送达而额外发放奖金 |
| kitchen | 后厨 | 披萨店工作区语境；家用烹饪场景仍可按语境译“厨房” |
| unmentionables | 贴身衣物 | Maria 指先前被 Anon 意外看到的私密衣物，保留尴尬但不擅自改成裸体 |
| premier pizza establishment | 首屈一指的披萨店 | `pizza_main.rpy` 中 Anon 故作正式地介绍 Tony披萨店，保留夸张宣传腔 |
| `[custom name]'s Pizza` … `authentic` | `[自定义姓名]披萨店听起来没那么正宗` | 英文源缺少疑似 `sound` 的谓语；结合 Tony 被改名的条件和下一句讽刺笑点，按店名听感处理 |
| open 24/7 | 全天候营业 | `pizza_shop.rpy` 中“不全天候营业的披萨店”是学生噩梦式夸张，不机械写作“24/7开放” |
| archaic bylaws | 老掉牙的地方法规 | 星期日禁吃披萨是 Anon 假装严肃的荒诞笑话，不当作真实世界观法规扩写 |
| brains of the operation | 全靠她拿主意 | 强调 Maria 是实际经营核心，不直译“行动的大脑” |
| heart and soul | 主心骨 | 与上一句连续，说明 Maria 对店铺不可或缺 |
| capisce? | 懂了没？ | Tony 的固定江湖化口头表达，保留压迫或催促感 |

## `ano09.rpy` 专属称呼、车辆与意大利裔口吻

| 英文 | 当前处理 | 说明 |
|---|---|---|
| champ | 冠军 | Tony 对 Anon 的固定专属称呼；仅在英文明确使用 `champ` 时采用，不替代普通 `kid`／`kiddo` |
| babyface | 小帅哥 | Tina 对 Anon 的固定专属称呼；非称呼用法不得机械译成“娃娃脸”，应按语境处理为“长着娃娃脸的年轻人”等自然表达 |
| dollface | 美人儿 | Maria／Tony 使用的老派亲昵称呼；不是人物专名，不保留英文 |
| kid / kiddo | 小子／好小子 | 按责备、鼓励或熟稔语气选择，不与 `champ` 混用 |
| Yes, sir! | 遵命，老板！ | Anon 对 Tony 的玩笑式或恭敬回应；当前是雇佣关系，不机械译“先生” |
| Yes, ma’am. | 是，老板娘。 | Anon 对 Maria 的恭敬回应；结合披萨店经营关系处理 |
| scooter | 踏板车 | 与自行车、汽车分支区分 |
| car dealership / dealership | 车行 | 购买、置换车辆的场所 |
| trade-in | 旧车折价／旧车抵价 | 根据句式写“旧车抵了不少钱”“给旧车估了个好价”等 |
| calzone | 意式烤饺 | Maria 后厨制作的食物，不音译成人物名 |
| The Overcompensator | 过度补偿者 | 豪华车的夸张车型名，保留炫耀和补偿心理的笑点 |
| The Blue Falcon | 蓝色猎鹰号 | Tony 为车辆提出的夸张名字 |
| The Sapphire Stallion | 蓝宝石种马号 | 与“蓝色猎鹰号”并列的夸张车辆名 |
| Holy Mary, Mother, and Joseph! | 圣母玛利亚和圣约瑟在上！ | Maria 的天主教文化感叹，保留宗教色彩，不缩成泛化的“天哪” |
| forghedaboudit | 甭提了／别放在心上 | Tony 的意大利裔纽约式口头表达，按语用自然汉化，不保留英文拼写 |

- Tony、Maria 的意大利裔美国人口吻通过短句、老派口头语、夸张和宗教文化痕迹体现；不得硬套中国地方方言，也不得写成现代网络梗。
- Tony 帮助 Tina 源于与 Luigi 的兄弟情和遗属照顾承诺；相关调侃不得误译成明确婚外情。

## `ano10.rpy` 披萨制作、双关与生育诊断

| 英文 | 当前处理 | 说明 |
|---|---|---|
| hand-tossed dough | 手抛饼底 | 披萨制作术语，不译成泛化的“手工面团” |
| toppings | 配料／铺配料 | 按名词或动作自然处理 |
| deep-dish pizza | 深盘披萨 | Maria 明确鄙视的披萨类型 |
| pizza stone | 披萨石 | `double pizza stone setup` 译“上下两块披萨石” |
| pie / pizza pie | 披萨 | 披萨店语境，不直译“馅饼” |
| cannoli / cannolis | 意式奶油甜馅卷 | 食品名称统一；`Holy cannoli` 是感叹语，须另按语用翻译 |
| protégé | 徒弟 | Tony 对 Anon 的培养定位，跨 `ano10.rpy`、`ano11.rpy`、`tin_vault.rpy` 保持一致 |
| mustache ride | 骑胡子 | 成人双关；保留 Anon 不懂含义的喜剧节奏，不提前解释成口交 |
| my boys can’t swim | 我的小蝌蚪游不动了 | Tony 对不育诊断的委婉比喻 |
| my batter’s expired | 我的面糊过期了 | 与披萨店身份相符的生育比喻 |
| my milk’s turned sour | 我的牛奶馊了 | 与上一句连续递进，不擅自改成医学说明 |
| my gun’s shooting blanks | 我的枪打的是空包弹 | 生育能力比喻；随后才直白说明精液没有精子 |

- `ano10.rpy` 中 Maria 的“奖励”先以意式奶油甜馅卷制造误导，但 `mar_cook.rpy` 的成功分支后续明确描写了 Maria 借“奶油馅点心”双关为 Anon 口交。前段保留食物误导，后段不得净化或跳过明确的性行为。
- Tony 与 Luigi 是胜似亲兄弟的黑帮旧友；`more than friends` 不得译出恋爱关系。

## `ano11.rpy` 生育选择、俄式食品与黑帮专名

| 英文 | 当前处理 | 说明 |
|---|---|---|
| adoption | 领养 | Tina 提出的家庭选择；不得误写成收养宠物或临时照顾 |
| sperm donor | 精子捐献者 | 区分匿名捐献者与夫妻认识、信任的捐献人 |
| swimmers | 小蝌蚪 | Tony 对精子的委婉说法，并承接池塘/游泳双关 |
| pregnancy stuff | 生孩子的事／备孕和生育难题 | Maria 尚未怀孕；不得误译成已经发生的孕期事项 |
| pelmeni | 俄式饺子 | Igor 提议的俄式食物 |
| borscht | 罗宋汤 | Igor 反复惦记的食物；跨文件保持一致 |
| pirozhki | 俄式馅饼 | 结合场景作可理解的食品译名，不音译 |
| little bunny | 小兔子 | Dimitri 对 Anon 的戏谑性固定称呼 |
| The Plumber | `The Plumber` | Tony 的旧黑帮绰号，属于人物专名，保持英文原状 |
| Eddie Four-Fingers / Four-Fingers | `Eddie Four-Fingers`／`Four-Fingers` | 旧黑帮关系的姓名/绰号，保持英文拼写与原文形式 |
| pair of ducks | 一对二 | 骰子/牌桌式比喻，指 Maria 一人对付两名闯入者 |
| has balls | 有种 | 本义为有胆量；Igor 随后按“蛋蛋”误解，必须保留双层笑点 |
| Get. / The fuck. / Out of my shop! | 给。／老娘。／滚出我的店！ | 保持三条 Ren’Py 台词，中文连读为“给老娘滚出我的店！” |

## `ano13.rpy` 特殊披萨、地点与调查术语

| 英文 | 当前处理 | 说明 |
|---|---|---|
| pear | 梨 | 特殊披萨配料；与后两项构成连续列举 |
| prosciutto | 意式风干火腿 | 不泛化为普通“火腿”，跨文件保持食品术语 |
| gorgonzola | 戈贡佐拉奶酪 | 蓝纹奶酪品种；不使用不稳定音译 |
| pear-prosciutto-gorgonzola pizza | 梨、意式风干火腿和戈贡佐拉奶酪披萨 | 三项配料多次重复，顺序和核心译名保持一致 |
| Beachside Apartments | 海滨公寓 | 地点专名；保留房号变量或数字 |
| calzone | 意式烤饺 | 与 `ano09.rpy` 一致；藏锉刀的越狱笑话仍保留核心食品译名 |
| serving a ten stretch upstate | 在州北部监狱服十年刑 | 黑帮口语；同时保留地点方向、监禁和刑期信息 |
| dirty Russkies | 俄国杂种 | Tony 的粗俗敌对称呼；按原文保留攻击性，不推广成中性族群称谓 |
| extra sausage on the side | 另外还加一根“香肠”吗？ | Tina 借披萨配料影射 Anon 的阴茎；用弯引号点明双关，同时保留 Anon 一时没听懂的笑点 |

- `Eddie Four-Fingers` 在本文件恢复为英文原名；不得写作“Eddie·四指”等混合形式。
- `babyface`、`dollface`、`champ` 继续分别固定为“小帅哥”“美人儿”“冠军”。
- 动态日期 `[saga.time.dow + when]`、`[saga.time.dow + when + 3]` 必须原样保留，只调整外围中文语序。
## `ano15.rpy` 自然受孕、走私情报与 Tony 双关

| 英文 | 当前处理 | 说明 |
|---|---|---|
| hydration is key | 补水最重要 | Tony 反复叮嘱的运动补水口号；`ano13.rpy` 和 `ano15.rpy` 统一 |
| capicola | 卡皮科拉火腿 | 意大利式熟食；保留 Tony 的食物比喻 |
| file（越狱工具） | 锉刀 | 藏在意式烤饺里的金属工具，不译成“文件” |
| mustache ride | 骑胡子 | 已在 `ano10.rpy` 和 `ano15.rpy` 复核；保留成人双关及 Anon 早期没听懂的笑点 |
| calzone | 意式烤饺 | `ano09.rpy`、`ano13.rpy`、`ano15.rpy` 统一核心译名 |
| Boy, boy, boy... very tall boy. | 男孩，男孩，男孩……长得高高的男孩。 | Tony 给 Maria 的尴尬暗号；保留重复节奏和拙劣掩饰感 |
| workplace seminar | 职场性骚扰培训 | Maria 针对 Tony 向员工说露骨话的惩罚式威胁；Tony 害怕的是再次参加强制培训，不是与 Maria 发生性行为 |
## `ano16.rpy` 家庭身份与黑帮式元叙事

| 英文 | 当前处理 | 说明 |
|---|---|---|
| godfather | 教父 | 指 Anon 担任 Tony 与 Maria 孩子的教父；同时承接 Tony 的黑帮背景和下一句《教父》式玩笑，不改成“干爹” |
| an offer you can't refuse | 一个你没法拒绝的提议 | 保留《教父》式固定笑点；按 Tony 口吻自然表达，不直译成僵硬公文语 |
| Not this update! | 这次更新不给！ | 第四面墙式版本结尾；必须保留“更新”的元叙事含义 |


## `ton_baby.rpy` 黑帮电影引用、育儿与披萨店语境

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `wingman`（Tony／Luigi 往事） | 僚机 | 化用《壮志凌云》台词；两人争着让对方当自己的僚机，连续两句必须保留互相顶嘴的笑点 |
| `bank / blood bank` | 银行／血库 | Tony 先假装答应送人去银行，再以“血库”落到枪杀威胁；中文优先保证自然的暴力反转，不生造“血银行” |
| `ciabatta` | 夏巴塔面包 | Tony 转述 Luigi 改写动作片台词时提到的意大利面包；保持 Luigi 英文姓名，不音译 |
| `rat`（黑帮语境） | 告密者 | 指背叛或向警方告密的人，不机械译成“老鼠／鼠辈” |
| `Forgiveness is between you and god...` | 原不原谅你，是你和上帝之间的事；我只是负责送你去见他 | Tony 的死亡威胁式黑帮名句，两句必须连续承接，不能译成普通会面安排 |
| `Say hello to my little friend!` | 跟我的小家伙打声招呼吧！ | 化用《疤面煞星》枪战台词，`little friend` 指武器笑点，不是小朋友 |
| `good, solid Italian stock` | 骨子里是正儿八经的意大利人 | Tony 认为孩子承受得住暴力故事的血统自豪，不采用“优秀、坚实的血统”等翻译腔 |
| `The show must go on`（Tony产后返店） | 店里的生意还得照常做 | 指舍不得离开 Maria 和孩子却仍须营业，不按舞台语境机械译“演出必须继续” |
| `Give her my love`（后厨成人暗示） | 替我好好疼疼她 | Tony 明知并鼓励 Anon 与 Maria 亲热；结合后续“别让顾客听见”理解，不弱化为普通问候 |
| `deliveries`（披萨店柜台） | 外送订单／几单外送 | 指等 Anon 配送的披萨订单，不译成笼统的“货” |

## 卧室设备与系统交互

| 英文 | 当前处理 | 说明 |
|---|---|---|
| Consum-R | Consum-R | 商场店名，保持英文原拼写和连字符；电脑零件线索与其他购物任务统一 |
| PC | 电脑 | 普通叙述和内心独白使用自然中文，不保留界面外的英文缩写 |
| higher resolution graphics | 更高分辨率的画面 | 电脑修复后的画质升级元叙事，不译成生硬的“图形” |
| bugs（游戏故障） | BUG | 仅用于游戏程序故障语境，与昆虫含义区分 |
| cheat menu | 作弊菜单 | 手机 Wi-Fi 连续点击彩蛋；保留玩家主动寻找并最终解锁的第四面墙逻辑 |


## Maria 线固定双关、专名与成人表达

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `champ` | 冠军 | Tony 对 Anon 的专属称呼 |
| `The Falsettos` | 《假声》 | 电视节目标题 |
| `horizontal pizzica` | “横着做披萨” | 保留性双关 |
| `primed pussy` | 水润润、正等着开干的骚屄 | 保留 Tony 的露骨起哄 |
| `tap that` | 好好肏她一顿 | 明确性行为动作 |
| `work that big cock` | 好好使唤那根大鸡巴 | Tony 的粗俗起哄 |
| `lampredotto` | 灯笼牛肚 | 意大利食物比喻 |
| `Devil's Threeway` | 恶魔三人行 | Tony 为三人性交提出的夸张招式名 |
| `The Kidney Shifter` | 移肾术 | Tony 为性交动作提出的夸张招式名 |
| `batter` | 面糊 | 造人语境下指精液，延续披萨店食物双关 |
| `little guys` | 小家伙们 | 指精子，保持 Tony 半玩笑式造人说法 |
| `cannoli` | 意式奶油甜馅卷 | 食品核心译名不变；成人双关中仍保持同一意象 |
| `au jus` | 肉汁 | Maria 在披萨店后厨使用的食物式性比喻 |
| `Yes, ma’am.` | 是，老板娘。 | Anon 的服从式回应，同时对应 Maria 的经营者身份 |
| `break` | 休息／歇会儿 | 先指工作间歇，随后成为性交邀请和事后回味的连续双关 |
| `Gimme another baby` | 再让我怀一个 | Maria 明确要求再次受孕，不直译成生硬的“再给我一个宝宝” |
| `lookin’ for trouble` | 来找刺激／找刺激 | 后期性邀约式双关，不按普通“找麻烦”处理 |
| `Wages.` | 工钱 | 披萨外送欠付报酬的菜单主题；金额变量原样保留 |
| `buddy`（Tony 对 Anon） | 小兄弟 | Tony 在雇佣早期的粗犷亲近称呼；不得误作字面亲兄弟，也不与专属 `champ`“冠军”混用 |
| `smalls`（Tony 对 Anon） | 小子 | Tony 在送餐失败时使用的调侃式小辈称呼；承接“你真要了我的命”的抱怨语气 |
| `hands are a little full`（抱婴儿状态） | 腾不开手 | `pizza_boxes.rpy` 取工钱分支中的视觉语义；不是泛指资金紧张或事务繁忙 |
| `settle up`（工钱语境） | 结清工钱 | 指 Tony／Maria 支付披萨外送报酬，不泛化成“处理事情” |
| `short tempered people`（披萨店厨房） | 脾气火爆的人 | Anon 对后厨工作人员的概括式吐槽；保留喜剧性的危险感，不擅自点名或强化成暴力威胁 |
| `wander in there`（受限入口） | 随便闯进去 | 指未经允许进入披萨店厨房，不是已经进门后在里面闲逛 |
| `Baby.`（菜单主题） | 宝宝 | 指谈论宝宝，不是亲昵称呼“宝贝” |
| `kid` / `handsome` | 小子／帅哥 | 标记 Maria 与 Anon 从长辈式审视到亲密暧昧的关系变化 |
## Jenny 线固定辱称与成人角色称谓

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `perv` / `pervert`（Jenny 对 Anon） | 变态 | Jenny 从前期偷窥冲突延续使用的高频辱称；后续可随关系阶段调整整句语气，但核心称呼不漂移为“色狼”等其他译法 |
| `loser`（Jenny 对 Anon） | 废柴 | Jenny 高频固定辱称；整句强度随关系阶段调整，核心称呼保持一致 |
| `The Electro Clit` | 电击阴蒂棒 | Pink 出售的情趣玩具产品名 |
| `Electro Clit Light` | 电击阴蒂棒轻量版 | 原版缺货时出现的低功率版本 |
| `Pink` | 粉色诱惑 | 商场二楼情趣用品店；用户确认的意译，保留粉色意象与成人氛围，不作“粉红”或“粉红情趣用品店” |
| `Pink Channel` | `Pink Channel` | Jenny 使用的成人内容账号／频道专名，保持英文拼写，不译作“粉红频道” |
| `turn me down`（Jenny 性邀约） | 拒绝我 | `jen_visit.rpy` 中指拒绝她当夜的性要求，不译作普通“让我失望”；拒绝分支必须保留 Anon 明确说不的边界 |
| `Daddy`（`jen04.rpy` 成人影片角色扮演） | 爸爸 | 属色情角色称谓，不是人物姓名或真实亲属身份；与育儿支线中孩子对父亲的 Daddy 必须按场景区分 |
| `Sluttygram` | `Sluttygram` | 成人照片订阅网站专名，保持英文拼写和大小写，不译成“浪荡格莱姆”“偷情网”等中文名称 |
| `wimp`（`jen05.rpy` 中 Jenny 对 Anon） | 窝囊废 | 同一场景两次出现，后续仍按关系阶段复核；不对其他角色的普通用法做全仓替换 |
| Bad Monster | 坏怪物 | Pink出售的大型情趣玩具名称；与资源物品、任务提示及Jenny线保持一致 |
| Pink Cyclone | `Pink Cyclone` | CLT 游戏宣传活动中的角色/品牌专名，保持英文拼写，不译作“粉红旋风/粉色旋风” |
| World of Orcette / WoO | `World of Orcette` / `WoO` | Erik、Karl、Justin参与的网络游戏及其缩写，保持英文，不使用中文书名 |
| Brutalitops | `Brutalitops` | Karl的游戏角色名，保持英文，不音译为“野蛮托普斯/残忍之巅” |
| WPWF | `WPWF` | Women's Professional Wrestling Federation 的缩写；解释全称时译“女子职业摔角联盟” |
| no contest（摔角） | 无结果 | 比赛不计胜负，不等同于平局；战绩 `34-0-1` 的最后一项按“1场无结果”处理 |
| Cosmic Cumics | 宇宙漫画 | 漫画及游戏商店；保留宇宙／科幻风格，与 UI 一致，可称“宇宙漫画店”。原拼写有成人谐趣，不为硬凑双关损害店名自然度 |
| GooTube | `GooTube` | 视频平台专名，保持英文拼写和大小写，不译作普通“视频网站”或仿照现实平台改名 |
| VirginLily69 | `VirginLily69` | Lily 的网络主播名，保持英文拼写、数字和大小写 |
| cosplay / costumes（`lily.rpy`） | cosplay／cosplay服 | 指 Lily 的亚文化爱好及店内新款服装，避免“戏服”造成舞台演出误解；其他剧情中的普通角色扮演仍按场景处理 |
| `huge... fan base`（Lily） | 巨大的……粉丝群 | 保留停顿形成的胸部双关，不把 `fan base` 错译成身体部位，也不能抹掉暧昧 |
| `forms`（Lily 的身材语境） | 丰满的身材 | 指她难塞进紧身 cosplay 服的丰满曲线，不译成抽象的“形式”或笼统的“身体” |
| camshow / camshows | 成人直播 | Jenny 线涉及色情表演时明确成人性质，不泛化成普通视频直播 |
| `fool around`（私人性邀约） | 亲热一下 | 在卧室等明确成人语境中指发生亲密性行为，不译为含混的“玩玩／搞点事情”；任务提示等其他句法仍须按场景处理 |
| Judith 食物式感叹：`wowie waffles` / `Magnificent muffins` / `Holy honey buns` | 哇哦，华夫饼！／妙极了，松饼！／老天，蜂蜜面包！ | 保留 Judith 幼稚、押头韵又古怪的感叹模式，不统一抹平成普通“太棒了／天哪” |
| `Specs.` / `spectacles`（Judith 线） | 眼镜 | `judith.rpy` 的任务菜单指向 `specs_judith.rpy` 眼镜事件；储物柜锁定提示中的 `spectacles` 是 Judith 的私人备用眼镜，不得误作“规格”或“护目镜” |
| `Bathroom fun.`（Judith 线菜单） | 浴室亲热 | 通过 `choice='stall'` 指向 `jud_stall.rpy` 的私下亲热事件；保留菜单式简短表达，不译成含混的“浴室趣事” |
| `faptic engine` / `Faptic Engine` | 触觉引擎 | Tori／June 相关任务中的虚构振动部件，可提供皮肤触觉反馈；保持既有译法与大小写变体对应，不拆成普通“发动机” |
| `Dress.`（Kassy／Cupid 菜单） | 连衣裙 | 指 Anon 在女装店要找的裙装商品／任务话题，是名词，不译成动作“穿衣服” |
| `cum for me`（对女性） | 为我高潮／高潮给我看 | 指要求女性达到高潮，不能误写成射精；对男性说出同一句时必须按男性射精语义另译 |
| `Finish her!`（`jen_finger.rpy` 菜单） | 让她高潮！ | 选择继续指交直至 Jenny 高潮、潮吹；不得译成伤害或杀死她 |
| `life was flashing before my eyes` | 看见人生走马灯 | `jen_pool.rpy` 中 Anon 因被 Jenny 压入水中、接近溺水而出现人生走马灯，不是因高潮“爽死了” |
| `skinny dipping` | 裸泳 | 指不穿泳衣游泳；与 `deb23.rpy` 已有译法保持一致 |
| `cannonball`（跳水） | 炸弹入水 | Anon 裸身跳入泳池故意溅 Jenny 的动作及后续复述，两处保持一致 |
| `peasant`（公主角色扮演） | 贱民 | 与 `Princess Jenny / your highness` 配套，属于双方性支配角色，不是现实阶级称谓 |
| `Screw you! / That's the idea.` | “操你！”／“没错，就是这个意思。” | 保留 `screw` 同时表示辱骂和性交的双关；不得将前句改成“去你的”而切断回应笑点 |
| `doggy / good boy / treat`（Jenny 支配玩法） | 小狗狗／乖狗狗／奖励 | 与公主角色、学狗叫和乞求配套；`good boy` 在此不是普通“乖孩子”，`treat` 也不是食物或赏钱 |
| `take it deep`（口交） | 含深一点／再含深一点 | `jen_shower.rpy` 中指 Jenny 尝试深喉；必须明确口交动作，不能含混成普通“再深一点” |
| `I like swallowing your cum` | 我喜欢吞你的精液 | Jenny 在没有观众的淋浴间私下承认真实性偏好；紧接着仍否认喜欢 Anon，不得据此提前坐实恋爱关系 |
| `cuddle up`（`jen_sleep.rpy`） | 搂着睡 | Jenny 用“我来只为做爱，不是为了搂着睡”区分性需求与非性亲密；不能泛化成普通“抱一下”而丢失同床语境 |
| `big fucking baby` | 他妈的巨婴 | Jenny 指 Anon 像小孩一样闹脾气，不是骂他“大傻逼”；保留幼稚、黏人的语义 |
| `a taste of her own medicine`（`jen_sleep.rpy`） | 让她尝尝被人吊胃口的滋味 | Anon 中途放弃做爱，以 Jenny 过去戏弄自己的方式反制；不得直译成“尝尝自己的药” |
| ski mask / mask | 滑雪面罩／面具 | 具体品类译“滑雪面罩”；泛指用于直播遮脸的用品译“面具”，不写作“口罩” |
| stunt cock | 鸡巴替身 | `jen18.rpy` 中 Anon 缺席成人直播后的连续行业笑点，三处复述保持一致 |
| camgirl | 成人女主播 | 指女性成人直播从业者；`jen15.rpy` 与 `jenny.rpy` 统一，不写成容易与平台名混淆的“色情主播” |
| tips（成人直播） | 打赏 | 观众为 Jenny 的镜头动作和表演付费，不译为普通“小费” |
| subscribers（成人直播） | 订阅者 | Jenny 对付费观众群体的称呼 |
| `sex goddess`（Jenny 自称／成人直播角色） | 性爱女神 | Jenny 在早期个人成人直播、后续共同直播、性交自夸和孕期表演中反复使用的成人角色称谓 |
| Sam9 / sam9 | `Sam9` / `sam9` | CAMslut 用户名，按各处英文原文保持大小写，不音译 |
| footjob / jerk off with feet | 足交／用脚打手枪 | Jenny线按句法处理；动作和射精结果必须明确，不弱化为普通按摩 |
| lick my toes | 舔我的脚趾 | Jenny 对 Anon 的支配式成人挑逗，不泛化成“舔脚”而丢失具体动作 |
| boy toy（Jenny） | 小男宠 | Jenny 在成人直播支配 Anon 时使用的性称谓，不译为普通“小玩具” |
| Princess Jenny | 公主Jenny／公主[saga.cast.jenny] | 支配角色称谓；姓名或变量保持英文原状，内部复述使用中文双引号 |
| cheerleader | 啦啦队员 | 与 `head cheerleader` 区分；泛指啦啦队成员 |
| head cheerleader | 啦啦队长 | Jenny 过去在大学啦啦队中的身份 |
| cheerleading uniform / cheer uniform | 啦啦队制服 | Jenny 的大学旧制服；两种英文说法统一 |
| pom-pom / pom-poms | 啦啦球 | 啦啦队员手持的一对彩球；不得误译为“绒球花”，也不在“啦啦队彩球／彩球／拉拉球／绒球”之间漂移 |
| cheerleading routine / routine（啦啦队语境） | 啦啦队动作／整套动作 | `viv04.rpy` 中指为州冠军赛编排和练习的完整动作；按句法可写“编排啦啦队动作”“想一套新动作”“把整套动作练好”，不误译成日常作息 |
| State Championship（啦啦队） | 州冠军赛 | Roxxy 准备参加的赛事；Jenny 过去 `won ... state championships` 时按获奖结果译“赢得州冠军”，不能把参赛和夺冠混为一谈 |
| gun show（Bridget） | 肌肉秀 | Bridget 对镜展示手臂肌肉的自夸双关，不是枪械表演 |
| PING（成人直播） | 叮 | 观众打赏提示音；保留星号和 `{w=...}` 等演出格式 |
| CAMslut | `CAMslut` | 成人直播平台专名，保持英文拼写和大小写 |
| camslut | 成人直播骚货 | 小写为泛称而非平台名，按句法自然处理；`jen24.rpy` 中为 Anon 自嘲 |
| eat pussy | 舔屄 | 明确口交动作，原文露骨时不弱化成“服务”或“取悦” |
| suck your dick | 给你吹箫 | Jenny 首次口交场景的自然粗俗表达 |
| `peaches / my peaches`（`jen22.rpy`） | 桃子／我的桃子 | 早餐中用于掩饰成人直播的连续双关；字面是水果，同时承接 Anon 为 Jenny 舔屄、她高潮时弄湿其脸和头发。后续复述保持“桃子”，不能换成其他水果或直白解释而破坏 Debbie 不知情的笑点 |
| `little whipping boy`（Jenny 线） | 出气筒 | Anon 拒绝再任 Jenny 发泄和使唤；`jen23.rpy` 与 `jen_cam.rpy` 保持一致，不直译成“挨鞭子的男孩” |
| `jerk him / jerk him again` | 给他打手枪／再给他打一次手枪 | 成人直播中的手交动作，不能误译为口交 |
| `gawked at`（成人直播） | 被人围观 | Jenny 拒绝的是被观众观看，不代表她没有私人性需求 |
| `get paid and laid` | 既赚钱又做爱 | Jenny 对成人直播中商业收益和性交收益并存的粗俗概括 |
| `cum all over your face`（女性） | 在你脸上高潮，喷得你满脸都是 | 女性高潮不得写成“射满你的脸” |
| `boyfriend`（`jen25.rpy`、`jen26.rpy`） | 男朋友 | Jenny 为吓退偷窥者临时冒认 Anon 的身份；`jen26.rpy` 中 Zana 持续误认，Jenny 在发生更多主动性行为后仍再次否认正式关系。保留暧昧试探，但不能提前坐实恋爱 |
| `stalker` | 跟踪狂 | 指反复尾随、躲藏并偷窥 Jenny 的人；动作 `stalking / spying on` 依句法译“跟踪／偷窥” |
| `gummy worms` | 虫形软糖 | Jenny 在电影院约会中反复索要的零食；不译成“软糖虫”等倒装表达 |
| `blueberry slushy` | 蓝莓冰沙 | Jenny 在电影院约会中指定的饮品 |
| `Bitch Perfect` | 《完美贱人》 | 电影院上映的女性向电影标题；保留对 `Pitch Perfect` 式片名的戏仿感 |
| `Blue Ninja Lollipop Girl` | 《蓝忍者棒棒糖女孩》 | Anon 与 Jenny 小时候一起看过的卡通电影标题 |
| `Pals` | 《好友》 | `jen_gfe.rpy` 中 Jenny 童年常与 Debbie 一起看的虚构老情景喜剧；两次提及时统一，正文保留原有 `{i}` 斜体标签，剧中人物 Matt、Courtney 保持英文 |
| `criminal harassment` | 刑事骚扰 | Anon 对 Zana 跟踪、偷窥行为的法律性质描述 |
| `autograph` | 签名 | Zana 作为 CAMslut 粉丝索要的亲笔签名；与 Jenny “在你脸上签名”的挥拳双关保持一致 |
| `chick flick` | 女性向电影 | Anon 对 Jenny 所选影片类型的口语评价，不译成贬损女性观众的生硬直译 |
| `lovey-dovey bullshit` | 卿卿我我的屁话 | Jenny 对恋爱式亲密行为的粗俗贬称；`jen27.rpy` 为拒绝 Anon 的正式约会诉求，`jen_gfe.rpy` 后续复述时保持同一核心语气 |
| `girlfriend experience` / `girlfriend thing`（Jenny 线） | 女友体验 | Jenny 在第三次拒绝真实恋爱后提出的一晚五百美元假女朋友服务；不能译成“女朋友游戏”，也不能暗示两人已建立正式关系 |
| `the real thing`（`jen28.rpy`） | 真正的女朋友／真正的恋爱关系 | Anon 拒绝付费假扮安排时提出的关系诉求，不是“真家伙”或性器官 |
| `girlfriend the shit out of you` | 按语境译为“把女朋友演得极好／提供极好的女友体验” | `girlfriend` 在此被临时动词化，是演技和角色扮演笑点，绝不能误译成性交 |
| `two braincells ... fighting for third place` | 两个脑细胞还都在争第三名 | Jenny 对 Anon 的智力挖苦；保留“两个却争第三名”的荒谬笑点 |
| `white picket fence` | 白色尖桩篱笆 | 美国郊区传统家庭生活的象征；与结婚、生孩子和小砖房共同构成 Jenny 对安定伴侣生活的讽刺清单 |
| `tan / burn`（日晒） | 晒黑／晒伤 | Jenny 的皮肤不会晒黑，只会晒伤；两者必须明确区分 |
| `local theater`（Jenny 线） | 本地电影院 | 本线为放映电影的场所，不译成舞台剧院 |
| `grandmother` / `nana` / `grandma`（Debbie 对 Jenny 的孩子） | 外婆 | Debbie 是 Jenny 的母亲，中文按母系亲属关系处理；不得译为“奶奶” |
| `momma bear` | 护崽母熊 | Jenny 产后强烈保护孩子，连医护检查和托儿安排都会抗拒 |
| `little one` / `little ones`（育儿） | 小家伙／小宝贝 | 按单胎、双胎及语气自然选择；不得误作情侣昵称 |
| `Daddy`（`jen_baby.rpy` 育儿） | 爸爸 | Jenny 当着孩子明确指称 Anon，确认真实父亲身份与共同育儿；须与成人影片角色扮演中的 Daddy 按场景区分 |
| `porn name` | 色情艺名 | Jenny 设想孩子未来成人直播身份时使用的黑色幽默，不弱化成普通“艺名” |
| `scramble your eggs`（`jen_table.rpy`） | 把你的“蛋”炒一炒 | 承接 Debbie 询问炒蛋做法的早餐／性交双关；Anon 故意把 `eggs` 转指 Jenny 的生殖意义，不能平译成真要替她做早餐 |
| `over easy`（鸡蛋做法） | 双面嫩煎 | 指鸡蛋翻面后仍保留流心的做法，不误译成“单面煎” |

## Josie 线车行术语与连续笑点

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `TPS report(s)` | TPS报告 | Yoshi 与 Josie 关于车行文书工作的重复笑点；与后面的普通费用报表区分 |
| `T-straps` | T字带凉鞋 | Josie 网上抢购的露趾鞋款；`jos01.rpy` 四次重复时保持一致 |
| `Hattori Hanzō` | `Hattori Hanzō` | 人物姓名保持英文原状，不写“服部半藏” |
| `Freetwood Panhandrer` / `Fleetwood Panhandler` | 分别保持英文拼写 | 前者是 Yoo 的误读，后者是 Anon 的纠正；不得统一拼写而破坏笑点 |
| `J-Ro` / `J-Lo` | 分别保持英文拼写 | Yoo 的误称与原名形成笑点；不得擅自统一 |
| `Mini Vulva` | 迷你外阴 | 小型汽车的色情双关车型名；`jos_trade.rpy` 三处统一，不漂移为“迷你小穴／迷你小阴唇” |
| `SL-700 Crotch Rocket` | SL-700 胯下火箭 | 纯电动踏板车车型名；保留 `crotch rocket` 的胯下／高速摩托双关，不译成“肌肉摩托” |
| `Cotton`（`That’s a bold strategy, Cotton.`） | 保持 `Cotton` | 《躲避球》式文化引用中的人物姓名，按英文姓名规则保留，不泛化成“老兄” |
| `poor boy` | 穷小子 | Yoo 对 Anon 贫穷身份的固定羞辱称呼；不得漂移为“可怜的小子／可怜的孩子” |
| `Employee of the month` / `Emproyee of month` | 月度最佳员工 | Yoo 炫耀连续五个月获奖的头衔；后者是原文故意拼错，中文仍统一同一头衔 |
| `Phone.`（`yoshi.rpy` 菜单） | 手机 | 此处专指 Yoshi 扣下的 Josie 手机，是 `jos01.rpy` 潜入办公室分支入口，不泛化为座机 |

## Konty 机器人称呼与口癖

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `K.O.N.T.E.R.I.N.A.` | `K.O.N.T.E.R.I.N.A.` | Konty 的完整型号名，按英文专名原样保留全部句点和大小写 |
| `K-bot` | `K-bot` | Anon 给 Konty 取的昵称；保持连字符与大小写，不写成 `KBot` 或中文音译 |
| `Friend-Uhh` / `Friend-uhh` | 按原文保持 `Friend-Uhh` / `Friend-uhh` | Konty 把 Anon 的迟疑 `Uhh...` 误识别为称号后形成的专属称呼；不同句子的大小写须逐字服从英文原文 |
| `[saga.cast.tori.clan]-san` | `[saga.cast.tori.clan]-san` | Konty 对 Tori 的日式敬称；变量和 `-san` 后缀均保持，不改成“小姐／桑” |
| `Sexo en la playa` | `Sexo en la playa` | Konty 为拉丁流行乐播放列表取的西语标题；保持原文，不直译成“海滩性爱” |

## 图书馆馆务与办证用语

| 英文表达 | 统一处理 | 说明 |
|---|---|---|
| `library card` / `membership card` | 借书证 | 两者在 `library_shelf.rpy` 指同一张图书馆借阅证件；不得在同一流程中漂移为“会员卡” |
| `membership`（图书馆） | 办借书证／借阅资格 | 按句法处理：询问价格或加入时优先说“办借书证／办理”，菜单主题可译“办理借书证”；避免脱离场景的抽象“会员资格” |
| `membership fee` / `Membership is twenty dollars` | 办证费／办证要二十美元 | 指取得借阅资格的一次性费用，不是购买书本的价格 |
| `selection(s)`（图书馆） | 馆藏／藏书 | 指馆内可供借阅的书籍范围，不译成商品式“精选内容” |
| `front desk` / Jane 的 `desk` | 前台 | 均指 Jane 办证、查书和处理馆务的工作位置 |
| `librarian` | 图书管理员 | `library_study.rpy` 中 Anon 考虑报告做爱事件时专指 Jane，不泛化为“管理员” |
| `open` / `closed`（图书馆营业状态） | 开馆／闭馆 | 图书馆使用馆务表达，不写普通商店式“开门／关门” |
| `having sex` / `doing it`（`library_study.rpy`） | 做爱 | 上下文明确指第三方性交时必须直译核心动作，不弱化为“搞／做这种事” |

## 商场照相亭用语

| 英文 | 统一中文 | 说明 |
|---|---|---|
| photo booth / mall booth（拍照设施） | 照相亭 | `mall_booth.rpy` 场景中的自动拍照设施，不与厕所隔间等普通 `booth` 混用 |
| `capturing memories`（照相亭语境） | 定格回忆 | 同时保留摄影和保存共同经历的双关，不直译成生硬的“捕捉记忆” |
| `Advance time`（地点菜单） | 推进时间 | 明确表示游戏时间段推进的机制用语，不改写成“等一会儿”或“消磨时间” |
| `Take it slow and stick around.`（商场菜单） | 慢慢逛，继续留在商场 | 与离场选项对照，表示保留当前地点流程；`Take it slow` 不直译为放慢脚步 |
## Melody 线音乐、舞台与称呼双关

| 英文 | 推荐中文 | 说明 |
|---|---|---|
| `sugar`（Melody 对 Anon） | 甜心 | Melody 的高频专属称呼；后续逐文件统一，不与普通“糖”或其他角色语境混用 |
| `honey`（Melody 早期课堂鼓励） | 亲爱的 | `melody.rpy` 中安慰 Anon 能补回课程进度时的温柔称呼；语气比后期成人调情更日常，不与 `sugar` 的固定审计项混同 |
| `baby`（Melody 对 Anon） | 宝贝 | 成人调情称呼；不儿童化 |
| `good boy`（Melody 成人后戏） | 真乖 | 成熟支配式夸奖；不译“好孩子” |
| `Yes, ma’am!`（Anon 对 Melody） | 遵命，老师！ | 成人命令场景中的师生身份调情；不生硬译“女士” |
| `Miss [saga.cast.melody.clan]` | `[saga.cast.melody.clan]老师` | Anon 对音乐老师的姓氏称呼；保留变量，不译成“小姐” |
| `skin flute` | 肉箫 | Melody 的长笛／口交双关；与 `play/blow/master an instrument` 连续处理 |
| `private performance` | 私人演奏 | 既指只为 Anon 进行的演出，也指口交 |
| `master an instrument` / `mastering an instrument` | 练熟／精通一种乐器 | 保留练习乐器与提升口交技巧的双关，按句法自然变化 |
| `rousing speech` | 激昂的演讲 | 回扣 `mel06.rpy` 中 Anon 在讲台上被口交时被迫继续的公开致辞 |
| `encore` | 返场演出 | Melody 再次口交的舞台双关；不音译“安可” |
| `finale` | 压轴／压轴好戏／压轴表演 | 按演出句法选择；`mel_office.rpy` 指私人舞蹈最后的自慰展示，不译“结局” |
| `Fill me up`（性交） | 把我灌满 | 明确要求内射；保留动作结果，不弱化为普通“给我” |
| `groove` / `get back in the groove`（音乐课） | 玩音乐／找回节奏 | `melody.rpy` 中前者邀请 Anon 加入课堂演奏，后者同时指补回学习状态和音乐节奏；不得泛化成“嗨”或普通“重新适应” |
## Mia 线学校与美术事件术语

| 英文 | 推荐中文 | 说明 |
|---|---|---|
| `Art partner.` | 美术搭档 | `mia.rpy` 事件菜单；指 Barbara 私人美术课和学校美术比赛支线中的绘画搭档，不泛化为表演艺术或抽象“艺术伙伴” |
## Micoe 新生儿护理入口术语

| 英文 | 推荐中文 | 说明 |
|---|---|---|
| `How are they?`（新生儿护理菜单） | 孩子怎么样？ | `micoe.rpy` 公共菜单，需同时兼容男婴、女婴和双胞胎；不用固定复数代词“他们” |

## Tori 线血清材料与 DNA 样本

| 英文／内部标识 | 推荐中文 | 说明 |
|---|---|---|
| `misc_tissue` / used tissue（`tor05`） | 用过的纸巾 | 指 Ursula 办公室垃圾桶中带有唾液 DNA 的纸巾；是 Tori 血清任务的样本物品。叙述取样动作时可写“从垃圾桶里拿走用过的纸巾”，不得误成普通备用纸巾、卫生纸或 Ursula 主动提供的样本 |
| `horny toad` / `horny toad extract` | 发情蟾蜍／发情蟾蜍提取物 | Tori 血清任务中的虚构材料；`horny` 与繁殖季相呼应，需保留“发情”笑点，不译成“角蟾／角蛙／色蛤蟆”。不带 `horny` 的普通 `toad` 仍译“蟾蜍”，角色口中的 `frog` 译“青蛙” |
| `kleptomania`（Anon 自嘲） | 偷窃癖 | `note_tori.rpy` 中 Anon 对连续偷拿学校物品的夸张自嘲；按口吻译成“偷窃癖”，不作正式医学诊断或心理标签扩展 |
| `note_tori` / key code to Tori's office | Tori办公室密码纸条／门禁密码 | 与`tor01.rpy`的搜查任务连续；`school_office2.rpy` 中没有门禁密码就无法通过电子密码锁；`note_tori.rpy`中的`else`强调在万能钥匙之外又少了别的东西，保留为“还有别的” |


## Olivia 线与陌生人成人邂逅用语

| 英文表达 | 统一译法 | 说明 |
|---|---|---|
| `Olivia` | `Olivia` | 英文姓名及说话人标识保持原状，不音译。 |
| `breasts`（Olivia 初遇场景） | 胸 | 口语化成人挑逗；与本场“摸胸”“喜欢我的胸”保持一致，不机械译为“胸部”。 |
| `play with`（明确成人语境） | 玩／玩玩 | Olivia 用于引导触摸和性互动；按上下文保留挑逗，不净化为普通玩耍。 |
| `big boy`（成人挑逗称呼） | 大男孩 | Olivia 离别时对 Anon 的调情称呼；不改成正式亲昵称谓，也不坐实关系。 |


## 商场摊位误会用语

| 英文表达 | 统一译法 | 说明 |
|---|---|---|
| `Adonis` | 阿多尼斯 | Pietro 自称拥有神话中美男子般的外貌；保留专名和自恋的戏剧感，不泛化成普通“美男子”。 |
| `apply the oil`（Pietro） | 涂油／帮我涂油 | 指摊位服务中的涂油动作，属于误会核心；不得写成 Anon 主动提出按摩。 |
| `get my abs` | 帮我练出腹肌 | Pietro 对自己身材的自恋式要求；与后文“我没有腹肌吗？”的误会连续。 |
## `sam_stall.rpy` 更衣隔间、成熟形象与拟声

| 英文 | 推荐中文 | 说明 |
|---|---|---|
| `MILF`（Anon 对成熟女性的性化称呼） | 性感熟女 | 作为 Anon 对成熟女性的色情化类型判断；若剧情未确认母亲或婚姻身份，不擅自译成“人妻／妈妈” |
| `{i}*Hurk*{/i}` | `{i}*呃唔*{/i}` | 被物体击中、噎住或受压时的短促闷哼；保留斜体标签与星号，和 `ano01.rpy` 统一 |
## 学校公共区域与设施

| 英文 | 推荐中文 | 说明 |
|---|---|---|
| `utility closet` | 杂物间 | 学校走廊内存放工具、清洁用品或设备的小房间；与 `mel05.rpy` 统一，不译成售卖杂货的“杂货间” |
| `automated keypad lock` | 电子密码锁 | `school_office2.rpy` 中 Tori 办公室门上的键盘式门锁；`automated` 表示电子门禁装置，不生硬译成“自动密码锁” |
| `key code` / `code`（Tori办公室门锁） | 门禁密码 | 与 `tor01.rpy`、`note_tori.rpy` 的潜入任务连续；不要误译为“钥匙密码／关键密码” |
| public-address announcement / `pa` | 校内广播 | `school_pa.rpy` 的 23 条随机校园广播；保持正式播报腔与荒诞内容之间的反差 |
| public display of affection / `PDA` | 公开亲热 | 指在公共场合搂抱、亲吻等亲密行为；广播下一句直接升级到手和生殖器，不能弱化成普通“示爱” |
| `main office`（学校） | 校务办公室 | 学生、失物和紧急情况集中处理处；不同于 Ursula 的私人校长办公室 |
| `Conda Hivic` | `Conda Hivic` | 虚构车型名，影射 Honda Civic；保持英文拼写，不音译成“康达·海威克” |
| `chili`（食堂菜品） | 辣味肉酱 | 美式浓稠豆肉炖菜；`school_pa.rpy` 的食物中毒笑点中不能按字面译“辣椒” |
| `jockstrap` | 护裆 | 男性运动护具；`extra extra small jockstrap` 译“超超小号护裆”，保留尺寸羞辱笑点 |

## `tony.rpy` 披萨店日常入口与菜单用语

| 英文表达 | 统一译法 | 说明 |
|---|---|---|
| `Trial.`（Tony 菜单） | 试送 | 指 `ano07.rpy` 正式录用前的披萨送餐测试，不译成泛化的“试试” |
| `Vehicle.`（Tony 菜单） | 车子 | 指 `ano09.rpy` 中 Anon 买到的送餐车辆，可能为踏板车或汽车，不限定成某一种车型 |
| `There's my guy!` | 我的好小子来了 | Tony 对 Anon 的粗犷长辈式欢迎，不写成字面亲兄弟或现代“哥们”腔 |
| `She's a peach, ain't she?` | 她可真是个宝，对吧？ | Tony 对 Maria 的赞美，与 `ton_baby.rpy` 统一，不只泛化为“她是个好人” |

## Debbie 家车库工具与父亲遗物

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `Dad's old drill` / `old drill of Dad's` | 爸爸以前用的那把旧电钻／爸爸那把旧电钻 | 指 Anon 已故父亲留在 Debbie 家车库架上的充电式电钻；名词 `drill` 应译“电钻”，不能误作仅指钻头的“钻头” |
| `The batteries are still charged too.` | 电池居然也还有电 | Anon 发现旧工具仍能使用时的轻微惊喜；`charged` 指电池仍有电，不是已经完成新一轮充电 |

## Diane 菜园任务与车库铲子

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `shovel`（Diane 菜园任务） | 铲子 | 指 Debbie 家车库取得、用于替换 Diane 断掉旧铲子的完整园艺工具；与电钻、钻头等其他工具区分，不漂移为“铁锹” |
| `One shovel: acquired!` | 铲子一把，入手！ | 尚未见过 Diane 时的游戏式物品取得自言自语，不是正式系统提示 |
| `busting your ass for Diane` | 替 Diane 累死累活 | Jenny 嘲笑 Anon 在炎热天气做园艺体力活，不是为 Diane“卖命”或遭受暴力 |

## 电视新闻与频道讽刺

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `perp walk` | 被押走时的样子／押解示众 | 指嫌犯戴着手铐在媒体镜头前被警方押走的公开画面；`tv.rpy` 中 Anon 嘲笑 Ronald 被捕时仍“挺有派头”，不能误译成警察“出警走姿” |
| `give a press conference from jail` | 在监狱里开新闻发布会 | Ronald 因腐败被捕后仍穿囚服面对媒体讲话的荒诞新闻画面，保留 Anon 连续两句的惊讶和讽刺 |
| `get into`（观看沙滩排球） | 对……感兴趣 | Anon 看到女子沙滩排球转播后表达观看兴趣和性吸引，不是说自己要下场“参与”运动 |


## `tym_stall.rpy` 更衣隔间涂鸦与掩饰口吻

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `You saw nothing, bro.` | 你什么都没看见，哥们儿。 | Tyme 被 Anon 撞见拿记号笔在更衣隔间内涂写后，尴尬地要求对方装作没看见；`bro` 是同龄陌生人间的随口称呼，不译成正式的“兄弟”。 |
| `work up the courage to write` | 鼓足勇气写下…… | Anon 根据 Tyme 犹豫涂写的动作作出的猜测；强调下笔前的胆怯，不是“努力完成写作”或正式写文章。 |

## `ang.rpy` 教堂用语与任务材料

| 英文 | 当前处理 | 说明 |
|---|---|---|
| house of our lord | 主的殿堂 | Angela 的庄重宗教欢迎语，不按字面写成“我主的房子” |
| unburden yourself | 卸下心中重担 | 暗含向神职人员倾诉／告解；Anon 离开时用中文双引号重复，保留局促感 |
| Go with God, child. | 愿上帝与你同在，孩子。 | 教堂送别语，保持温和、年长的神职口吻 |
| linens（教堂艺术任务） | 亚麻布／白色亚麻布 | `ang.rpy` 菜单使用简写“亚麻布”；`bar05.rpy` 具体对话说明实际取得的是旧白色洗礼袍，用作学校艺术项目的画布材料 |

## `ari_stall.rpy` 更衣隔间俚语与成人指代

| 英文 | 当前处理 | 说明 |
|---|---|---|
| Holy hand grenades, Batman! | 神圣手榴弹啊，Batman！ | Anon 看到 Ariane 胸部时的混搭式夸张惊叹；`Batman` 保持英文专名 |
| those are marvelous | 这对奶子也太赞了吧 | `those` 明确指 Ariane 裸露的双乳，成人内容不得模糊成“那些东西” |
| booth（泳池更衣区） | 隔间 | 指带门的更衣隔间，不是座位、摊位或售货亭 |
| No shit, Sherlock. | 这还用你说，Sherlock。 | 尖刻表达“这不是废话吗”；`Sherlock` 保持英文专名，不汉化为福尔摩斯 |
| show off the goods | 展示身体／露给人看 | `the goods` 暗指 Ariane 的胸部和身体；按句法自然展开，不译成普通商品展示 |
| smooth（搭讪） | 搭讪顺利／搭讪漂亮 | `that wasn't exactly smooth` 是 Anon 自嘲刚才的接近方式很失败，不是动作不流畅 |

## `bar01.rpy` 美术课与比赛起点

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `slab of clay` | 一块陶土 | Barbara 课前让学生领取的塑形材料；不误译成已有板状形态的“黏土板／泥板” |
| `align our chakras` | 调整脉轮 | Barbara 的嬉皮式课前冥想用语，保留其神秘主义教师口吻 |
| `the mayor's art contest` | 市长举办的美术比赛／市长美术比赛 | Ronald 举办、第一名奖金一千美元的比赛；是 Barbara 美术线贯穿任务，不漂移为抽象“艺术竞赛” |
| `quack`（Ursula 骂 Barbara） | 江湖骗子 | Ursula 嘲讽 Barbara 的冥想与脉轮教学不靠谱，不是普通“蠢货” |
| `Yes, ma'am.`（Anon 对 Barbara） | 好的，老师。 | 师生课堂语境按身份自然处理；不生硬译“女士” |

## `bar02.rpy` 美术搭档、画板任务与专名

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `art pad` / `artpad` | 画板 | 指夹纸绘画用的便携画板；同一任务中不得漂移成“画册” |
| `cutie pie`（Barbara 对 Mia） | 小可爱 | Barbara 对 Mia 的热情亲昵称呼；本阶段含欣赏与轻度调情，但不能提前写成稳定成人关系 |
| `Starchild` | Starchild | Barbara 过去追随乐队时结识的女性朋友专名，保持英文，不译“星孩” |
| `Praia do Abricó` | Praia do Abricó | Rio de Janeiro 的天体海滩专名，保持原文拼写 |
| `Rio de Janeiro` | Rio de Janeiro | Barbara 的巴西老家，保持英文专名 |
| `My sneak could be one hundred` | 就算我的潜行技能满级 | Anon 面对走廊储物柜时的电子游戏属性笑话，保留 RPG 语感 |

## `bar03.rpy` 拼贴课、图书馆与成人双关

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `collage` | 拼贴画 | Barbara 第二次双人美术课的核心作品；Anon 把 `collage` 听成 `college`，中文用“拼贴画／大学”保留误听笑点 |
| `function room`（图书馆） | 多功能室 | 图书馆存放旧杂志的房间；同一任务不得漂移为“宴会厅／功能室” |
| `special brownies` | 特制布朗尼 | Barbara 烤给 Melody 的含蓄成人笑点，保留 `special` 的暗示，不在原文未明说时直接补成“大麻布朗尼” |
| `gag reflex` | 反胃反射／呕吐反射 | 肛门笑话中用“反胃反射”保留荒诞感；Barbara 讲自己受训克服时用常见医学表达“呕吐反射” |
| `quinoa` | 藜麦 | Barbara 课后建议 Anon 购买的健康食品，后续任务保持统一 |

## `bar04.rpy` 裸模课、画架与课堂称谓

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| `easel` | 画架 | Barbara 裸模写生课使用的木制画架；包括旧画架和 Anon 制作的新画架，不译成“支架” |
| `charcoal`（素描工具） | 炭笔 | 裸模写生时用于绘画的炭笔／炭条；按课堂动作写“拿出炭笔”，不误成普通木炭 |
| `special brownies`（裸模课） | 特制布朗尼 | 与 `bar03.rpy` 保持一致；学生食用后明显兴奋、眩晕和放松，但不在原文未明说时擅自补写成“大麻布朗尼” |
| `Yes, ma'am.`（学生对 Barbara） | 好的，老师。 | 保留师生课堂身份；学生对 Ursula 服从时则按其身份译“校长” |

## 本轮收尾统一补充

| 英文／标识 | 推荐中文 | 说明 |
|---|---|---|
| Cuntech | Cuntech | 虚构科技公司专名，保持英文原状，不音译、不汉化；所有格和中文助词直接接在英文后。 |
| talent show | 才艺表演 | 学校活动名称全仓统一为“才艺表演”，不写成“才艺秀”“天赋表演”或“表演赛”。 |
| faptic engine | 触觉引擎 | Tori／Erik 科技线的固定术语；统一使用“触觉引擎”，不再混用“触感引擎”或“Faptic引擎”。 |
| key code | 门禁密码 | Tori 办公室电子锁所需的密码；与万能钥匙、密码纸条的剧情功能区分。 |
| traditional tanto | 传统的短刀 | Hana 线中的日式短刀，不译成“胁差”；Hana 为女性，Hana-san 按场景使用“小姐”等合适称谓。 |
| Bubbles | Bubbles | CineSaga Theater 店员的英文昵称／姓名，保持英文，不译成“泡泡”。 |
| babyface | 小帅哥 | Tina 对 Anon 的固定亲昵称呼；非称呼语境仍按句意处理。 |
| sugar（Melody 对 Anon） | 甜心 | Melody 后期成人关系中的固定称呼；不与 Sugar Tats 或 sugar daddy 等普通词组混用。 |

Tori 血清线的关系阶段必须保持清晰：第一种血清让 Ursula 不再反对实验，但鸡汤基底造成母鸡副作用；第二种血清用于处理 Tori 的低性欲／无性欲状态。只有后者完成后，Anon 与 Tori 才进入明确的成人关系，不能把两种血清的作用或时间顺序混写。

## bytecode_strings / sms_fix 本轮确认

| 英文 | 中文 | 说明 |
|---|---|---|
| camming career | 直播事业 | Jenny 的成人直播副业；不译为“摄像头事业”。 |
| camshow / camshows | 成人直播 | 带色情表演语境时使用；`on stream` 译为“在直播中”。 |
| chat（成人直播语境） | 直播间观众 | 指观看直播并留言的观众群体。 |
| deprive ... of attention | 冷落…… | 任务条件是暂时不理会角色，不是吸引注意。 |
| foul play（调查语境） | 人为犯罪／他杀迹象 | 不译为“犯规行为”。 |
| The Electro Clit / ElectroClit | 电击阴蒂棒 | Pink 出售的情趣玩具；轻量版为“电击阴蒂棒轻量版”。 |
| Bad Monster | 坏怪物 | Pink 出售的大型情趣玩具名称。 |
| cookie jar | 角色图鉴 | 解锁角色图鉴变体或场景。 |
| Half wind-relieving pose | 半排气式 | 瑜伽姿势名称。 |
| Outlood Express | Outlood快递 | 游戏中的恶搞专名，保留 `Outlood`。 |
| Waning Crescent / Waxing Crescent / Third Quarter | 残月／娥眉月／下弦月 | 月相 UI 统一译法。 |
| Gym. | 体育馆 | 本项目中学校场景既有译法；不机械改为“健身房”。 |


## 跨行断句精修专项（2026-08-06）

| 英文表达 | 推荐中文 | 说明 |
|---|---|---|
| Your big... / ... Thing. | 你的……／……大家伙。 | Debbie 直播场景中的欲言又止；中文合并后应为“你的……大家伙”，不能译成“你的大家伙……的东西”。 |
| desirable（Debbie 直播自述） | 很有魅力 | Debbie 说自己因 Anon 的谈论而重新感到有吸引力；不译成对外施加意味的“令人渴望”。 |
| bearing down ... at the end | 可真用力……／尤其是最后那一下 | Tina 高潮时身体用力的性爱语境；at the end 指“尤其是最后那一下”，不是“结束了”。 |
| Something... Priceless!! | 一件……／……无价之宝！！ | Maria 对 Anon 带给家庭的意义表示感谢；用量词“一件”使跨行名词结构自然衔接。 |
| My brain's... not really... | 我的脑子……还没转过来…… | Tina 性行为后的余韵表达；补足中文谓语，避免“我的脑子……还没……操，真爽”的悬空句。 |


## Vivienne 法语教学线第三语言显示

| 法语原文／标识 | 推荐中文释义 | 使用规则 |
|---|---|---|
| `Merci beaucoup` | 非常感谢 | 无 `show_lang` 时保留法语并在全角括号内补中文释义。 |
| `Oui` / `Oui!` / `Oui?` | 是的／对／嗯？ | 按语气翻译；无 `show_lang` 时保留法语原文并加括号释义。 |
| `Magnifique` | 太棒了 | Vivienne 夸奖学生或作品时使用；菜单字符串同样保留法语原文。 |
| `Vraiment?` | 真的吗？ | 表示惊讶或确认，不弱化问号和感叹号语气。 |
| `D'accord, OK, je suis désolé!` | 好、好，我错了！ | Vivienne 挨罚时的道歉；无 `show_lang` 的菜单字符串保留法语并加中文释义。 |
| `Ow, ça fait mal!` | 哎哟，好痛！ | Vivienne 受罚时的疼痛反应；带 `show_lang` 时主对白只显示中文。 |
| `Pas plus!` | 别再打了！ | Vivienne 请求 Ursula 停手；带 `show_lang` 时主对白只显示中文。 |
| `Connasse!` | 你个贱货！ | Vivienne 对 Ursula 的失控辱骂；带 `show_lang` 时主对白只显示中文。 |
| `mon bel homme` / `jeune homme` | 我的帅哥／小伙子 | Vivienne 对 Anon 的法语亲昵称呼，按关系阶段保留暧昧程度。 |

## 第三语言呈现规则与术语

- 无 `show_lang`：保留第三语言原文，并在后面用全角括号补充中文释义。
- 有 `show_lang`：主对白只保留自然中文；第三语言文本保留在 `show_lang` 中。

### 通用第三语言词汇

- `Oui`：是的／对／是呀（按语境）
- `Bonjour`：你好
- `Au revoir`：再见
- `C'est la vie`：人生就是这样
- `capisce`：懂了没
- `prosciutto`：意式风干火腿
- `gorgonzola`：戈贡佐拉奶酪
- `capicola`：卡皮科拉火腿
- `Irasshaimase`：欢迎光临
- `Arigatō gozaimashita`：非常感谢
- `hajimemashite`：初次见面
- `piña colada`：椰林飘香
- `Crèche`：育幼院
- `bicyclette`：自行车
- `fromage`：奶酪
