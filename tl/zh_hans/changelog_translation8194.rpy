# Translate the bundled game changelog at display time, retaining native layout.
# Unknown entries fall back to English; never replace saga.menu.logs or game data.
init -1 python:
    import re as _ssct_logs_re

    def _ssct_changelog_translation(source):
        return renpy.translate_string(source + '{#ssct_changelog}').removesuffix('{#ssct_changelog}')

    def _ssct_changelog_text(content):
        result = []
        for line in content.splitlines(True):
            body = line.rstrip('\r\n')
            ending = line[len(body):]
            if body.startswith('- '):
                body = _ssct_changelog_translation(body)
            elif body.startswith('{=logs_menu_group}'):
                body = _ssct_logs_re.sub(r'\b(Preview|Hotfix)(?= \d)', lambda match: _ssct_changelog_translation(match.group(1)), body)
            result.append(body + ending)
        return ''.join(result)

init 1:
    screen logs():
        style_prefix 'logs_menu' tag menu


        default keys = saga.menu.logs.keys()
        default log = next(iter(saga.menu.logs))
        default scroll = ui.adjustment()

        use base_menu():
            side 't c':

                label _('Changelog')

                vbox:
                    hbox:
                        for v in keys:
                            textbutton v action (SetScreenVariable('log', v),
                                             Function(scroll.change , 0))
                        textbutton _('Older') action SetScreenVariable('log', None)

                    viewport:
                        draggable True
                        mousewheel True
                        scrollbars 'vertical'
                        yadjustment scroll

                        if log:
                            text _ssct_changelog_text(saga.menu.logs[log]) substitute False
                        else:
                            text _('Older changelog entries can be found on the '
                               'official wiki.')



translate zh_hans strings:

    # game/changelog.txt:5
    old "- Fixed a handful of issues where Josie would turn invisible when buying vehicles.{#ssct_changelog}"
    new "- 修复了购买车辆时Josie会变得不可见的若干问题。{#ssct_changelog}"

    # game/changelog.txt:6
    old "- Expanded the mall with a coffee shop, security office and rooftop.{#ssct_changelog}"
    new "- 扩建商场，新增咖啡店、保安室和屋顶区域。{#ssct_changelog}"

    # game/changelog.txt:11
    old "- Restored Josie's mini route with four upgraded quests.{#ssct_changelog}"
    new "- 恢复Josie的短支线，包含四个升级后的任务。{#ssct_changelog}"

    # game/changelog.txt:12
    old "- Created an original animation as part of a quest upgrade and restored four more.{#ssct_changelog}"
    new "- 在任务升级中新增一段原创动画，并恢复另外四段动画。{#ssct_changelog}"

    # game/changelog.txt:13
    old "- Inserted a button for Jiang the mechanic in the garage of the dealership.{#ssct_changelog}"
    new "- 在车行车库中加入机械师Jiang的交互按钮。{#ssct_changelog}"

    # game/changelog.txt:14
    old "- Added more unlockable characters for the contacts app in Anon's phone.{#ssct_changelog}"
    new "- 为Anon手机的联系人应用增加更多可解锁角色。{#ssct_changelog}"

    # game/changelog.txt:15
    old "- Enabled option to play preview mode without money boost for players that want it.{#ssct_changelog}"
    new "- 新增选项，让有需要的玩家可以在不获得额外金钱的情况下游玩预览模式。{#ssct_changelog}"

    # game/changelog.txt:16
    old "- Improved the car dealership with crowd art for all times of day.{#ssct_changelog}"
    new "- 完善车行在一天中各个时段的人群美术。{#ssct_changelog}"

    # game/changelog.txt:17
    old "- Displayed the price of shop items alongside option to add them to the basket.{#ssct_changelog}"
    new "- 在将商品加入购物篮的选项旁显示价格。{#ssct_changelog}"

    # game/changelog.txt:18
    old "- Reworked text message system to support bidirectional and photo messaging.{#ssct_changelog}"
    new "- 重做短信系统，支持双向收发和图片消息。{#ssct_changelog}"

    # game/changelog.txt:19
    old "- Fixed missing pregnancy wheel and replay unlocks for Maria's bedroom scenes.{#ssct_changelog}"
    new "- 修复Maria卧室场景缺少受孕转盘和回放解锁的问题。{#ssct_changelog}"

    # game/changelog.txt:20
    old "- Stopped Tony temporarily not showing in afternoon variant of Maria's couch scene.{#ssct_changelog}"
    new "- 修复Maria沙发场景的下午变体中Tony暂时不显示的问题。{#ssct_changelog}"

    # game/changelog.txt:21
    old "- Expanded support for animation modes in x-ray system.{#ssct_changelog}"
    new "- 扩展透视系统对动画模式的支持。{#ssct_changelog}"

    # game/changelog.txt:22
    old "- Reduced clutter in replay menus by hiding some minor variants until unlocked.{#ssct_changelog}"
    new "- 在解锁前隐藏部分细微变体，减少回放菜单中的杂乱条目。{#ssct_changelog}"

    # game/changelog.txt:23
    old "- Corrected long-standing scheduling issue in Debbie's car repair quest.{#ssct_changelog}"
    new "- 修正Debbie修车任务中长期存在的日程安排问题。{#ssct_changelog}"

    # game/changelog.txt:24
    old "- Various typo, text-to-speech, and posing fixes.{#ssct_changelog}"
    new "- 修复多处拼写、文字转语音和角色姿势问题。{#ssct_changelog}"

    # game/changelog.txt:29
    old "- Created a new event for Maria in the pizzeria pantry in the evening.{#ssct_changelog}"
    new "- 为Maria新增晚间披萨店储藏室事件。{#ssct_changelog}"

    # game/changelog.txt:30
    old "- Reimagined Maria's apartment bedroom scene and restored it.{#ssct_changelog}"
    new "- 重新设计并恢复Maria公寓卧室场景。{#ssct_changelog}"

    # game/changelog.txt:31
    old "- Restored Maria's blowjob scene and expanded it to be possible during pregnancy.{#ssct_changelog}"
    new "- 恢复Maria的口交场景，并扩展为孕期也可触发。{#ssct_changelog}"

    # game/changelog.txt:32
    old "- Finished the full version of Maria's couch scenes.{#ssct_changelog}"
    new "- 完成Maria沙发场景的完整版本。{#ssct_changelog}"

    # game/changelog.txt:33
    old "- Improved passive parts of Maria's pregnancy cycle to be more context-aware.{#ssct_changelog}"
    new "- 改进Maria怀孕周期中的被动事件，使其更符合当前情境。{#ssct_changelog}"

    # game/changelog.txt:34
    old "- Added a new Maria button in her bedroom for Sunday afternoons.{#ssct_changelog}"
    new "- 新增Maria在星期日下午出现在卧室时的交互按钮。{#ssct_changelog}"

    # game/changelog.txt:35
    old "- Reintroduced fleshed-out random changing room encounters with nine to find.{#ssct_changelog}"
    new "- 恢复内容更丰富的更衣室随机邂逅，共有九种可发现的事件。{#ssct_changelog}"

    # game/changelog.txt:36
    old "- Completed reimplementation of Miss Dewitt's content.{#ssct_changelog}"
    new "- 完成Dewitt老师内容的重新实现。{#ssct_changelog}"

    # game/changelog.txt:37
    old "- Adapted and enabled Tina's pregnancy cycle and broken A/C event.{#ssct_changelog}"
    new "- 适配并启用Tina的怀孕周期和空调故障事件。{#ssct_changelog}"

    # game/changelog.txt:38
    old "- Replaced remnants of old Anon art throughout Jenny's route.{#ssct_changelog}"
    new "- 替换Jenny支线中残留的旧版Anon美术。{#ssct_changelog}"

    # game/changelog.txt:39
    old "- Built a new stairwell for the mall in preparation for future content.{#ssct_changelog}"
    new "- 为商场新增楼梯间，为后续内容做准备。{#ssct_changelog}"

    # game/changelog.txt:40
    old "- Gifted Eve a cute pair of cat ears for use during the karaoke event.{#ssct_changelog}"
    new "- 给Eve准备了一对可爱的猫耳，用于卡拉OK事件。{#ssct_changelog}"

    # game/changelog.txt:41
    old "- Provided a Cyclone poster inventory item to collect in Jenny's route.{#ssct_changelog}"
    new "- 在Jenny支线中加入可收集的Cyclone海报物品。{#ssct_changelog}"

    # game/changelog.txt:42
    old "- Reworked assets for Jiang to bring the character up to current standards.{#ssct_changelog}"
    new "- 重做Jiang的美术资源，使角色达到当前制作标准。{#ssct_changelog}"

    # game/changelog.txt:43
    old "- Updated crowd assets on the dealership forecourt to current standards.{#ssct_changelog}"
    new "- 将车行前院的人群美术更新至当前标准。{#ssct_changelog}"

    # game/changelog.txt:44
    old "- Opened a penguin sanctuary in the ground floor corridor of the apartment complex.{#ssct_changelog}"
    new "- 在公寓楼一层走廊开设企鹅保护区。{#ssct_changelog}"

    # game/changelog.txt:45
    old "- Included Tammy's evening yoga in her bedroom in the cookie jar.{#ssct_changelog}"
    new "- 将Tammy晚间在卧室做瑜伽的场景加入角色图鉴。{#ssct_changelog}"

    # game/changelog.txt:46
    old "- Began work on phone improvements, starting with emojis, with more to follow.{#ssct_changelog}"
    new "- 开始改进手机功能，首先加入表情符号，后续还将继续扩展。{#ssct_changelog}"

    # game/changelog.txt:47
    old "- Tweaked how some scenes are displayed in the cookie jar to reduce clutter.{#ssct_changelog}"
    new "- 调整角色图鉴中部分场景的显示方式，减少菜单杂乱。{#ssct_changelog}"

    # game/changelog.txt:48
    old "- Rescued players trapped in the bank from saves made prior to wip.7712.{#ssct_changelog}"
    new "- 修复在wip.7712之前保存的存档中玩家被困在银行的问题。{#ssct_changelog}"

    # game/changelog.txt:49
    old "- Addressed some broken posing when speaking to Debbie by the pool.{#ssct_changelog}"
    new "- 修复在泳池边与Debbie交谈时的部分角色姿势错误。{#ssct_changelog}"

    # game/changelog.txt:50
    old "- Prevented early release of Debbie when she's shunning Anon.{#ssct_changelog}"
    new "- 防止Debbie躲着Anon时过早解除回避状态。{#ssct_changelog}"

    # game/changelog.txt:51
    old "- Usual miscellaneous detritus of various typo fixes, art quirks and metadata.{#ssct_changelog}"
    new "- 修复其他多处拼写、美术细节和元数据问题。{#ssct_changelog}"

    # game/changelog.txt:56
    old "- Addressed issue where owning a car prior to Tony's suggestion would break Tina.{#ssct_changelog}"
    new "- 修复在Tony提出购车建议前已拥有车辆会导致Tina状态异常的问题。{#ssct_changelog}"

    # game/changelog.txt:57
    old "- Resolved issue with some of Maria's replays not being unlocked correctly.{#ssct_changelog}"
    new "- 解决Maria的部分回放未正确解锁的问题。{#ssct_changelog}"

    # game/changelog.txt:58
    old "- Fixed Anon's face temporarily going missing when visiting Tina in her apartment.{#ssct_changelog}"
    new "- 修复拜访公寓里的Tina时Anon的脸部暂时消失的问题。{#ssct_changelog}"

    # game/changelog.txt:59
    old "- Inserted small guidance dialogue that was missed in the repeatable pantry event.{#ssct_changelog}"
    new "- 补上可重复储藏室事件中遗漏的简短引导对话。{#ssct_changelog}"

    # game/changelog.txt:60
    old "- Ensured babies held by Maria and Tony match between navigation and dialogue.{#ssct_changelog}"
    new "- 确保Maria和Tony抱着的宝宝在导航画面与对话画面中保持一致。{#ssct_changelog}"

    # game/changelog.txt:61
    old "- Added missing handprint to Maria's dress in the lead-in to her kitchen scene.{#ssct_changelog}"
    new "- 补上Maria厨房场景开始前连衣裙上缺失的手印。{#ssct_changelog}"

    # game/changelog.txt:66
    old "- Resumed main story route with two reworked, and three upgraded quests.{#ssct_changelog}"
    new "- 继续恢复主线，加入两个重做任务和三个升级任务。{#ssct_changelog}"

    # game/changelog.txt:67
    old "- Added two original scenes (for Tina and Maria), and upgraded four more.{#ssct_changelog}"
    new "- 新增Tina和Maria各一段原创场景，并升级另外四段场景。{#ssct_changelog}"

    # game/changelog.txt:68
    old "- Refined x-ray animation system and added it to all existing sex scenes.{#ssct_changelog}"
    new "- 改进透视动画系统，并将其加入所有现有性爱场景。{#ssct_changelog}"

    # game/changelog.txt:69
    old "- Introduced three placeholder narrative events on which to build in future.{#ssct_changelog}"
    new "- 加入三个临时叙事事件，为后续内容打下基础。{#ssct_changelog}"

    # game/changelog.txt:70
    old "- Enhanced character art of Kassy, Lily, Maria, Micoe, Roz, Tina, and Tony.{#ssct_changelog}"
    new "- 改进Kassy、Lily、Maria、Micoe、Roz、Tina和Tony的角色美术。{#ssct_changelog}"

    # game/changelog.txt:71
    old "- Rescaled some aspects of Zana to be more consistent across his character.{#ssct_changelog}"
    new "- 调整Zana部分美术的尺寸，使角色各处比例更加一致。{#ssct_changelog}"

    # game/changelog.txt:72
    old "- Tweaked face art for Missy, Jenny, Debbie, and Josie.{#ssct_changelog}"
    new "- 微调Missy、Jenny、Debbie和Josie的面部美术。{#ssct_changelog}"

    # game/changelog.txt:73
    old "- Inserted non-quest related buttons for Liu at the bank and Micoe at the hospital.{#ssct_changelog}"
    new "- 为银行的Liu和医院的Micoe加入与任务无关的交互按钮。{#ssct_changelog}"

    # game/changelog.txt:74
    old "- Reworked crowds in apartment complex, hospital, mall and pizza shop.{#ssct_changelog}"
    new "- 重做公寓楼、医院、商场和披萨店的人群美术。{#ssct_changelog}"

    # game/changelog.txt:75
    old "- Improved details in comic shop, library, recovery room and town map backgrounds.{#ssct_changelog}"
    new "- 完善漫画店、图书馆、休养室和小镇地图的背景细节。{#ssct_changelog}"

    # game/changelog.txt:76
    old "- Revisited art for the conclusion of Debbie's evening scene in the kitchen.{#ssct_changelog}"
    new "- 重新打磨Debbie晚间厨房场景结尾的美术。{#ssct_changelog}"

    # game/changelog.txt:77
    old "- Updated art for playing the pizza delivery mini game in the evening.{#ssct_changelog}"
    new "- 更新晚间披萨配送小游戏的美术。{#ssct_changelog}"

    # game/changelog.txt:78
    old "- Restored the PA system announcements in the school.{#ssct_changelog}"
    new "- 恢复学校广播系统的公告。{#ssct_changelog}"

    # game/changelog.txt:79
    old "- Split layout of busy replay menus to be more easily digestible.{#ssct_changelog}"
    new "- 拆分内容较多的回放菜单，使其更易浏览。{#ssct_changelog}"

    # game/changelog.txt:80
    old "- Restaged door knock actions in the apartment complex to match layout.{#ssct_changelog}"
    new "- 重新安排公寓楼的敲门动作，使其符合场景布局。{#ssct_changelog}"

    # game/changelog.txt:81
    old "- Polished dialogue in first three quests of Jenny's route.{#ssct_changelog}"
    new "- 精修Jenny支线前三个任务的对话。{#ssct_changelog}"

    # game/changelog.txt:82
    old "- Gave Maria's bedroom closet a viewable interior.{#ssct_changelog}"
    new "- 让Maria卧室的衣柜内部可以查看。{#ssct_changelog}"

    # game/changelog.txt:83
    old "- Brought back Anon's employee-of-the-month plaque in the pizzeria.{#ssct_changelog}"
    new "- 恢复披萨店中Anon的月度最佳员工奖牌。{#ssct_changelog}"

    # game/changelog.txt:84
    old "- Crossed sex toys acquired by Jenny off the wish list on her computer.{#ssct_changelog}"
    new "- Jenny购入性玩具后，会从电脑上的愿望清单中划掉对应条目。{#ssct_changelog}"

    # game/changelog.txt:85
    old "- Resolved long standing reservation bug in Jenny's cinema event.{#ssct_changelog}"
    new "- 解决Jenny电影院事件中长期存在的预订错误。{#ssct_changelog}"

    # game/changelog.txt:86
    old "- Replaced random dialogue loops in lewd scenes with narrative driven progression.{#ssct_changelog}"
    new "- 将成人场景中的随机对话循环替换为由叙事推动的流程。{#ssct_changelog}"

    # game/changelog.txt:87
    old "- Revisited art of Jenny's breakfast table event to add Anon's t-shirt for continuity.{#ssct_changelog}"
    new "- 重新打磨Jenny早餐桌事件的美术，加入Anon的T恤以保持前后连贯。{#ssct_changelog}"

    # game/changelog.txt:88
    old "- Expanded text-to-speech coverage for clickable items.{#ssct_changelog}"
    new "- 扩展可点击物品的文字转语音覆盖范围。{#ssct_changelog}"

    # game/changelog.txt:89
    old "- Captured pregnancy state of Jenny when unlocking her wet t-shirt bathroom scene.{#ssct_changelog}"
    new "- 解锁Jenny浴室湿T恤场景时记录她的怀孕状态。{#ssct_changelog}"

    # game/changelog.txt:90
    old "- Created more variants for flies in the science lab and dirt in the forest.{#ssct_changelog}"
    new "- 为科学实验室的苍蝇和森林中的泥土增加更多变体。{#ssct_changelog}"

    # game/changelog.txt:91
    old "- Increased image cache size to prevent fighting in particularly busy scenes.{#ssct_changelog}"
    new "- 增大图像缓存，避免复杂场景中的缓存资源相互挤占。{#ssct_changelog}"

    # game/changelog.txt:92
    old "- Restructured various labels to be consistent in how we name and use variables.{#ssct_changelog}"
    new "- 重构多个脚本标签，统一变量的命名和使用方式。{#ssct_changelog}"

    # game/changelog.txt:93
    old "- Upgraded Ren'Py to version 8.5.3.{#ssct_changelog}"
    new "- 将Ren'Py升级至8.5.3版。{#ssct_changelog}"

    # game/changelog.txt:94
    old "- Squashed various continuity issues and typos.{#ssct_changelog}"
    new "- 修复多处前后连贯性问题和拼写错误。{#ssct_changelog}"

    # game/changelog.txt:95
    old "- Various replay system tweaks and fixes.{#ssct_changelog}"
    new "- 对回放系统进行多项微调和修复。{#ssct_changelog}"

    # game/changelog.txt:100
    old "- Fixed exceptions in Mia and Tammy's replay menus.{#ssct_changelog}"
    new "- 修复Mia和Tammy回放菜单中的异常。{#ssct_changelog}"

    # game/changelog.txt:105
    old "- Created two completely new repeatable events for Debbie in the lobby and backyard.{#ssct_changelog}"
    new "- 为Debbie新增两个可重复事件，分别发生在门厅和后院。{#ssct_changelog}"

    # game/changelog.txt:106
    old "- Expanded Debbie catching Anon watching porn on TV event with multiple lewd variants.{#ssct_changelog}"
    new "- 扩展Debbie撞见Anon在电视上看色情片的事件，加入多个成人内容变体。{#ssct_changelog}"

    # game/changelog.txt:107
    old "- Allowed Debbie to visit Anon's room at night if she's pent up, even when pregnant.{#ssct_changelog}"
    new "- Debbie欲求不满时可在夜间拜访Anon的房间，孕期也可以。{#ssct_changelog}"

    # game/changelog.txt:108
    old "- Added small optional bonus scene to Debbie and Anon's first trip to Cupid.{#ssct_changelog}"
    new "- 在Debbie与Anon首次前往丘比特时加入一段可选的额外小场景。{#ssct_changelog}"

    # game/changelog.txt:109
    old "- Restored foreplay frames omitted during build up with Debbie in Anon's bed.{#ssct_changelog}"
    new "- 恢复与Debbie在Anon床上亲热时遗漏的前戏画面。{#ssct_changelog}"

    # game/changelog.txt:110
    old "- Introduced a new button for Debbie in the lobby, fully integrated with her story.{#ssct_changelog}"
    new "- 在门厅为Debbie新增交互按钮，并完整接入她的剧情。{#ssct_changelog}"

    # game/changelog.txt:111
    old "- Extended Debbie's backyard button to make more sense after she gets a swimsuit.{#ssct_changelog}"
    new "- 扩展Debbie在后院的交互按钮，使其在获得泳装后更符合情境。{#ssct_changelog}"

    # game/changelog.txt:112
    old "- Distinguished replays new in the current update to aid discoverability.{#ssct_changelog}"
    new "- 标出当前更新新增的回放，方便玩家发现。{#ssct_changelog}"

    # game/changelog.txt:113
    old "- Rebuilt the replay system to better handle and highlight variants to players.{#ssct_changelog}"
    new "- 重建回放系统，更好地处理场景变体并向玩家突出显示。{#ssct_changelog}"

    # game/changelog.txt:114
    old "- Developed new centralised method for choice tracking during dialogue.{#ssct_changelog}"
    new "- 开发新的集中式对话选项记录方式。{#ssct_changelog}"

    # game/changelog.txt:115
    old "- Overhauled how NPC visits to Anon's room work to accommodate more than just Jenny.{#ssct_changelog}"
    new "- 重做NPC拜访Anon房间的机制，使其能够支持Jenny之外的更多角色。{#ssct_changelog}"

    # game/changelog.txt:116
    old "- Switched on tree house lights in a few backgrounds where they were off.{#ssct_changelog}"
    new "- 点亮此前部分背景中未亮起的树屋灯光。{#ssct_changelog}"

    # game/changelog.txt:117
    old "- Blocked sleeping in Debbie's bed while she is avoiding Anon.{#ssct_changelog}"
    new "- Debbie躲着Anon时，禁止在她的床上睡觉。{#ssct_changelog}"

    # game/changelog.txt:118
    old "- Fixed small issue with invisible Jenny in her second cam show scene.{#ssct_changelog}"
    new "- 修复Jenny第二次色情直播场景中的轻微不可见问题。{#ssct_changelog}"

    # game/changelog.txt:119
    old "- Prevented Jenny being invisible to the peephole in the week after she gives birth.{#ssct_changelog}"
    new "- 防止Jenny产后一周内在窥视孔画面中不可见。{#ssct_changelog}"

    # game/changelog.txt:120
    old "- Cleaned up staging issue in reminder dialogue for Jenny's first sex toy quest.{#ssct_changelog}"
    new "- 修正Jenny首次性玩具任务提醒对话中的场景安排问题。{#ssct_changelog}"

    # game/changelog.txt:121
    old "- Modified trigger in Pink Cyclone quest so as to not temporarily break shop system.{#ssct_changelog}"
    new "- 调整Pink Cyclone任务的触发条件，避免商店系统暂时异常。{#ssct_changelog}"

    # game/changelog.txt:122
    old "- Ensured Jenny will always put her back to the wall before inviting Anon to shower.{#ssct_changelog}"
    new "- 确保Jenny邀请Anon一起洗澡前总会先背靠墙壁。{#ssct_changelog}"

    # game/changelog.txt:123
    old "- Increased Jenny presence awareness in various Debbie events.{#ssct_changelog}"
    new "- 加强多个Debbie事件对Jenny是否在场的判断。{#ssct_changelog}"

    # game/changelog.txt:124
    old "- Moved Anon to correct position after deciding not to sleep in Jenny's bed.{#ssct_changelog}"
    new "- 决定不在Jenny床上睡觉后，将Anon移到正确位置。{#ssct_changelog}"

    # game/changelog.txt:125
    old "- Provided secondary trigger in Debbie's first mall trip to avoid conflict with Jenny.{#ssct_changelog}"
    new "- 在Debbie首次逛商场的事件中加入备用触发条件，避免与Jenny的事件冲突。{#ssct_changelog}"

    # game/changelog.txt:126
    old "- Stopped Debbie's mug from vanishing in some car repair quest dialogues.{#ssct_changelog}"
    new "- 防止Debbie的杯子在部分修车任务对话中消失。{#ssct_changelog}"

    # game/changelog.txt:127
    old "- Addressed missing dialogue in car repair quest when speaking to Josie in person.{#ssct_changelog}"
    new "- 补上修车任务中与Josie当面交谈时缺失的对话。{#ssct_changelog}"

    # game/changelog.txt:128
    old "- Patched problem where Debbie's arm would vanish too soon in some couch scenes.{#ssct_changelog}"
    new "- 修复部分沙发场景中Debbie的手臂过早消失的问题。{#ssct_changelog}"

    # game/changelog.txt:129
    old "- Rectified strange NPC behaviour after Debbie informs Anon she is pregnant.{#ssct_changelog}"
    new "- 修正Debbie告知Anon自己怀孕后NPC的异常行为。{#ssct_changelog}"

    # game/changelog.txt:130
    old "- Resolved issue with incompatible Anon rig layers in Debbie's shower event.{#ssct_changelog}"
    new "- 解决Debbie淋浴事件中Anon角色绑定图层不兼容的问题。{#ssct_changelog}"

    # game/changelog.txt:131
    old "- Swapped background used for Erik's karaoke party for better visual consistency.{#ssct_changelog}"
    new "- 替换Erik卡拉OK派对的背景，使视觉表现更加一致。{#ssct_changelog}"

    # game/changelog.txt:132
    old "- Adjusted various asset names for consistency and state representation.{#ssct_changelog}"
    new "- 调整多项资源名称，统一命名并更准确地表示状态。{#ssct_changelog}"

    # game/changelog.txt:133
    old "- Removed unintended background change during trips to Raven Hill.{#ssct_changelog}"
    new "- 移除前往渡鸦山时意外发生的背景切换。{#ssct_changelog}"

    # game/changelog.txt:134
    old "- Upgraded stat check when asking Debbie about kissing practice with a player choice.{#ssct_changelog}"
    new "- 将向Debbie询问接吻练习时的属性检查改为玩家选项。{#ssct_changelog}"

    # game/changelog.txt:135
    old "- Delayed escalation in Debbie mall event such that it aligns with her story content.{#ssct_changelog}"
    new "- 延后Debbie商场事件的进一步发展，使其与她的剧情进度一致。{#ssct_changelog}"

    # game/changelog.txt:136
    old "- Corrected error in internal lust adjustment after sex on counter top with Debbie.{#ssct_changelog}"
    new "- 修正与Debbie在台面上性爱后内部欲望值调整的错误。{#ssct_changelog}"

    # game/changelog.txt:137
    old "- Tweaked staging for scenes early in Debbie's story to match with later scenes.{#ssct_changelog}"
    new "- 微调Debbie支线前期场景的安排，使其与后续场景一致。{#ssct_changelog}"

    # game/changelog.txt:138
    old "- Solved the black screen \"pop\" previously present at the end of some replays.{#ssct_changelog}"
    new "- 解决部分回放结束时此前出现的黑屏闪跳。{#ssct_changelog}"

    # game/changelog.txt:139
    old "- Applied intended title font in character replay menus.{#ssct_changelog}"
    new "- 为角色回放菜单应用原本指定的标题字体。{#ssct_changelog}"

    # game/changelog.txt:140
    old "- Improved tooling used to streamline asset maintenance tasks.{#ssct_changelog}"
    new "- 改进工具，简化美术资源维护工作。{#ssct_changelog}"

    # game/changelog.txt:141
    old "- Strived to be more consistent in menu terminology and oft-repeated phrases.{#ssct_changelog}"
    new "- 进一步统一菜单术语和经常重复的短语。{#ssct_changelog}"

    # game/changelog.txt:142
    old "- Various typo fixes, hint clarifications, and rig metadata adjustments.{#ssct_changelog}"
    new "- 修复多处拼写错误，明确提示，并调整角色绑定元数据。{#ssct_changelog}"

    # game/changelog.txt:147
    old "- Expanded Debbie's mall trip event with many more variants and escalation.{#ssct_changelog}"
    new "- 扩展Debbie逛商场事件，加入更多变体和进一步发展的内容。{#ssct_changelog}"

    # game/changelog.txt:148
    old "- Installed the sleeping in Debbie's bed event with multiple escalating stages.{#ssct_changelog}"
    new "- 加入在Debbie床上睡觉的事件，包含多个逐步发展的阶段。{#ssct_changelog}"

    # game/changelog.txt:149
    old "- Continued restoring main story adding the pizza prep and mob visit quests.{#ssct_changelog}"
    new "- 继续恢复主线，加入制作披萨和黑帮来访任务。{#ssct_changelog}"

    # game/changelog.txt:150
    old "- Polished Jenny's lewd scene art, extending cum-shots and fixing small details.{#ssct_changelog}"
    new "- 打磨Jenny成人场景的美术，延长射精镜头并修复细节。{#ssct_changelog}"

    # game/changelog.txt:151
    old "- Created more cutscenes and variants for mall trips, including pregnancy support.{#ssct_changelog}"
    new "- 为逛商场事件新增过场与变体，包括孕期支持。{#ssct_changelog}"

    # game/changelog.txt:152
    old "- Improved various aspects of the character art for Maria and Tony.{#ssct_changelog}"
    new "- 改进Maria和Tony角色美术的多个方面。{#ssct_changelog}"

    # game/changelog.txt:153
    old "- Moved Tony's bag into the closet — a new location in Maria & Tony's apartment.{#ssct_changelog}"
    new "- 将Tony的包移入衣柜；这是Maria与Tony公寓中的新地点。{#ssct_changelog}"

    # game/changelog.txt:154
    old "- Extended the community pool location with a pump room.{#ssct_changelog}"
    new "- 为社区泳池新增水泵房。{#ssct_changelog}"

    # game/changelog.txt:155
    old "- Revisited x-ray animations to be more lively and be more orientation agnostic.{#ssct_changelog}"
    new "- 改进透视动画，使其更生动，并减少对朝向的依赖。{#ssct_changelog}"

    # game/changelog.txt:156
    old "- Added slider to control the opacity of the dialogue box background.{#ssct_changelog}"
    new "- 新增用于调整对话框背景透明度的滑块。{#ssct_changelog}"

    # game/changelog.txt:157
    old "- Adjusted shower peeks to avoid showing the same animation back-to-back.{#ssct_changelog}"
    new "- 调整偷看淋浴事件，避免连续出现相同动画。{#ssct_changelog}"

    # game/changelog.txt:158
    old "- Wrote and posed variant for vehicle turn-in that was previously unhandled.{#ssct_changelog}"
    new "- 为此前未处理的交还车辆情况补写并配置场景变体。{#ssct_changelog}"

    # game/changelog.txt:159
    old "- Enhanced spot metadata system to better handle use of rotational information.{#ssct_changelog}"
    new "- 改进位置元数据系统，使其更好地处理旋转信息。{#ssct_changelog}"

    # game/changelog.txt:160
    old "- Introduced presence tags to views, allowing for more dynamic elements in cutscenes.{#ssct_changelog}"
    new "- 为视图加入在场状态标签，让过场能够包含更多动态元素。{#ssct_changelog}"

    # game/changelog.txt:161
    old "- Remediated minor migration oversight to repair any affected saves.{#ssct_changelog}"
    new "- 修正轻微的存档迁移遗漏，修复受影响的存档。{#ssct_changelog}"

    # game/changelog.txt:162
    old "- Fixed missing assets to stop pregnant Debbie turning invisible in shower.{#ssct_changelog}"
    new "- 补上缺失资源，防止孕期Debbie在淋浴时不可见。{#ssct_changelog}"

    # game/changelog.txt:163
    old "- Brought a few remaining parts of the game into the translation system.{#ssct_changelog}"
    new "- 将游戏中少数尚未接入的部分纳入翻译系统。{#ssct_changelog}"

    # game/changelog.txt:164
    old "- Various spelling corrections and posing tweaks and lots of metadata.{#ssct_changelog}"
    new "- 修正多处拼写、角色姿势和大量元数据。{#ssct_changelog}"

    # game/changelog.txt:169
    old "- Reimagined and added back the Debbie leaning on the counter scene.{#ssct_changelog}"
    new "- 重新设计并恢复Debbie倚着台面的场景。{#ssct_changelog}"

    # game/changelog.txt:170
    old "- Rewrote and added a new animation to the evening scene with Debbie.{#ssct_changelog}"
    new "- 重写与Debbie的晚间场景，并加入一段新动画。{#ssct_changelog}"

    # game/changelog.txt:171
    old "- Introduced a new random encounter with Debbie in the basement.{#ssct_changelog}"
    new "- 新增与Debbie在地下室的随机邂逅。{#ssct_changelog}"

    # game/changelog.txt:172
    old "- Rebuilt Debbie's progressive shower events and added to cookie jar.{#ssct_changelog}"
    new "- 重建Debbie逐步发展的淋浴事件，并加入角色图鉴。{#ssct_changelog}"

    # game/changelog.txt:173
    old "- Reimplemented main story up to and including buying vehicles.{#ssct_changelog}"
    new "- 重新实现主线，直至购买车辆的部分。{#ssct_changelog}"

    # game/changelog.txt:174
    old "- Added the repeatable version of getting caught with Debbie's pants.{#ssct_changelog}"
    new "- 加入拿着Debbie裤子被撞见事件的可重复版本。{#ssct_changelog}"

    # game/changelog.txt:175
    old "- Enabled hand-holding in Debbie's mall visits, including when pregnant.{#ssct_changelog}"
    new "- 允许在与Debbie逛商场时牵手，孕期也可以。{#ssct_changelog}"

    # game/changelog.txt:176
    old "- Developed capability to prevent unwanted visitors to Anon's bedroom.{#ssct_changelog}"
    new "- 新增阻止不受欢迎的访客进入Anon卧室的功能。{#ssct_changelog}"

    # game/changelog.txt:177
    old "- Inadvertently caused playtest team to found {i}The Cult of the Chair{/i}.{#ssct_changelog}"
    new "- 无意中促使测试团队创立了{i}椅子神教{/i}。{#ssct_changelog}"

    # game/changelog.txt:178
    old "- Rolled meeting Maria into the quest where Anon is hired as a delivery boy.{#ssct_changelog}"
    new "- 将初次认识Maria的事件并入Anon被雇为送货员的任务。{#ssct_changelog}"

    # game/changelog.txt:179
    old "- Split out Maria's hair flower so it can be oriented correctly.{#ssct_changelog}"
    new "- 将Maria头发上的花拆为独立资源，使其朝向能够正确调整。{#ssct_changelog}"

    # game/changelog.txt:180
    old "- Established the base for Maria's button dialogue options.{#ssct_changelog}"
    new "- 建立Maria交互按钮对话选项的基础。{#ssct_changelog}"

    # game/changelog.txt:181
    old "- Updated the repairing Debbie's car quest to support visiting Josie in person.{#ssct_changelog}"
    new "- 更新修理Debbie汽车的任务，支持当面拜访Josie。{#ssct_changelog}"

    # game/changelog.txt:182
    old "- Installed basic functionality for the car dealership.{#ssct_changelog}"
    new "- 加入车行的基本功能。{#ssct_changelog}"

    # game/changelog.txt:183
    old "- Improved Josephine face art, especially lighting of her teeth.{#ssct_changelog}"
    new "- 改进Josephine的面部美术，尤其是牙齿的光照。{#ssct_changelog}"

    # game/changelog.txt:184
    old "- Hooked up buttons and schedules for the various dealership employees.{#ssct_changelog}"
    new "- 接入车行多名员工的交互按钮和日程。{#ssct_changelog}"

    # game/changelog.txt:185
    old "- Published \"Muffdiver\" magazine and allowed it to be viewed in the inventory.{#ssct_changelog}"
    new "- 推出“Muffdiver”杂志，并允许在物品栏中查看。{#ssct_changelog}"

    # game/changelog.txt:186
    old "- Implemented easy difficulty to automatically skip some mini games.{#ssct_changelog}"
    new "- 加入简单难度，自动跳过部分小游戏。{#ssct_changelog}"

    # game/changelog.txt:187
    old "- Changed the tutorial to only trigger if it has already been seen.{#ssct_changelog}"
    new "- 调整教程，使其仅在此前已经看过时触发。{#ssct_changelog}"

    # game/changelog.txt:188
    old "- Restaged Debbie's kitchen dialogue to better reflect button position.{#ssct_changelog}"
    new "- 重新安排Debbie厨房对话的场景，使其更符合按钮位置。{#ssct_changelog}"

    # game/changelog.txt:189
    old "- Touched up art for some of the pizzeria and dealership locations.{#ssct_changelog}"
    new "- 润色披萨店和车行部分地点的美术。{#ssct_changelog}"

    # game/changelog.txt:190
    old "- Finished removing old Anon art from Jenny's photo quest.{#ssct_changelog}"
    new "- 完成Jenny照片任务中旧版Anon美术的替换。{#ssct_changelog}"

    # game/changelog.txt:191
    old "- Tweaked a couple of Debbie quest reminders to not block her button.{#ssct_changelog}"
    new "- 微调Debbie的两处任务提醒，避免阻塞她的交互按钮。{#ssct_changelog}"

    # game/changelog.txt:192
    old "- Addressed Jenny referencing payment that may never have occurred.{#ssct_changelog}"
    new "- 修正Jenny提到一笔可能从未发生的付款的问题。{#ssct_changelog}"

    # game/changelog.txt:193
    old "- Stopped Debbie trying to cook during the helping around the house quest.{#ssct_changelog}"
    new "- 阻止Debbie在帮忙做家务任务期间尝试做饭。{#ssct_changelog}"

    # game/changelog.txt:194
    old "- Ensured Anon eventually gets wet when showering with Jenny.{#ssct_changelog}"
    new "- 确保Anon与Jenny一起洗澡时最终会被淋湿。{#ssct_changelog}"

    # game/changelog.txt:195
    old "- Optimised rig attribute preprocessing and added a feature to aid organisation.{#ssct_changelog}"
    new "- 优化角色绑定属性的预处理，并加入方便组织管理的功能。{#ssct_changelog}"

    # game/changelog.txt:196
    old "- Made it much easier to share sets of assets between rig poses.{#ssct_changelog}"
    new "- 让不同角色绑定姿势之间共享资源组更加容易。{#ssct_changelog}"

    # game/changelog.txt:197
    old "- Fixed soft-lock in Debbie pool quest to when Jenny was using the bathroom.{#ssct_changelog}"
    new "- 修复Jenny使用浴室时Debbie泳池任务发生的软锁。{#ssct_changelog}"

    # game/changelog.txt:198
    old "- Prevented bad player state after first Jenny telescope quest.{#ssct_changelog}"
    new "- 防止Jenny首次望远镜任务结束后玩家状态异常。{#ssct_changelog}"

    # game/changelog.txt:199
    old "- Repaired posing for Debbie drying her breasts just outside the shower.{#ssct_changelog}"
    new "- 修复Debbie刚走出淋浴时擦拭胸部的姿势。{#ssct_changelog}"

    # game/changelog.txt:200
    old "- Cleaned up scene previews that may now be unlocked normally.{#ssct_changelog}"
    new "- 清理现在已经可以正常解锁的场景预览。{#ssct_changelog}"

    # game/changelog.txt:201
    old "- Upgraded Ren'Py to version 8.5.0.{#ssct_changelog}"
    new "- 将Ren'Py升级至8.5.0版。{#ssct_changelog}"

    # game/changelog.txt:202
    old "- Various metadata additions, typo fixes, and consistency tweaks.{#ssct_changelog}"
    new "- 补充多项元数据，修复拼写并微调一致性。{#ssct_changelog}"

    # game/changelog.txt:207
    old "- Fixed save migrations for saves made prior to 21.0.0-wip.5252.{#ssct_changelog}"
    new "- 修复对21.0.0-wip.5252之前存档的迁移。{#ssct_changelog}"

    # game/changelog.txt:208
    old "- Added missing dialogue arm asset for Debbie while pregnant.{#ssct_changelog}"
    new "- 补上Debbie孕期对话中缺失的手臂资源。{#ssct_changelog}"

    # game/changelog.txt:213
    old "- Repaired import chain that caused bad virtual screen size and broken rigs.{#ssct_changelog}"
    new "- 修复导致虚拟屏幕尺寸异常和角色绑定损坏的导入链。{#ssct_changelog}"

    # game/changelog.txt:214
    old "- Fixed exception being thrown the first time Jenny's GFE event is played.{#ssct_changelog}"
    new "- 修复首次游玩Jenny的GFE事件时抛出异常的问题。{#ssct_changelog}"

    # game/changelog.txt:219
    old "- Capped off Debbie's route with her new original finale quest.{#ssct_changelog}"
    new "- 为Debbie支线加入全新原创的最终任务，完成支线收尾。{#ssct_changelog}"

    # game/changelog.txt:220
    old "- Added a pregnancy cycle for Debbie, including various new dialogue scenes.{#ssct_changelog}"
    new "- 为Debbie加入怀孕周期，包括多段新对话场景。{#ssct_changelog}"

    # game/changelog.txt:221
    old "- Created a new Japanese restaurant location and two new workers within.{#ssct_changelog}"
    new "- 新增日式餐厅地点及其中的两名员工。{#ssct_changelog}"

    # game/changelog.txt:222
    old "- Introduced two new characters in restaurant with button dialogue.{#ssct_changelog}"
    new "- 在餐厅引入两名新角色，并提供交互按钮对话。{#ssct_changelog}"

    # game/changelog.txt:223
    old "- Expanded art for Jenny and Debbie to support cross route pregnancy.{#ssct_changelog}"
    new "- 扩展Jenny和Debbie的美术，以支持跨支线的怀孕状态。{#ssct_changelog}"

    # game/changelog.txt:224
    old "- Made assets for characters sleeping in recovery rooms at night.{#ssct_changelog}"
    new "- 制作角色夜间在休养室睡觉的资源。{#ssct_changelog}"

    # game/changelog.txt:225
    old "- Installed cribs in character bedrooms for when they are nursing.{#ssct_changelog}"
    new "- 在角色卧室中加入育儿时使用的婴儿床。{#ssct_changelog}"

    # game/changelog.txt:226
    old "- Introduced simulation mechanics to support dynamic motion in aquarium.{#ssct_changelog}"
    new "- 引入模拟机制，支持水族箱中的动态运动。{#ssct_changelog}"

    # game/changelog.txt:227
    old "- Upgraded animation support in sets for smoother restaurant water feature.{#ssct_changelog}"
    new "- 改进场景的动画支持，使餐厅水景更加流畅。{#ssct_changelog}"

    # game/changelog.txt:228
    old "- Cleaned up some dynamic shot definitions to make them more composable.{#ssct_changelog}"
    new "- 整理部分动态镜头定义，使其更便于组合使用。{#ssct_changelog}"

    # game/changelog.txt:229
    old "- Prevented pregnancies stalling indefinitely in some edge cases.{#ssct_changelog}"
    new "- 防止某些边缘情况下怀孕进程无限停滞。{#ssct_changelog}"

    # game/changelog.txt:230
    old "- Wrote a custom mesh generator to support warping in restaurant menu.{#ssct_changelog}"
    new "- 编写自定义网格生成器，支持餐厅菜单的变形效果。{#ssct_changelog}"

    # game/changelog.txt:231
    old "- Stopped teleport effect in some unforeseen scene trigger scenarios.{#ssct_changelog}"
    new "- 消除部分未预料到的场景触发情况下出现的瞬移效果。{#ssct_changelog}"

    # game/changelog.txt:232
    old "- Optimised button routing for characters to make them more extensible.{#ssct_changelog}"
    new "- 优化角色按钮路由，使其更易扩展。{#ssct_changelog}"

    # game/changelog.txt:233
    old "- Fixed Jenny becoming invisible in cam show videos while pregnant.{#ssct_changelog}"
    new "- 修复Jenny孕期在色情直播视频中不可见的问题。{#ssct_changelog}"

    # game/changelog.txt:234
    old "- Inserted missing rails dialogue in trip to Pink with Jenny.{#ssct_changelog}"
    new "- 补上与Jenny前往粉色诱惑时缺失的引导对话。{#ssct_changelog}"

    # game/changelog.txt:235
    old "- Tweaked Kassy's button dialogue to support choosing a topic.{#ssct_changelog}"
    new "- 微调Kassy交互按钮的对话，支持选择话题。{#ssct_changelog}"

    # game/changelog.txt:236
    old "- Addressed misplaced basket abandonment prompt in Cupid.{#ssct_changelog}"
    new "- 修正丘比特中放弃购物篮提示出现位置不当的问题。{#ssct_changelog}"

    # game/changelog.txt:237
    old "- Ensured Diane's shovel quest cannot leave Jenny in a broken state.{#ssct_changelog}"
    new "- 确保Diane的铲子任务不会使Jenny陷入异常状态。{#ssct_changelog}"

    # game/changelog.txt:238
    old "- Corrected clipping of frames when using screen shake effects.{#ssct_changelog}"
    new "- 修正屏幕震动效果造成的画面裁切。{#ssct_changelog}"

    # game/changelog.txt:239
    old "- Various typo corrections, presence checks, and context consistency fixes.{#ssct_changelog}"
    new "- 修复多处拼写、在场判断和语境一致性问题。{#ssct_changelog}"

    # game/changelog.txt:244
    old "- Continued Debbie's route with one original, and one reworked quest.{#ssct_changelog}"
    new "- 继续Debbie支线，加入一个原创任务和一个重做任务。{#ssct_changelog}"

    # game/changelog.txt:245
    old "- Inserted missing diary entry after Jenny catches Anon during Debbie boobjob.{#ssct_changelog}"
    new "- 补上Jenny撞见Anon接受Debbie乳交后缺失的日记条目。{#ssct_changelog}"

    # game/changelog.txt:246
    old "- Fixed issue with some blurred assets being cut-off too early.{#ssct_changelog}"
    new "- 修复部分模糊资源过早被裁掉的问题。{#ssct_changelog}"

    # game/changelog.txt:247
    old "- Expanded replay of Debbie's boobjob scene to include more of the lewd preamble.{#ssct_changelog}"
    new "- 扩展Debbie乳交场景的回放，包含更多成人前戏内容。{#ssct_changelog}"

    # game/changelog.txt:248
    old "- Added hide button to quick menu on touch devices where other options are unavailable.{#ssct_changelog}"
    new "- 在其他选项不可用的触屏设备快捷菜单中加入隐藏按钮。{#ssct_changelog}"

    # game/changelog.txt:249
    old "- Restored Debbie's bush in lotion massage animation.{#ssct_changelog}"
    new "- 恢复涂乳液按摩动画中Debbie的阴毛。{#ssct_changelog}"

    # game/changelog.txt:250
    old "- Wrote new shader in order to visually communicate flashbacks.{#ssct_changelog}"
    new "- 编写新着色器，用视觉效果表达闪回。{#ssct_changelog}"

    # game/changelog.txt:251
    old "- Reworked Debbie's bedroom location with improved art.{#ssct_changelog}"
    new "- 重做Debbie卧室地点，改进美术。{#ssct_changelog}"

    # game/changelog.txt:252
    old "- Updated art of Debbie hovering at the door when entering Anon's room.{#ssct_changelog}"
    new "- 更新Debbie进入Anon房间时在门口徘徊的美术。{#ssct_changelog}"

    # game/changelog.txt:253
    old "- Improved character art for Lily and Judith.{#ssct_changelog}"
    new "- 改进Lily和Judith的角色美术。{#ssct_changelog}"

    # game/changelog.txt:254
    old "- Drew new TV channel variant in order to better match narrative use.{#ssct_changelog}"
    new "- 绘制新的电视频道变体，使其更符合剧情用途。{#ssct_changelog}"

    # game/changelog.txt:255
    old "- Created several new variant UI assets.{#ssct_changelog}"
    new "- 制作多项新的界面资源变体。{#ssct_changelog}"

    # game/changelog.txt:256
    old "- Blocked a teleportation bug when speaking to Annie during Miss Okita's serum quest.{#ssct_changelog}"
    new "- 修复Okita老师药剂任务中与Annie交谈时发生的瞬移错误。{#ssct_changelog}"

    # game/changelog.txt:257
    old "- Corrected oversight in pizza mini game where zero deliveries would cause crash.{#ssct_changelog}"
    new "- 修正披萨小游戏中零次配送会导致崩溃的遗漏。{#ssct_changelog}"

    # game/changelog.txt:258
    old "- Resolved conflict between Miss Dewitt and Miss Ross routes when collecting planks.{#ssct_changelog}"
    new "- 解决收集木板时Dewitt老师与Ross老师支线的冲突。{#ssct_changelog}"

    # game/changelog.txt:259
    old "- Ensured replay of Debbie blowjob scene in Anon's room correctly unlocks.{#ssct_changelog}"
    new "- 确保Debbie在Anon房间中的口交场景回放正确解锁。{#ssct_changelog}"

    # game/changelog.txt:260
    old "- Applied correct tint to Anon's bedsheets during Debbie's visits.{#ssct_changelog}"
    new "- Debbie来访时，为Anon的床单应用正确色调。{#ssct_changelog}"

    # game/changelog.txt:261
    old "- Attempted to support two-decade old hardware in equirectangular projection shader.{#ssct_changelog}"
    new "- 尝试在等距柱状投影着色器中支持二十年前的硬件。{#ssct_changelog}"

    # game/changelog.txt:262
    old "- Upgraded Ren'Py to version 8.4.1, and made new accessibility options available.{#ssct_changelog}"
    new "- 将Ren'Py升级至8.4.1版，并开放新的辅助功能选项。{#ssct_changelog}"

    # game/changelog.txt:263
    old "- Various minor posing improvements, metadata adjustments, and asset tweaks.{#ssct_changelog}"
    new "- 微调多处角色姿势、元数据和资源。{#ssct_changelog}"

    # game/changelog.txt:268
    old "- Added one original, one reworked, and one upgraded quest to Debbie's route.{#ssct_changelog}"
    new "- 为Debbie支线加入一个原创任务、一个重做任务和一个升级任务。{#ssct_changelog}"

    # game/changelog.txt:269
    old "- Continued the main story with two more upgraded quests and pizza mini game.{#ssct_changelog}"
    new "- 继续主线，加入两个升级任务和披萨小游戏。{#ssct_changelog}"

    # game/changelog.txt:270
    old "- Expanded Debbie's recurring shower event with another level of escalation.{#ssct_changelog}"
    new "- 扩展Debbie可重复的淋浴事件，加入更进一步的阶段。{#ssct_changelog}"

    # game/changelog.txt:271
    old "- Included two new animations, for future quests, in shower previews section.{#ssct_changelog}"
    new "- 在淋浴预览区域加入两段用于未来任务的新动画。{#ssct_changelog}"

    # game/changelog.txt:272
    old "- Made previewable animations available, already unlocked, to the cookie jar.{#ssct_changelog}"
    new "- 将可预览的动画以已解锁状态加入角色图鉴。{#ssct_changelog}"

    # game/changelog.txt:273
    old "- Moved rig system over to new positioning system.{#ssct_changelog}"
    new "- 将角色绑定系统迁移至新的定位系统。{#ssct_changelog}"

    # game/changelog.txt:274
    old "- Overhauled how transitions are managed to better facilitate future usage.{#ssct_changelog}"
    new "- 重做转场管理方式，方便未来使用。{#ssct_changelog}"

    # game/changelog.txt:275
    old "- Drew many more art assets for Anon, Debbie, Dimitri, Igor, and Kassy.{#ssct_changelog}"
    new "- 为Anon、Debbie、Dimitri、Igor和Kassy绘制更多美术资源。{#ssct_changelog}"

    # game/changelog.txt:276
    old "- Revisited Jenny cam show handjob animation and added more frames.{#ssct_changelog}"
    new "- 重新打磨Jenny色情直播中的手交动画，增加画面帧。{#ssct_changelog}"

    # game/changelog.txt:277
    old "- Enhanced Jenny shower blowjob scene with more cum frames and other tweaks.{#ssct_changelog}"
    new "- 改进Jenny淋浴口交场景，增加射精画面帧并进行其他微调。{#ssct_changelog}"

    # game/changelog.txt:278
    old "- Worked on adding variety to Summerville in the form of more crowd variants.{#ssct_changelog}"
    new "- 通过更多人群变体，为夏日镇增添变化。{#ssct_changelog}"

    # game/changelog.txt:279
    old "- Reworked washroom and second floor concourse of the mall with more details.{#ssct_changelog}"
    new "- 重做商场洗手间和二楼大厅，增加细节。{#ssct_changelog}"

    # game/changelog.txt:280
    old "- Created art for a new TV show for use in Debbie's route.{#ssct_changelog}"
    new "- 为Debbie支线制作新电视节目的美术。{#ssct_changelog}"

    # game/changelog.txt:281
    old "- Extended the Cupid store location with a new storage room.{#ssct_changelog}"
    new "- 为丘比特商店新增储藏室。{#ssct_changelog}"

    # game/changelog.txt:282
    old "- Plumbed in the next stage of Debbie's pool button.{#ssct_changelog}"
    new "- 接入Debbie泳池交互按钮的下一阶段。{#ssct_changelog}"

    # game/changelog.txt:283
    old "- Installed water VFX for shower preview animation.{#ssct_changelog}"
    new "- 为淋浴预览动画加入水流视觉特效。{#ssct_changelog}"

    # game/changelog.txt:284
    old "- Fixed part of Jenny's initial sex cam show quest being accidentally skipped.{#ssct_changelog}"
    new "- 修复Jenny首次性爱直播任务中的部分内容被意外跳过的问题。{#ssct_changelog}"

    # game/changelog.txt:285
    old "- Tweaked second dream sequence in Debbie's route to be more performant.{#ssct_changelog}"
    new "- 微调Debbie支线的第二段梦境，提高运行性能。{#ssct_changelog}"

    # game/changelog.txt:286
    old "- Allowed photo booth to be interacted with once again.{#ssct_changelog}"
    new "- 恢复照相亭的交互功能。{#ssct_changelog}"

    # game/changelog.txt:287
    old "- Prevented minor state corruption when clearing the shower at night.{#ssct_changelog}"
    new "- 防止夜间清理淋浴状态时发生轻微的状态损坏。{#ssct_changelog}"

    # game/changelog.txt:288
    old "- Guarded against pathological player behaviour in Roxxy visit quest.{#ssct_changelog}"
    new "- 防止Roxxy来访任务中玩家的极端操作引发异常。{#ssct_changelog}"

    # game/changelog.txt:289
    old "- Various minor posing improvements.{#ssct_changelog}"
    new "- 微调多处角色姿势。{#ssct_changelog}"

    # game/changelog.txt:294
    old "- Fixed crash in Debbie's mall trip event if Anon was busy the night prior.{#ssct_changelog}"
    new "- 修复Anon前一晚忙于其他事情时Debbie逛商场事件会崩溃的问题。{#ssct_changelog}"

    # game/changelog.txt:295
    old "- Corrected minor typo in reminder dialogue for Debbie's mall trip event.{#ssct_changelog}"
    new "- 修正Debbie逛商场事件提醒对话中的轻微拼写错误。{#ssct_changelog}"

    # game/changelog.txt:300
    old "- Continued Debbie's route with one original, two reworked, and two upgraded quests.{#ssct_changelog}"
    new "- 继续Debbie支线，加入一个原创任务、两个重做任务和两个升级任务。{#ssct_changelog}"

    # game/changelog.txt:301
    old "- Added another level of escalation into Debbie's recurring shower event.{#ssct_changelog}"
    new "- 为Debbie可重复的淋浴事件加入更进一步的阶段。{#ssct_changelog}"

    # game/changelog.txt:302
    old "- Allowed three new animations, intended for future quests, to be previewed early.{#ssct_changelog}"
    new "- 允许提前预览三段原本用于未来任务的新动画。{#ssct_changelog}"

    # game/changelog.txt:303
    old "- Restored the first two quests of Diane's route, including gardening mini game.{#ssct_changelog}"
    new "- 恢复Diane支线的前两个任务，包括园艺小游戏。{#ssct_changelog}"

    # game/changelog.txt:304
    old "- Wired up Diane's early game button in her garden.{#ssct_changelog}"
    new "- 接入Diane在花园中的游戏前期交互按钮。{#ssct_changelog}"

    # game/changelog.txt:305
    old "- Overhauled a large number of assets and scenes that occur on Debbie's couch.{#ssct_changelog}"
    new "- 重做大量发生在Debbie沙发上的美术资源和场景。{#ssct_changelog}"

    # game/changelog.txt:306
    old "- Expanded the forest slightly. Don't worry about it, nothing to see there. >_>;;{#ssct_changelog}"
    new "- 稍微扩展了森林。别担心，那里没什么好看的。>_>;;{#ssct_changelog}"

    # game/changelog.txt:307
    old "- Created a new blend mode to help simulate dimming of light sources.{#ssct_changelog}"
    new "- 新增混合模式，帮助模拟光源变暗的效果。{#ssct_changelog}"

    # game/changelog.txt:308
    old "- Combined some cutscene assets, allowing art to be upgraded while saving space.{#ssct_changelog}"
    new "- 合并部分过场资源，在节省空间的同时升级美术。{#ssct_changelog}"

    # game/changelog.txt:309
    old "- Slowed speed of vertical pan the first time Anon dreams of Debbie.{#ssct_changelog}"
    new "- 放慢Anon首次梦见Debbie时镜头的垂直移动速度。{#ssct_changelog}"

    # game/changelog.txt:310
    old "- Mitigated issue impacting cancellation of auto-nav in deferred events.{#ssct_changelog}"
    new "- 缓解影响延后事件中取消自动导航的问题。{#ssct_changelog}"

    # game/changelog.txt:311
    old "- Adjusted some character information in the contacts app, and added Diane.{#ssct_changelog}"
    new "- 调整联系人应用中的部分角色信息，并加入Diane。{#ssct_changelog}"

    # game/changelog.txt:312
    old "- Spaced out the timeline between a couple of existing Debbie quests.{#ssct_changelog}"
    new "- 拉开Debbie两个现有任务之间的时间间隔。{#ssct_changelog}"

    # game/changelog.txt:313
    old "- Made a minor cutscene variation for the lotion variant of Debbie's mall event.{#ssct_changelog}"
    new "- 为Debbie商场事件的乳液变体制作小幅过场变化。{#ssct_changelog}"

    # game/changelog.txt:314
    old "- Applied patch to prevent incorrect rendering of some visual effects on Android.{#ssct_changelog}"
    new "- 应用补丁，防止Android上部分视觉特效渲染错误。{#ssct_changelog}"

    # game/changelog.txt:315
    old "- Tweaked the positioning system to work better with nested character rigs.{#ssct_changelog}"
    new "- 微调定位系统，使其更好地支持嵌套角色绑定。{#ssct_changelog}"

    # game/changelog.txt:316
    old "- Factored out some magic numbers to aid readability as the codebase further expands.{#ssct_changelog}"
    new "- 提取部分魔法数字，提高代码库扩展时的可读性。{#ssct_changelog}"

    # game/changelog.txt:317
    old "- Updated some nighttime Jenny scenes with a tint to better fit the time of day.{#ssct_changelog}"
    new "- 为Jenny的部分夜间场景调整色调，使其更符合时段。{#ssct_changelog}"

    # game/changelog.txt:318
    old "- Fixed incorrect zoning of Diane's house which could break some quests.{#ssct_changelog}"
    new "- 修复Diane房屋区域划分错误导致部分任务异常的问题。{#ssct_changelog}"

    # game/changelog.txt:319
    old "- Resolved a soft-lock in Miss Okita's route concerning Mrs. Smith's office.{#ssct_changelog}"
    new "- 解决Okita老师支线中涉及Smith太太办公室的软锁。{#ssct_changelog}"

    # game/changelog.txt:320
    old "- Altered projection shader to circumvent very rare bug in some graphics drivers.{#ssct_changelog}"
    new "- 修改投影着色器，绕过部分显卡驱动中的极罕见错误。{#ssct_changelog}"

    # game/changelog.txt:321
    old "- Improved text layout of background information in contacts app.{#ssct_changelog}"
    new "- 改进联系人应用中人物背景信息的文字布局。{#ssct_changelog}"

    # game/changelog.txt:322
    old "- Corrected various typos in existing dialogue.{#ssct_changelog}"
    new "- 修正现有对话中的多处拼写错误。{#ssct_changelog}"

    # game/changelog.txt:327
    old "- Increased resolution of assets used in Anon's nightmare.{#ssct_changelog}"
    new "- 提高Anon噩梦中所用资源的分辨率。{#ssct_changelog}"

    # game/changelog.txt:328
    old "- Fixed Jenny not always rendering correctly during Anon's nightmare.{#ssct_changelog}"
    new "- 修复Anon噩梦中Jenny有时渲染不正确的问题。{#ssct_changelog}"

    # game/changelog.txt:329
    old "- Restored translation support in choice menus.{#ssct_changelog}"
    new "- 恢复选项菜单的翻译支持。{#ssct_changelog}"

    # game/changelog.txt:330
    old "- Hid duplicate Debbie that could appear in background of a few scenes.{#ssct_changelog}"
    new "- 隐藏部分场景背景中可能出现的重复Debbie。{#ssct_changelog}"

    # game/changelog.txt:335
    old "- Fixed Debbie not always rendering correctly during Anon's panty flashback.{#ssct_changelog}"
    new "- 修复Anon内裤闪回中Debbie有时渲染不正确的问题。{#ssct_changelog}"

    # game/changelog.txt:340
    old "- Expanded Debbie's route with one original, three reworked, and six upgraded quests.{#ssct_changelog}"
    new "- 扩展Debbie支线，加入一个原创任务、三个重做任务和六个升级任务。{#ssct_changelog}"

    # game/changelog.txt:341
    old "- Created a new mall trip event with Debbie that evolves with her story.{#ssct_changelog}"
    new "- 新增与Debbie逛商场的事件，并随她的剧情发展而变化。{#ssct_changelog}"

    # game/changelog.txt:342
    old "- Moved over to using Debbie's new art when she appears in other routes.{#ssct_changelog}"
    new "- Debbie出现在其他支线时改用她的新版美术。{#ssct_changelog}"

    # game/changelog.txt:343
    old "- Updated Debbie's art in her button dialogue, including sleeping Debbie.{#ssct_changelog}"
    new "- 更新Debbie交互按钮对话的美术，包括睡着的Debbie。{#ssct_changelog}"

    # game/changelog.txt:344
    old "- Rebuilt peeking on Debbie in the shower event with more new art.{#ssct_changelog}"
    new "- 加入更多新美术，重建偷看Debbie淋浴的事件。{#ssct_changelog}"

    # game/changelog.txt:345
    old "- Extended Debbie's schedule to rarely place her by the pool of an evening.{#ssct_changelog}"
    new "- 扩展Debbie的日程，让她偶尔在晚间出现在泳池边。{#ssct_changelog}"

    # game/changelog.txt:346
    old "- Built new x-ray system and began adding it to existing scenes.{#ssct_changelog}"
    new "- 建立新的透视系统，并开始加入现有场景。{#ssct_changelog}"

    # game/changelog.txt:347
    old "- Wrote up Frank and Bridget's background information for the phone.{#ssct_changelog}"
    new "- 为手机编写Frank和Bridget的背景信息。{#ssct_changelog}"

    # game/changelog.txt:348
    old "- Improved dialogue hint when clicking on exterior garage door with key.{#ssct_changelog}"
    new "- 改进持有钥匙时点击车库外门的对话提示。{#ssct_changelog}"

    # game/changelog.txt:349
    old "- Locked that lotion bottle in Debbie's drawer. For now.{#ssct_changelog}"
    new "- 锁住Debbie抽屉里的那瓶乳液。暂时如此。{#ssct_changelog}"

    # game/changelog.txt:350
    old "- Restored correct hover effect to quick menu.{#ssct_changelog}"
    new "- 恢复快捷菜单正确的悬浮效果。{#ssct_changelog}"

    # game/changelog.txt:351
    old "- Prevented quick load feature attempting to load incompatible saves.{#ssct_changelog}"
    new "- 防止快速读档功能尝试载入不兼容存档。{#ssct_changelog}"

    # game/changelog.txt:352
    old "- Removed non-functional options from quick menu when viewing a replay.{#ssct_changelog}"
    new "- 查看回放时移除快捷菜单中无法使用的选项。{#ssct_changelog}"

    # game/changelog.txt:353
    old "- Revisited animation system to improve stability, most notably during rollback.{#ssct_changelog}"
    new "- 改进动画系统的稳定性，尤其是回滚时的表现。{#ssct_changelog}"

    # game/changelog.txt:354
    old "- Retooled mimic system to be more reliable and prediction friendly.{#ssct_changelog}"
    new "- 重整模仿系统，使其更可靠、更易进行资源预加载。{#ssct_changelog}"

    # game/changelog.txt:355
    old "- Fixed edge-case migration issue when loading some saves from Preview 1.{#ssct_changelog}"
    new "- 修复载入部分预览版1存档时出现的边缘迁移问题。{#ssct_changelog}"

    # game/changelog.txt:356
    old "- Guarded against Judith being able to break a Miss Ross quest.{#ssct_changelog}"
    new "- 防止Judith导致Ross老师的任务异常。{#ssct_changelog}"

    # game/changelog.txt:357
    old "- Various small posing improvements to Debbie content from last preview.{#ssct_changelog}"
    new "- 微调上一预览版Debbie内容中的多处角色姿势。{#ssct_changelog}"

    # game/changelog.txt:358
    old "- Ensured consistent view of hallway in Debbie's house during navigation.{#ssct_changelog}"
    new "- 确保导航时Debbie家中的走廊画面保持一致。{#ssct_changelog}"

    # game/changelog.txt:359
    old "- Adjusted timings of some ambient sounds to avoid hard cuts as they loop.{#ssct_changelog}"
    new "- 调整部分环境音的时序，避免循环时突然中断。{#ssct_changelog}"

    # game/changelog.txt:360
    old "- Addressed issue where map music could linger into rails dialogue.{#ssct_changelog}"
    new "- 修复地图音乐持续到引导对话中的问题。{#ssct_changelog}"

    # game/changelog.txt:361
    old "- Dealt with flip-flop continuity issues in Jenny's telescope scenes.{#ssct_changelog}"
    new "- 处理Jenny望远镜场景中拖鞋前后不一致的问题。{#ssct_changelog}"

    # game/changelog.txt:362
    old "- Made sure the fake guitar is added to the wall properly in Melody's route.{#ssct_changelog}"
    new "- 确保Melody支线中的假吉他正确添加到墙上。{#ssct_changelog}"

    # game/changelog.txt:363
    old "- Cobbled together a new shader to support equirectangular projection.{#ssct_changelog}"
    new "- 制作支持等距柱状投影的新着色器。{#ssct_changelog}"

    # game/changelog.txt:364
    old "- Optimised some hot code paths to keep navigation snappy.{#ssct_changelog}"
    new "- 优化部分高频执行代码，让导航保持流畅。{#ssct_changelog}"

    # game/changelog.txt:365
    old "- Resolved issue where using spot metadata would prevent asset prediction.{#ssct_changelog}"
    new "- 解决使用位置元数据会阻止资源预加载的问题。{#ssct_changelog}"

    # game/changelog.txt:366
    old "- Added a basic bloom visual effect to help distinguish daydreams.{#ssct_changelog}"
    new "- 新增基础泛光视觉效果，帮助区分白日梦。{#ssct_changelog}"

    # game/changelog.txt:367
    old "- Helped rails to feel a little more natural when multiple paths may be taken.{#ssct_changelog}"
    new "- 存在多条可选路径时，让引导流程更加自然。{#ssct_changelog}"

    # game/changelog.txt:368
    old "- Enabled visible cues for choices that require unmet stat checks.{#ssct_changelog}"
    new "- 为未满足属性检查条件的选项启用可见提示。{#ssct_changelog}"

    # game/changelog.txt:369
    old "- Developed many new rig assets for both Jiang and Kassy.{#ssct_changelog}"
    new "- 为Jiang和Kassy开发大量新角色绑定资源。{#ssct_changelog}"

    # game/changelog.txt:370
    old "- Upgraded Ren'Py to version 8.3.4.{#ssct_changelog}"
    new "- 将Ren'Py升级至8.3.4版。{#ssct_changelog}"

    # game/changelog.txt:371
    old "- Touched up art of Anon using telescope in Jenny's route.{#ssct_changelog}"
    new "- 润色Jenny支线中Anon使用望远镜的美术。{#ssct_changelog}"

    # game/changelog.txt:372
    old "- Redrew telescope shot from Jenny's route to bring its quality up to par.{#ssct_changelog}"
    new "- 重绘Jenny支线的望远镜镜头，使其达到当前质量标准。{#ssct_changelog}"

    # game/changelog.txt:373
    old "- Produced new assets for Jenny to reflect her pregnancy in Debbie's route.{#ssct_changelog}"
    new "- 制作新资源，体现Jenny在Debbie支线中的怀孕状态。{#ssct_changelog}"

    # game/changelog.txt:374
    old "- Revamped various cutscenes and created multiple new ones.{#ssct_changelog}"
    new "- 翻新多个过场并新增多段过场。{#ssct_changelog}"

    # game/changelog.txt:375
    old "- Put together a new translatable module to help with expressing time periods.{#ssct_changelog}"
    new "- 制作新的可翻译模块，方便表达时间段。{#ssct_changelog}"

    # game/changelog.txt:376
    old "- Tweaked layer management logic to prevent Jenny's laptop appearing twice.{#ssct_changelog}"
    new "- 微调图层管理逻辑，防止Jenny的笔记本电脑显示两次。{#ssct_changelog}"

    # game/changelog.txt:377
    old "- Integrated meeting Tammy outside Debbie's house with new mall trip event.{#ssct_changelog}"
    new "- 将Debbie家门外与Tammy见面的事件接入新的逛商场事件。{#ssct_changelog}"

    # game/changelog.txt:378
    old "- Found and fixed a latent bug in how metadata scaling was being applied.{#ssct_changelog}"
    new "- 发现并修复元数据缩放应用方式中潜藏的错误。{#ssct_changelog}"

    # game/changelog.txt:379
    old "- Solved problem that would cause some sounds to play sooner than intended.{#ssct_changelog}"
    new "- 解决部分声音比预期更早播放的问题。{#ssct_changelog}"

    # game/changelog.txt:380
    old "- Tackled various other continuity and posing issues in earlier Debbie quests.{#ssct_changelog}"
    new "- 处理Debbie前期任务中的其他多处连贯性和姿势问题。{#ssct_changelog}"

    # game/changelog.txt:381
    old "- Stopped Jenny's first sex toy quest from interfering with the timeline.{#ssct_changelog}"
    new "- 防止Jenny首次性玩具任务干扰时间线。{#ssct_changelog}"

    # game/changelog.txt:382
    old "- Remedied various issues when Jenny showered at night.{#ssct_changelog}"
    new "- 修复Jenny夜间淋浴时的多项问题。{#ssct_changelog}"

    # game/changelog.txt:383
    old "- Introduced small dialogue variations to account for when Debbie is at the mall.{#ssct_changelog}"
    new "- 加入简短的对话变体，以适应Debbie在商场时的情况。{#ssct_changelog}"

    # game/changelog.txt:384
    old "- Inserted variant for claiming glasses from Judith during art class.{#ssct_changelog}"
    new "- 加入美术课上向Judith领取眼镜的变体。{#ssct_changelog}"

    # game/changelog.txt:385
    old "- Many small asset changes to adjust expressions and smooth arm joints.{#ssct_changelog}"
    new "- 微调多项资源，调整表情并让手臂关节衔接更顺畅。{#ssct_changelog}"

    # game/changelog.txt:386
    old "- Reduced the use of magic numbers throughout the priority system.{#ssct_changelog}"
    new "- 减少优先级系统中魔法数字的使用。{#ssct_changelog}"

    # game/changelog.txt:387
    old "- Prepared and cleaned up the codebase for a future move to Python 3.12.{#ssct_changelog}"
    new "- 为未来迁移至Python 3.12整理和清理代码库。{#ssct_changelog}"

    # game/changelog.txt:388
    old "- Eliminated various other minor bugs in existing quests.{#ssct_changelog}"
    new "- 消除现有任务中的其他多处轻微错误。{#ssct_changelog}"

    # game/changelog.txt:393
    old "- Resolved Debbie's route failing to re-activate correctly in some migrated saves.{#ssct_changelog}"
    new "- 修复部分迁移存档中Debbie支线未能正确重新激活的问题。{#ssct_changelog}"

    # game/changelog.txt:394
    old "- Fixed soft-lock in Judith's locker when reclaiming library book from Camila.{#ssct_changelog}"
    new "- 修复从Camila处取回图书馆书籍时Judith储物柜中的软锁。{#ssct_changelog}"

    # game/changelog.txt:399
    old "- Added all new event early in Debbie's story.{#ssct_changelog}"
    new "- 在Debbie剧情前期加入全新事件。{#ssct_changelog}"

    # game/changelog.txt:400
    old "- Upgraded four of Debbie's existing quests with new art and dialogue.{#ssct_changelog}"
    new "- 为Debbie四个现有任务升级美术和对话。{#ssct_changelog}"

    # game/changelog.txt:401
    old "- Improved existing cutscenes and added new ones.{#ssct_changelog}"
    new "- 改进现有过场并新增多段过场。{#ssct_changelog}"

    # game/changelog.txt:402
    old "- Updated home location backgrounds and closeups.{#ssct_changelog}"
    new "- 更新住宅地点的背景和特写。{#ssct_changelog}"

    # game/changelog.txt:403
    old "- Added multiple new bodies, arms and facial assets for Debbie and Anon.{#ssct_changelog}"
    new "- 为Debbie和Anon新增多套身体、手臂和面部资源。{#ssct_changelog}"

    # game/changelog.txt:404
    old "- Changed Debbie's default buttons to use new art.{#ssct_changelog}"
    new "- 将Debbie的默认交互按钮改用新版美术。{#ssct_changelog}"

    # game/changelog.txt:405
    old "- Expanded and improved the Cupid store to allow more space, rooms and variety.{#ssct_changelog}"
    new "- 扩建并改进丘比特商店，增加空间、房间和变化。{#ssct_changelog}"

    # game/changelog.txt:406
    old "- Upgraded Ren'Py to version 8.3.3.{#ssct_changelog}"
    new "- 将Ren'Py升级至8.3.3版。{#ssct_changelog}"

    # game/changelog.txt:407
    old "- Wrote a save migration to fully reset Debbie progress in preparation for her rework.{#ssct_changelog}"
    new "- 编写存档迁移，完全重置Debbie的进度，为支线重做做准备。{#ssct_changelog}"

    # game/changelog.txt:408
    old "- Added support for multi-asset cutscenes to easier include dynamic details such as pregnancy.{#ssct_changelog}"
    new "- 加入多资源过场支持，更方便地包含怀孕等动态细节。{#ssct_changelog}"

    # game/changelog.txt:409
    old "- Revisited attribute management to allow for more flexibility in when displaying backgrounds.{#ssct_changelog}"
    new "- 改进属性管理，使背景显示更加灵活。{#ssct_changelog}"

    # game/changelog.txt:410
    old "- Tweaked focus management on initial name screen to be more mobile friendly.{#ssct_changelog}"
    new "- 微调初始姓名界面的焦点管理，使其更适合移动设备。{#ssct_changelog}"

    # game/changelog.txt:411
    old "- Flipped the hallway between the entrance and living room.{#ssct_changelog}"
    new "- 翻转入口与客厅之间的走廊布局。{#ssct_changelog}"

    # game/changelog.txt:412
    old "- Fixed soft-lock with Annie outside Mrs. Smith's office.{#ssct_changelog}"
    new "- 修复Annie在Smith太太办公室外造成的软锁。{#ssct_changelog}"

    # game/changelog.txt:413
    old "- Resolved a problem with older saves causing problems accessing the phone.{#ssct_changelog}"
    new "- 解决旧存档访问手机时出现的问题。{#ssct_changelog}"

    # game/changelog.txt:414
    old "- Various art metadata additions and typo corrections.{#ssct_changelog}"
    new "- 补充多项美术元数据并修正拼写。{#ssct_changelog}"

    # game/changelog.txt:415
    old "- Addressed minor posing issues relating to mouth movement in teacher routes.{#ssct_changelog}"
    new "- 修复教师支线中与嘴部运动有关的轻微姿势问题。{#ssct_changelog}"

    # game/changelog.txt:416
    old "- Stopped the sink breaking prematurely in Debbie's route when sleeping in the beach house.{#ssct_changelog}"
    new "- 防止在海滨小屋睡觉时Debbie支线中的水槽过早损坏。{#ssct_changelog}"

    # game/changelog.txt:421
    old "- Upgraded visuals and user experience of the in-game phone.{#ssct_changelog}"
    new "- 升级游戏内手机的视觉效果和使用体验。{#ssct_changelog}"

    # game/changelog.txt:422
    old "- Added a character directory in the form of a contacts app on the phone.{#ssct_changelog}"
    new "- 在手机中加入联系人应用形式的角色目录。{#ssct_changelog}"

    # game/changelog.txt:423
    old "- Introduced the ability to rename characters via the phone.{#ssct_changelog}"
    new "- 新增通过手机为角色改名的功能。{#ssct_changelog}"

    # game/changelog.txt:424
    old "- Redesigned the look and feel of the game menus.{#ssct_changelog}"
    new "- 重新设计游戏菜单的外观和体验。{#ssct_changelog}"

    # game/changelog.txt:425
    old "- Mall crowd art improved and unique for each time tick.{#ssct_changelog}"
    new "- 改进商场人群美术，为每个时间段提供独特变体。{#ssct_changelog}"

    # game/changelog.txt:426
    old "- Beach crowd art improved and unique for each time tick.{#ssct_changelog}"
    new "- 改进海滩人群美术，为每个时间段提供独特变体。{#ssct_changelog}"

    # game/changelog.txt:427
    old "- Debbie cutscenes improved.{#ssct_changelog}"
    new "- 改进Debbie的过场。{#ssct_changelog}"

    # game/changelog.txt:428
    old "- New consistent art for Debbie's laundry basket.{#ssct_changelog}"
    new "- 为Debbie的洗衣篮制作统一的新美术。{#ssct_changelog}"

    # game/changelog.txt:429
    old "- Mini game art now matches quality and styling of new UI.{#ssct_changelog}"
    new "- 让小游戏美术达到新界面的质量和风格。{#ssct_changelog}"

    # game/changelog.txt:430
    old "- Jenny body assets slight improvements such as arms and shoulders.{#ssct_changelog}"
    new "- 微调Jenny的身体资源，包括手臂和肩膀。{#ssct_changelog}"

    # game/changelog.txt:435
    old "- Reimplemented routes for Miss Bissette, Miss Okita, and Miss Ross.{#ssct_changelog}"
    new "- 重新实现Bissette老师、Okita老师和Ross老师的支线。{#ssct_changelog}"

    # game/changelog.txt:436
    old "- Partially completed route for Miss Dewitt, with the rest due back in a future update.{#ssct_changelog}"
    new "- 部分完成Dewitt老师支线，其余内容将在后续更新中回归。{#ssct_changelog}"

    # game/changelog.txt:437
    old "- Restored Judith mini-route, with fully updated character art.{#ssct_changelog}"
    new "- 恢复Judith的短支线，并全面更新角色美术。{#ssct_changelog}"

    # game/changelog.txt:438
    old "- Added a new event for Debbie in the kitchen at the end of her route.{#ssct_changelog}"
    new "- 在Debbie支线结尾新增厨房事件。{#ssct_changelog}"

    # game/changelog.txt:439
    old "- Introduced a second Jenny cunnilingus animation (for submissive Anon).{#ssct_changelog}"
    new "- 新增Jenny的第二段舔阴动画，用于顺从的Anon。{#ssct_changelog}"

    # game/changelog.txt:440
    old "- Reworked Jenny GFE ending with dominant and submissive variants and new animations.{#ssct_changelog}"
    new "- 重做Jenny的GFE结局，加入支配与顺从变体及新动画。{#ssct_changelog}"

    # game/changelog.txt:441
    old "- Added back remaining Debbie events including laundry, garage, movie, panties, and bedroom.{#ssct_changelog}"
    new "- 恢复Debbie其余事件，包括洗衣、车库、电影、内裤和卧室事件。{#ssct_changelog}"

    # game/changelog.txt:442
    old "- Enabled most of the NPCs usually found at and around the college.{#ssct_changelog}"
    new "- 启用通常出现在学院及周边的大多数NPC。{#ssct_changelog}"

    # game/changelog.txt:443
    old "- Restored Jenny confrontation about sleeping with Debbie.{#ssct_changelog}"
    new "- 恢复Jenny就与Debbie同床一事质问Anon的事件。{#ssct_changelog}"

    # game/changelog.txt:444
    old "- Connected up menu and location music as well as ambient sounds.{#ssct_changelog}"
    new "- 接入菜单、地点音乐和环境音。{#ssct_changelog}"

    # game/changelog.txt:445
    old "- Allowed pregnant variations of Jenny's visit scene to be unlocked in cookie jar.{#ssct_changelog}"
    new "- 允许在角色图鉴中解锁Jenny来访场景的孕期变体。{#ssct_changelog}"

    # game/changelog.txt:446
    old "- Updated crowd art for various locations, mainly around the college.{#ssct_changelog}"
    new "- 更新多个地点的人群美术，主要集中在学院周边。{#ssct_changelog}"

    # game/changelog.txt:447
    old "- Expanded the available replays to include all currently playable lewd content.{#ssct_changelog}"
    new "- 扩展可用回放，涵盖当前所有可游玩的成人内容。{#ssct_changelog}"

    # game/changelog.txt:448
    old "- Updated quick menu placement, and made it always available when enabled in settings.{#ssct_changelog}"
    new "- 更新快捷菜单位置；在设置中启用后，始终提供该菜单。{#ssct_changelog}"

    # game/changelog.txt:449
    old "- By popular demand, re-introduced a cheat menu. Yes, you still tap the wifi icon. Be persistent.{#ssct_changelog}"
    new "- 应广大玩家要求，重新加入作弊菜单。没错，还是点击WiFi图标。多试几次。{#ssct_changelog}"

    # game/changelog.txt:450
    old "- Restored some missing dialogues, including Debbie's shower scene.{#ssct_changelog}"
    new "- 恢复部分缺失对话，包括Debbie的淋浴场景。{#ssct_changelog}"

    # game/changelog.txt:451
    old "- Prevented some conflicts between Jenny and Debbie quests.{#ssct_changelog}"
    new "- 防止Jenny和Debbie的任务发生部分冲突。{#ssct_changelog}"

    # game/changelog.txt:452
    old "- Addressed transition timing issue in old art animations.{#ssct_changelog}"
    new "- 修正旧版美术动画中的转场时序问题。{#ssct_changelog}"

    # game/changelog.txt:453
    old "- Prevented scenario in which the wrench could be purchased more than once.{#ssct_changelog}"
    new "- 防止扳手被购买多次。{#ssct_changelog}"

    # game/changelog.txt:454
    old "- Fixed potential for unintentional save deletion when using the delete key.{#ssct_changelog}"
    new "- 修复使用删除键时可能意外删除存档的问题。{#ssct_changelog}"

    # game/changelog.txt:455
    old "- Improved a few prop descriptions to avoid accidental spoilers.{#ssct_changelog}"
    new "- 改进部分道具描述，避免无意剧透。{#ssct_changelog}"

    # game/changelog.txt:456
    old "- Added better names for some locations when being displayed on the back button.{#ssct_changelog}"
    new "- 改进返回按钮上部分地点的显示名称。{#ssct_changelog}"

    # game/changelog.txt:457
    old "- Clarified wording on mode select screen around why only one mode is currently available.{#ssct_changelog}"
    new "- 明确模式选择界面的说明，解释当前为何只有一种模式可用。{#ssct_changelog}"

    # game/changelog.txt:458
    old "- Updated to Ren'Py version 8.2.3.{#ssct_changelog}"
    new "- 将Ren'Py更新至8.2.3版。{#ssct_changelog}"

    # game/changelog.txt:459
    old "- Fixed various spelling, transition, and staging oversights.{#ssct_changelog}"
    new "- 修复多处拼写、转场和场景安排遗漏。{#ssct_changelog}"

    # game/changelog.txt:464
    old "- Expanded and re-exported all art assets at a much higher widescreen resolution.{#ssct_changelog}"
    new "- 将全部美术资源扩展并重新导出为分辨率更高的宽屏版本。{#ssct_changelog}"

    # game/changelog.txt:465
    old "- Rebuilt the entire codebase from scratch to improve performance and better support planned features.{#ssct_changelog}"
    new "- 从零重建整个代码库，提高性能并更好地支持计划中的功能。{#ssct_changelog}"

    # game/changelog.txt:466
    old "- Updated the posing to take advantage of new codebase, and the higher resolution assets.{#ssct_changelog}"
    new "- 更新角色姿势，以利用新代码库和更高分辨率的资源。{#ssct_changelog}"

    # game/changelog.txt: version heading term
    old "Preview{#ssct_changelog}"
    new "预览版{#ssct_changelog}"

    # game/changelog.txt: version heading term
    old "Hotfix{#ssct_changelog}"
    new "热修复{#ssct_changelog}"
