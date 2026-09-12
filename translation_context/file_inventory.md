# plot 文件清单

2026-09-12补充：7944源档案复核、日记覆盖、引擎验证和构建结果见`progress.md`最新记录。下方2026-08-03统计属于历史清单，不代表当前引擎的有效对白块数量；已按用户要求移除引擎确认的171个旧版orphan块。

更新时间：2026-08-03

本清单由仓库当前文件自动统计，用于人工安排精修顺序；“推定分组”和“主要说话人”仅作为定位线索，完成翻译前仍须通读完整文件及前后剧情。

## 总览

- `tl/zh_hans/src/plot` 下共有 **260** 个 `.rpy` 文件。
- 共包含 **35,091** 个 `translate zh_hans` 块和 **353** 组 `old/new` 字符串。
- 数字连续序列无缺号：`ano01-16`、`bar01-06`、`deb01-27`、`dia01-02`、`jen01-28`、`jud01-02`、`mar01-02`、`mel01-06`、`tin01-02`、`tor01-06`、`viv01-05`。
- 未发现内容完全相同的重复文件。是否存在废弃场景不能仅凭文件名判断，需结合游戏原始脚本和实际跳转关系确认。

## 序章/教程

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `+prologue.rpy` | 122 | 20 | 0 | mono、more |
| `+tutor.rpy` | 167 | 25 | 0 | tutor、extend |

## 主线/Anon

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `ano01.rpy` | 3664 | 609 | 3 | anon、erik、annie、eve、kevin、ursula |
| `ano02.rpy` | 729 | 121 | 0 | harold、debbie、anon、yumi |
| `ano03.rpy` | 1521 | 253 | 0 | anon、yumi、debbie、dimitri、jenny、mono |
| `ano04.rpy` | 261 | 43 | 0 | tammy、debbie、anon |
| `ano05.rpy` | 693 | 115 | 0 | debbie、anon、mono、jenny |
| `ano06.rpy` | 1977 | 329 | 0 | anon、dimitri、tony、igor、debbie、jenny |
| `ano07.rpy` | 1497 | 249 | 2 | tony、anon、maria |
| `ano08.rpy` | 26 | 4 | 1 | anon |
| `ano09.rpy` | 2311 | 385 | 1 | tony、anon、maria、tina、mono |
| `ano10.rpy` | 2257 | 321 | 4 | maria、anon、tony、extend |
| `ano11.rpy` | 2279 | 325 | 2 | tony、maria、anon、dimitri、tina、igor |
| `ano12.rpy` | 32 | 5 | 1 | anon |
| `ano13.rpy` | 3791 | 541 | 2 | anon、tony、tina、maria、becca、missy |
| `ano14.rpy` | 476 | 79 | 1 | anon、maria、tony |
| `ano15.rpy` | 5165 | 754 | 3 | tony、anon、maria、mono |
| `ano16.rpy` | 315 | 52 | 0 | tony、anon、maria |

## Debbie线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `deb01.rpy` | 465 | 77 | 0 | debbie、anon |
| `deb02.rpy` | 447 | 72 | 4 | anon、debbie |
| `deb03.rpy` | 1331 | 220 | 3 | debbie、anon、jenny、mono、more |
| `deb04.rpy` | 1131 | 188 | 0 | anon、jenny、debbie、mono、more |
| `deb05.rpy` | 1155 | 190 | 4 | debbie、anon、mono |
| `deb06.rpy` | 758 | 126 | 0 | anon、debbie |
| `deb07.rpy` | 848 | 141 | 0 | debbie、anon、mono、more |
| `deb08.rpy` | 2282 | 376 | 6 | anon、debbie、kassy、mono |
| `deb09.rpy` | 199 | 33 | 0 | anon、debbie、ursula |
| `deb10.rpy` | 530 | 88 | 0 | anon、jenny、debbie |
| `deb11.rpy` | 531 | 88 | 0 | anon、jenny、debbie |
| `deb12.rpy` | 802 | 132 | 3 | anon、debbie、jenny |
| `deb13.rpy` | 2937 | 487 | 4 | anon、debbie、josie、jiang、mono |
| `deb14.rpy` | 1182 | 194 | 5 | anon、debbie |
| `deb15.rpy` | 253 | 41 | 2 | anon、debbie |
| `deb16.rpy` | 1689 | 281 | 0 | anon、debbie、hym、lsd、jenny、mono |
| `deb17.rpy` | 399 | 66 | 0 | debbie、anon |
| `deb18.rpy` | 1071 | 178 | 0 | debbie、anon、dimitri、jenny、mono、igor |
| `deb19.rpy` | 1863 | 304 | 10 | debbie、anon、mono |
| `deb20.rpy` | 927 | 154 | 0 | diane、debbie、anon |
| `deb21.rpy` | 1833 | 305 | 0 | debbie、anon、jenny、rue、neil、mono |
| `deb22.rpy` | 739 | 122 | 2 | debbie、anon、ursula |
| `deb23.rpy` | 3984 | 660 | 6 | anon、debbie、kassy、mono、TODO、more |
| `deb24.rpy` | 2055 | 342 | 0 | debbie、anon、diane、mono |
| `deb25.rpy` | 2571 | 428 | 0 | debbie、anon、lsd、hym、mono |
| `deb26.rpy` | 5526 | 853 | 7 | anon、debbie、diane、titomi、hana、kassy |
| `deb27.rpy` | 800 | 133 | 0 | debbie、anon |

## Debbie支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `deb_baby.rpy` | 4612 | 758 | 16 | anon、debbie、jenny、diane、micoe、mono |
| `deb_island.rpy` | 925 | 153 | 2 | debbie、anon |
| `deb_kitchen.rpy` | 1233 | 205 | 1 | debbie、anon、jenny、mono |
| `deb_laundry.rpy` | 2003 | 333 | 2 | debbie、anon、mono |
| `deb_lobby.rpy` | 657 | 105 | 2 | debbie、anon |
| `deb_mall.rpy` | 3344 | 552 | 8 | debbie、anon、mono、more |
| `deb_pants.rpy` | 523 | 87 | 0 | debbie、anon |
| `deb_pool.rpy` | 339 | 56 | 0 | debbie、anon |
| `deb_shower.rpy` | 3163 | 526 | 2 | debbie、anon、mono |
| `deb_sink.rpy` | 1155 | 192 | 1 | debbie、anon |
| `deb_sleep.rpy` | 264 | 43 | 2 | anon、debbie |
| `deb_tv.rpy` | 4584 | 761 | 5 | debbie、anon、hym、mono、lsd |
| `deb_utility.rpy` | 80 | 13 | 0 | debbie、anon |
| `deb_visit.rpy` | 1777 | 295 | 2 | debbie、anon、mono |
| `debbie_attic.rpy` | 25 | 4 | 0 | mono、anon |
| `debbie_bed1.rpy` | 25 | 4 | 0 | anon |
| `debbie_bed2.rpy` | 43 | 7 | 0 | anon |
| `debbie_canvas.rpy` | 7 | 1 | 0 | anon |
| `debbie_drawer.rpy` | 21 | 3 | 0 | anon |
| `debbie_garage.rpy` | 49 | 8 | 0 | anon |
| `debbie_landing.rpy` | 25 | 4 | 0 | anon |
| `debbie_pants.rpy` | 43 | 7 | 0 | anon |
| `debbie_rug.rpy` | 405 | 67 | 0 | jenny、anon、mono、more |
| `debbie_tv.rpy` | 259 | 42 | 2 | anon、mono、debbie |
| `debbie.rpy` | 1277 | 207 | 9 | debbie、anon、TODO |

## Jenny线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `jen01.rpy` | 189 | 31 | 0 | anon、jenny |
| `jen02.rpy` | 351 | 58 | 0 | debbie、jenny、anon |
| `jen03.rpy` | 405 | 67 | 0 | anon、jenny、debbie、mono |
| `jen04.rpy` | 381 | 63 | 0 | anon、jenny、mans_voice |
| `jen05.rpy` | 931 | 129 | 7 | jenny、anon |
| `jen06.rpy` | 643 | 106 | 2 | anon、jenny |
| `jen07.rpy` | 1065 | 177 | 0 | anon、jenny、debbie |
| `jen08.rpy` | 1917 | 322 | 0 | anon、jenny、jane、ivy |
| `jen09.rpy` | 535 | 88 | 2 | anon、debbie、jenny、mono |
| `jen10.rpy` | 2331 | 388 | 0 | anon、jenny、grace、ivy |
| `jen11.rpy` | 288 | 46 | 0 | anon、jenny、debbie |
| `jen12.rpy` | 351 | 58 | 0 | anon、jenny |
| `jen13.rpy` | 451 | 75 | 0 | anon、jenny |
| `jen14.rpy` | 1248 | 192 | 0 | anon、jenny、debbie、cedric |
| `jen15.rpy` | 331 | 55 | 0 | jenny、anon |
| `jen16.rpy` | 1659 | 276 | 0 | jenny、anon、lily |
| `jen17.rpy` | 1767 | 293 | 0 | anon、erik、karl、pink、justin、jenny |
| `jen18.rpy` | 1083 | 180 | 0 | jenny、anon、mono |
| `jen19.rpy` | 343 | 57 | 0 | anon、jenny、debbie、mono |
| `jen20.rpy` | 439 | 73 | 0 | anon、jenny |
| `jen21.rpy` | 1035 | 172 | 0 | jenny、anon、mono |
| `jen22.rpy` | 357 | 59 | 0 | jenny、anon、debbie、mono |
| `jen23.rpy` | 1239 | 206 | 0 | jenny、anon |
| `jen24.rpy` | 1999 | 330 | 5 | jenny、anon、debbie、mono |
| `jen25.rpy` | 387 | 64 | 0 | anon、jenny、debbie、mono |
| `jen26.rpy` | 2697 | 449 | 0 | anon、jenny、zana、mono |
| `jen27.rpy` | 387 | 64 | 0 | anon、debbie、jenny |
| `jen28.rpy` | 969 | 161 | 1 | jenny、anon |

## Jenny支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `jen_baby.rpy` | 6094 | 919 | 11 | jenny、anon、debbie、diane、micoe、extend |
| `jen_cam.rpy` | 1173 | 195 | 0 | jenny、anon、mono、extend |
| `jen_deal.rpy` | 43 | 7 | 0 | jenny、anon |
| `jen_finger.rpy` | 577 | 95 | 2 | jenny、anon |
| `jen_gfe.rpy` | 2197 | 365 | 2 | jenny、anon、mono |
| `jen_pool.rpy` | 939 | 156 | 0 | jenny、anon、mono |
| `jen_shower.rpy` | 1963 | 326 | 2 | anon、jenny |
| `jen_sleep.rpy` | 822 | 133 | 6 | jenny、anon |
| `jen_table.rpy` | 951 | 158 | 0 | jenny、anon、debbie、mono |
| `jen_tv.rpy` | 873 | 145 | 1 | jenny、anon |
| `jen_visit.rpy` | 235 | 38 | 2 | jenny、anon、mono |
| `jenny_laptop.rpy` | 903 | 150 | 0 | jenny、anon |
| `jenny.rpy` | 926 | 150 | 7 | jenny、anon |

## Diane线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `dia01.rpy` | 597 | 99 | 0 | diane、anon、mono、more |
| `dia02.rpy` | 837 | 139 | 0 | diane、anon、mono |

## Diane支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `diane_lobby.rpy` | 19 | 3 | 0 | anon |
| `diane_plot.rpy` | 69 | 11 | 0 | anon、diane |
| `diane.rpy` | 65 | 9 | 3 | diane、anon |

## 酒吧线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `bar01.rpy` | 663 | 110 | 0 | barb、anon、ursula、mia、mono、more |
| `bar02.rpy` | 2025 | 337 | 0 | anon、barb、mia、eve、chad、mono |
| `bar03.rpy` | 1857 | 309 | 0 | anon、barb、mia、melody、kevin、jane |
| `bar04.rpy` | 3585 | 597 | 0 | anon、barb、judith、mia、ursula、mono |
| `bar05.rpy` | 2817 | 469 | 0 | anon、barb、mia、annie、ursula、lily |
| `bar06.rpy` | 1185 | 197 | 0 | barb、anon、iwanka |

## Maria线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `mar01.rpy` | 1095 | 167 | 0 | maria、anon |
| `mar02.rpy` | 171 | 28 | 0 | tony、anon |

## Maria支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `mar_baby.rpy` | 2529 | 397 | 3 | anon、maria、tony、micoe |
| `mar_cook.rpy` | 272 | 67 | 2 | maria、anon |
| `mar_couch.rpy` | 3437 | 640 | 0 | maria、tony、anon、mono |
| `mar_dark.rpy` | 2590 | 370 | 1 | maria、tony、anon |
| `mar_door.rpy` | 560 | 140 | 0 | maria、anon |
| `mar_kitchen.rpy` | 231 | 38 | 0 | anon、maria |
| `mar_pantry.rpy` | 360 | 90 | 0 | maria、anon、extend |
| `maria_lounge.rpy` | 72 | 13 | 0 | anon、maria、TODO |
| `maria.rpy` | 385 | 60 | 7 | maria、anon |

## Melody线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `mel01.rpy` | 1887 | 314 | 0 | anon、melody、judith、erik、mono、ursula |
| `mel02.rpy` | 3235 | 475 | 0 | anon、eve、erik、melody、roxxy、kevin |
| `mel03.rpy` | 1039 | 167 | 0 | anon、melody、ursula、kevin、eve、annie |
| `mel04.rpy` | 724 | 181 | 0 | anon、melody、eve、tyrone、ursula、chad |
| `mel05.rpy` | 1108 | 277 | 0 | anon、erik、kevin、eve、mono、melody |
| `mel06.rpy` | 1344 | 336 | 0 | anon、melody、eve、kevin、mono、annie |

## Tina线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `tin01.rpy` | 181 | 30 | 0 | tina、anon、becca |
| `tin02.rpy` | 1030 | 167 | 0 | anon、tina、liu |

## Tina支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `tin_baby.rpy` | 1762 | 338 | 4 | anon、tina、becca、TODO、micoe |
| `tin_cubicle.rpy` | 7 | 1 | 0 | anon |
| `tin_dusk.rpy` | 1001 | 167 | 0 | tina、anon |
| `tin_vault.rpy` | 1231 | 204 | 2 | tina、anon、liu、tim |
| `tina_lounge.rpy` | 212 | 31 | 3 | anon、tina、TODO |
| `tina.rpy` | 251 | 37 | 1 | tina、anon |

## Tori线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `tor01.rpy` | 2151 | 358 | 0 | anon、tori、konty、mia、mono、erik |
| `tor02.rpy` | 2829 | 471 | 0 | anon、tori、judith、erik、june、mono |
| `tor03.rpy` | 1599 | 266 | 0 | anon、tori、june、erik、mono |
| `tor04.rpy` | 627 | 104 | 0 | tori、ursula、anon、mono |
| `tor05.rpy` | 2727 | 450 | 7 | anon、tori、ursula、annie、mono、vee |
| `tor06.rpy` | 1053 | 175 | 1 | anon、tori、mono |

## Tori支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `tor_office.rpy` | 375 | 62 | 0 | tori、anon |
| `tori.rpy` | 110 | 16 | 4 | tori、anon |

## Vivian线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `viv01.rpy` | 1322 | 219 | 3 | anon、viv、june、judith、jane、eve |
| `viv02.rpy` | 1664 | 276 | 3 | anon、viv、jane、ursula、mono、erik |
| `viv03.rpy` | 2138 | 354 | 5 | viv、anon、mia、roxxy、ursula、jane |
| `viv04.rpy` | 3771 | 626 | 5 | anon、roxxy、jenny、viv、bridget、debbie |
| `viv05.rpy` | 871 | 144 | 2 | viv、anon、mono、ursula、more |

## Vivian支线/场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `viv_office.rpy` | 85 | 14 | 0 | viv、anon |

## Ella线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `ell01.rpy` | 61 | 10 | 0 | anon、ella、mono |

## Josie线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `jos01.rpy` | 2359 | 392 | 2 | anon、josie、yoshi、yoo |

## Judith线

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `jud01.rpy` | 97 | 16 | 0 | judith、anon |
| `jud02.rpy` | 842 | 116 | 8 | anon、judith、camila、val |

## 独立角色/地点/物品场景

| 文件 | 行数 | 翻译块 | old/new | 主要说话人（推定） |
|---|---:|---:|---:|---|
| `ang.rpy` | 49 | 7 | 2 | anon、ang |
| `annie.rpy` | 88 | 14 | 2 | anon、annie |
| `anon_chair.rpy` | 31 | 5 | 0 | anon |
| `anon_pc.rpy` | 92 | 15 | 0 | anon、mono |
| `anon_phone.rpy` | 50 | 8 | 0 | anon |
| `apt_empty.rpy` | 25 | 4 | 0 | anon |
| `ari_stall.rpy` | 124 | 31 | 0 | anon、ariane |
| `bank_hall.rpy` | 15 | 2 | 0 | anon |
| `bank_lobby.rpy` | 43 | 7 | 0 | anon、more |
| `bank_vault.rpy` | 13 | 2 | 0 | anon |
| `bar_office.rpy` | 49 | 8 | 0 | anon、barb |
| `barb.rpy` | 287 | 40 | 12 | barb、anon |
| `bridget.rpy` | 155 | 25 | 2 | bridget、anon |
| `car_garage.rpy` | 13 | 2 | 0 | anon |
| `car_lounge.rpy` | 13 | 2 | 0 | anon |
| `car_shop.rpy` | 19 | 3 | 0 | anon |
| `cedric.rpy` | 473 | 77 | 3 | cedric、anon |
| `dexter.rpy` | 42 | 6 | 2 | dexter、anon |
| `ella.rpy` | 25 | 4 | 0 | anon、ella |
| `emm_stall.rpy` | 40 | 10 | 0 | anon、emma |
| `erik_bed.rpy` | 13 | 2 | 0 | anon |
| `erik_drawer.rpy` | 19 | 3 | 0 | anon |
| `erik.rpy` | 80 | 9 | 7 | anon、erik |
| `eve.rpy` | 275 | 44 | 3 | eve、anon |
| `gym_workout.rpy` | 13 | 2 | 0 | anon |
| `hana.rpy` | 377 | 59 | 8 | hana、anon |
| `helen_bed1_scope.rpy` | 49 | 8 | 0 | anon |
| `helen_bed2_scope.rpy` | 103 | 17 | 0 | anon |
| `helen_lobby.rpy` | 13 | 2 | 0 | anon |
| `ind_stall.rpy` | 68 | 17 | 0 | anon、indira |
| `ivy.rpy` | 103 | 16 | 2 | ivy、anon |
| `jane.rpy` | 47 | 4 | 6 | jane、anon |
| `jos_trade.rpy` | 833 | 133 | 9 | josie、anon |
| `josie.rpy` | 102 | 16 | 2 | josie、anon |
| `jud_stall.rpy` | 553 | 92 | 0 | judith、anon |
| `judith.rpy` | 124 | 19 | 3 | judith、anon |
| `june.rpy` | 72 | 11 | 2 | anon、june |
| `kassy.rpy` | 79 | 12 | 2 | kassy、anon |
| `kevin.rpy` | 152 | 25 | 0 | kevin、anon |
| `key_school.rpy` | 25 | 4 | 0 | anon |
| `konty.rpy` | 219 | 36 | 0 | konty、anon |
| `library_lobby.rpy` | 21 | 3 | 0 | anon |
| `library_shelf.rpy` | 239 | 38 | 3 | jane、anon |
| `library_study.rpy` | 135 | 22 | 0 | anon、jane |
| `lily.rpy` | 152 | 23 | 4 | lily、anon |
| `liu.rpy` | 102 | 16 | 2 | liu、anon |
| `mall_booth.rpy` | 25 | 4 | 0 | anon |
| `mall_hall1.rpy` | 18 | 2 | 2 | anon |
| `mel_office.rpy` | 397 | 98 | 2 | melody、anon |
| `melody.rpy` | 158 | 24 | 2 | melody、anon |
| `mia.rpy` | 62 | 10 | 1 | anon、mia |
| `micoe.rpy` | 37 | 5 | 2 | anon、micoe |
| `misc_lotion.rpy` | 13 | 2 | 0 | anon |
| `misc_tissue.rpy` | 13 | 2 | 0 | anon |
| `misc_toad.rpy` | 7 | 1 | 0 | anon |
| `misc_towel.rpy` | 13 | 2 | 0 | anon |
| `note_tori.rpy` | 19 | 3 | 0 | anon |
| `oli_stall.rpy` | 292 | 73 | 0 | olivia、anon |
| `photo_debbie_diane.rpy` | 13 | 2 | 0 | anon |
| `pie_stall.rpy` | 112 | 28 | 0 | anon、pietro |
| `pizza_boxes.rpy` | 273 | 45 | 0 | anon、maria、tony |
| `pizza_kitchen.rpy` | 13 | 2 | 0 | anon |
| `pizza_main.rpy` | 21 | 3 | 0 | anon |
| `pizza_shop.rpy` | 49 | 8 | 0 | anon |
| `roxxy.rpy` | 276 | 45 | 2 | roxxy、anon |
| `sam_stall.rpy` | 108 | 27 | 0 | anon、sammy |
| `school_boiler.rpy` | 7 | 1 | 0 | anon |
| `school_girls.rpy` | 19 | 3 | 0 | anon |
| `school_hall1.rpy` | 37 | 5 | 2 | anon |
| `school_locker.rpy` | 25 | 4 | 0 | anon |
| `school_office1.rpy` | 103 | 17 | 0 | ursula、anon |
| `school_office2.rpy` | 19 | 3 | 0 | anon |
| `school_pa.rpy` | 615 | 102 | 0 | pa、anon |
| `specs_judith.rpy` | 13 | 2 | 0 | anon |
| `sue_stall.rpy` | 40 | 10 | 0 | anon、sue |
| `sushi_shop.rpy` | 13 | 2 | 0 | anon |
| `tammy_bed1_scope.rpy` | 103 | 17 | 0 | anon |
| `tammy_bed2_scope.rpy` | 165 | 27 | 0 | anon |
| `tammy_lobby.rpy` | 25 | 4 | 0 | anon |
| `tammy_yard_scope.rpy` | 61 | 10 | 0 | anon |
| `tech_gamepad.rpy` | 13 | 2 | 0 | anon |
| `ten_stall.rpy` | 124 | 31 | 0 | anon、tenzin |
| `titomi.rpy` | 367 | 60 | 2 | titomi、anon |
| `ton_baby.rpy` | 884 | 152 | 1 | tony、anon |
| `tony.rpy` | 401 | 59 | 4 | tony、anon |
| `tool_drill.rpy` | 15 | 2 | 0 | anon |
| `tool_shovel.rpy` | 259 | 43 | 0 | anon、jenny |
| `tv.rpy` | 87 | 14 | 0 | anon |
| `tym_stall.rpy` | 28 | 7 | 0 | anon、tyme |
| `ursula.rpy` | 49 | 8 | 0 | anon、ursula |
| `vee.rpy` | 161 | 26 | 2 | vee、anon |
| `viv.rpy` | 158 | 24 | 4 | viv、anon |
| `yoo.rpy` | 281 | 45 | 3 | yoo、anon |
| `yoshi.rpy` | 84 | 13 | 2 | yoshi、anon |
| `zana.rpy` | 32 | 5 | 0 | zana、anon |


## 2026-09-12 前后对白审校覆盖口径

本次以21.0.0-wip.7944为准，对全部260个剧情翻译文件进行候选与入口定位；全库323个RPY另做结构和术语等静态审计。候选及补充阅读涉及132个剧情文件，包含通用人物交互、主线推进、初次／重复场景、忙碌拒绝、被打断、收尾、次晨及孕育后续。

47个核心文件的2705条较长候选完成英中对照，其他69个文件的3426条候选完成译文审阅及重点英中复核；另补查74个文件中的5928条未入前两组的较长条目，补读jen20、june并检查短否定回答。上述组有文件交集，候选也可能含非目标剧情或露骨段落，数量不是场景完成率。保留正确译文，实际只修改44个文件243处译文。

本轮完成的是已约定的非露骨前后对白专项系统复核，不是全部对白逐句重译，也不表示露骨段落已全面精修；未通过运行游戏逐场景验证。具体结果见progress.md，场景解释见storylines.md。

## 2026-09-12 全库筛查与第二遍复核口径

- 自动筛查323个文件、37947对原译文本。工具生成1347组重复候选、451组相似候选；人工处理20条专项标记、116条补充候选，并核对7组高差异重复句及2组同译相似句。候选可能重叠，不能相加为独立句数，也不代表逐一精读全部1798组。
- 回看前轮244条非露骨修改记录（243处净改动）、62条连贯性记录及51条语义记录，按当前文件确认，包含已按用户反馈撤回的2条Tina修改；历史日志不是当前译文依据。
- Jenny日记36页、296个片段按7944原始常量页序全读，修改后再次连读，重点复核分段、旁注指代及情绪转折。
- 本轮净改动100处、16个翻译文件：bytecode_strings75处（74处日记、1处标题），prop5处，14个剧情文件合计20处。保留正确译文和角色有意使用的科学术语。
- 这是全库筛查与疑点语境复核，不是37947条全部逐句重译或游戏内全分支验证。

## 2026-09-13 连续审读文件清单

完整读取下列文件的英中配对文本，共31个文件、2121对；包含菜单和空文本。疑点再查7944源码动作与分支，不能仅以相邻译文推断运行顺序。修改后复核关键句组及同源变体。此清单是本轮真实覆盖，不表示其余文件已完成逐句审读。

| 文件 | 原译对数 | 本轮改动 |
|---|---:|---:|
| barb.rpy | 51 | 5 |
| bar_office.rpy | 8 | 0 |
| diane.rpy | 11 | 2 |
| diane_lobby.rpy | 3 | 2 |
| diane_plot.rpy | 11 | 3 |
| erik.rpy | 15 | 3 |
| eve.rpy | 46 | 5 |
| judith.rpy | 21 | 1 |
| june.rpy | 12 | 0 |
| maria.rpy | 56 | 0 |
| melody.rpy | 25 | 0 |
| mia.rpy | 10 | 0 |
| roxxy.rpy | 46 | 0 |
| tin01.rpy | 30 | 5 |
| tina.rpy | 37 | 6 |
| tina_lounge.rpy | 33 | 6 |
| tin_cubicle.rpy | 1 | 0 |
| tony.rpy | 59 | 0 |
| tori.rpy | 19 | 3 |
| viv.rpy | 27 | 0 |
| viv_office.rpy | 14 | 0 |
| debbie.rpy | 215 | 25 |
| jenny.rpy | 156 | 2 |
| tor_office.rpy | 62 | 5 |
| bar01.rpy | 110 | 4 |
| dia01.rpy | 99 | 21 |
| jud_stall.rpy | 92 | 2 |
| mel_office.rpy | 99 | 0 |
| tin_dusk.rpy | 166 | 22 |
| viv01.rpy | 221 | 6 |
| jen_gfe.rpy | 366 | 10 |

## 2026-09-13 人工路径台账增量

本次新增804条记录，累计847/37947条。+tutor全24条；anon_chair全5条；ano01全611条（含3菜单）；bar04仅Annie模特邀请7条；bar05仅原脚本350–707范围157条。加上先前序章、Annie、Ang共43条。数量指逐项登记的已读文本，不是全部场景完成率。

+tutor本地条件已核对；ano01等文件即使文本全读，外围事件注册与未核实的跨任务调用仍保留待审状态。bar04、bar05未读部分明确不计覆盖。后续以manual_review.json的条目、源范围和指纹为准。

## 2026-09-13 美术后续人工路径增量

新增569条，累计1416/37947条：bar05由157增至469条（本地全文），bar06全197条，bar_office全8条，barb全51条，mini/paint唯一提示1条。bar05_art2调色重试、bar06首次/重复与办公室位置分支、barb邀请接受/拒绝均已连读。

已核对部分匹配版逻辑：取布及服装流转、预约日期与等待、画像后14天等待结果、获奖及首次完成后进入重复事件。完整事件装饰器、共享菜单与小游戏底层回调仍待审，相关文件保持local_paths_reviewed；数量不代表已验证所有运行路径。

## 2026-09-13 美术前半段人工路径增量

新增756条，累计2172/37947条：bar01全110条、bar02全337条、bar03全309条。对照源脚本连读全部本地标签、条件、被打断对白、场外发言和共用片段；关键物品与返回值逻辑另有核对记录。

bar02的背包不同持有状态、Chad交换/找Eve索回两路线，bar03的三类杂志不同收集进度及Melody答题成功/失败均已记录。完整事件装饰器、共享角色菜单和bar04未读段继续待审，保持local_paths_reviewed，不把文件文本读完写成所有运行路径完成。
