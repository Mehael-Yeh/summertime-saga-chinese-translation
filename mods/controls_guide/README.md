# 控制说明Mod / Controls guide

在设置中新增“控制 / Controls”页，以可滚动的“按键—功能”表格展示14项通用操作、5项小游戏操作及使用说明。文字跟随当前游戏语言切换；英文为默认语言，支持`zh_hans`中文。它只提供说明，不改按键绑定或游戏玩法。

## 安装 / Install

关闭游戏，将本目录的`controls_guide.rpy`复制到`游戏目录/game/mods/controls_guide/`，然后启动游戏，打开设置→控制。无需改动原版脚本。仓库发包流程会自动包含此Mod。

Close the game, copy `controls_guide.rpy` into `game/mods/controls_guide/`, then open Settings → Controls. No original script needs to be replaced.

## 卸载 / Uninstall

先在设置中切换到“显示”等原有页面，再关闭游戏。删除`game/mods/controls_guide/`内的`controls_guide.rpy`及同名编译文件`controls_guide.rpyc`。不删除存档或其他Mod。

Select an original settings tab, such as Display, before quitting. Remove this mod's `.rpy` and `.rpyc` files; keep saves and other mods.

## 兼容与验证 / Compatibility

- 已在`21.0.0-wip.8194`PC版隔离副本验证：英文→中文→英文，标签动作、表格顶部／底部、滚动与返回原版显示页；未逐个实际触发所列快捷键，也未验收触屏布局。
- 触屏版原有“控制”设置保留，本Mod入口显示为“键盘 / Keyboard”。
- 接入原版设置的标签栏及滚动区，保留现有设置内容；若未来版本布局无法唯一识别，不注入并写入游戏日志。游戏更新时需重新核对按键表与布局，不能沿用旧版验收结论。
- 翻译使用Mod专用上下文键，避免与汉化包已有`Controls`等译文重复注册。中文字体由已安装的汉化包提供。

Verified on the 8194 PC build with English/Chinese language switching, tab actions and scrolling. Future layouts and touch devices need separate verification. Chinese display requires the translation pack's fonts.
