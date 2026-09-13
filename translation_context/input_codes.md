# 游戏内输入代码与翻译兼容

更新时间：2026-09-13

用途与维护方式见[index.md](index.md)。

适配依据：21.0.0-wip.7944，本地 `saga.data.jenny_laptop`、`saga.data.anon_pc`、`saga.tech.computer`、`saga.store`、`saga.tech.television` 的字节码及 `src/mini/pc.rpy`。仅核对游戏内谜题输入，不涉及真实账号认证。

| 输入位置 | 原校验值 | 可输入写法 | 规则 |
| --- | --- | --- | --- |
| Jenny电脑 | `badmonster`，输入类转成大写校验 | `badmonster`、`BADMONSTER` | 按本体原键校验，不翻译、不加中文别名，也不接受带空格的 `BAD MONSTER`；中文“坏怪物”不是密码 |
| Anon电脑 | `cookies`，输入类转成大写校验 | `cookies`、`COOKIES` | 必须输入英文原值；不提供中文别名 |
| 电视订阅代码 | `L6bv12R` | 保持原值 | 大小写敏感，不翻译、不自动转成大写 |
| 电视密码 | `12345` | 保持原值 | 保留原校验，不增加别名 |

密码与输入代码一律按本体原键校验：不翻译校验值，也不在翻译侧增加中文别名或空格兼容。玩家可见的线索文本（日记、提示、道具说明）保留游戏实际校验的英文写法，例如 Jenny 日记中的 `坏怪物（Bad Monster）` 用来指认道具英文名；玩家输入仍须是 `badmonster` / `BADMONSTER`。

运行时数据属性：两台电脑的登录提示（`prop.anon_pc.hint = 'Sticky'`、`prop.jenny_laptop.hint = 'My favorite toy ;)'`）和电脑桌面／窗口标题显示的 `app.name`（`Homework`、`Photos`、`Recycle Bin` 等）来自编译数据，不经过 Ren'Py 字符串翻译表。按用户决定，翻译侧不再保留 `hint_translations.rpy` 一类的运行时覆盖脚本，也不再保留 `input_code_aliases.rpy` 输入别名脚本；应用名以 `tl/zh_hans/extracted/anon_pc_jenny_laptop.rpy` 的 `old`/`new` 登记为准（`Homework→家庭作业`、`Photos→照片`、`Recycle Bin→回收站` 等），提示文本保持本体数据值。

新增同类翻译前必须同时检查：显示线索、原始校验值、输入类的字符限制/大小写/空格处理、提交方法及成功事件。可翻译的谜题词语优先使用 `old`/`new` 替换；数字、随机字母代码默认保留原值。不得全局翻译输入、放宽所有密码、改写原始键，或让无效输入直接触发成功。

尚未验证项：本体升级后须重新核对 `saga.tech.computer` 的认证类接口、两台电脑的提示与 `app.name` 显示路径。`src/mini/pc.rpy` 的 `pc_explorer` 直接用 `text app.name` 渲染桌面图标，不经 `__()`；若游戏内出现英文应用名，需要按上述说明补 `old`/`new` 或重新评估是否需要运行时处理。未进行场景游玩、实际 IME 输入或读档验证。
