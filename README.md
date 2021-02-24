<div align="center">

# NoneBot Plugin COC-Dicer

COC骰子娘插件 For Nonebot2

</div>

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/abrahum/nonebot-plugin-cocdicer/master/LICENSE">
    <img src="https://img.shields.io/github/license/abrahum/nonebot_plugin_cocdicer.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-cocdicer">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-cocdicer.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

## 使用方法

``` zsh
nb plugin install nonebot-plugin-cocdicer // or
pip install --upgrade nonebot-plugin-cocdicer
```
在 Nonebot2 入口文件（例如 bot.py ）增加：
``` python
nonebot.load_plugin("nonebot_plugin_cocdicer")
```
启动机器人后，输入 `.help` 获取帮助信息。

## 骰娘技能

- Done or Will be done soon

    - [x] .r    投掷指令
    - [x] .sc   san check
    - [x] .st   射击命中判定
    - [x] .ti   临时疯狂症状
    - [x] .li   总结疯狂症状
    - [x] .coc  coc角色作成
    - [x] .help 帮助信息
    - [x] .en   技能成长

- To Do

    - [ ] .set  设定
    - [ ] .rule 规则速查

## 指令详解

```
.r[dah#bp] a_number [+/-]ex_number
```
- d：骰子设定指令，标准格式为 xdy ， x 为骰子数量 y 为骰子面数， x 为1时可以省略， y 为100时可以省略；
- a：检定指令，根据后续 a_number 设定数值检定，注意 a 必须位于 a_number 之前，且 a_number 前需使用空格隔开；
- h：暗骰指令，骰子结构将会私聊发送给该指令者；（没测试过非好友，可以的话先加好友吧）
- #：多轮投掷指令， # 后接数字即可设定多轮投掷，注意 # 后数字无需空格隔开；
- b：奖励骰指令，仅对 D100 有效，每个 b 表示一个奖励骰；
- p：惩罚骰指令，同奖励骰；
- +/-：附加计算指令，目前仅支持数字，同样无需空格隔开。

> 举几个栗子：
> - `.r#2bba 70`：两次投掷 1D100 ，附加两个奖励骰，判定值为70；
> - `.rah`：D100暗骰，由于没有 a_number 参数，判定将被忽略；
> - `.ra2d8+10 70`：2D8+10，由于非D100，判定将被忽略。

以上指令理论上均可随意变更顺序并嵌套使用，如果不能，就是出bug了_(:3」∠)_

```
.sc success/failure san_number
```
- success：判定成功降低 san 值，支持 x 或 xdy 语法（ x 与 y 为数字）；
- failure：判定失败降低 san 值，支持语法如上；
- san_number：当前 san 值。

```
.en skill_level
```

- skill_level：需要成长的技能当前等级。

```
.coc age
```
- age：调查员年龄

> 交互式调查员创建功能计划中

## 特别鸣谢

[nonebot/nonebot2](https://github.com/nonebot/nonebot2/)：简单好用，扩展性极强的 Bot 框架

[Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：更新迭代快如疯狗的 [OneBot](https://github.com/howmanybots/onebot/blob/master/README.md) Golang 原生实现

