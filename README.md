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
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">
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

遇到任何问题，欢迎开 Issue ~

## 骰娘技能

- Done or Will be done soon

    - [x] .r    投掷指令
    - [x] .rh   暗投指令
    - [x] .sc   san check
    - [x] .st   射击命中判定
    - [x] .ti   临时疯狂症状
    - [x] .li   总结疯狂症状
    - [x] .coc  coc角色作成
    - [x] .help 帮助信息
    - [x] .en   技能成长
    - [x] .set  角色卡设定
    - [x] .show 角色卡查询
    - [x] .sa   快速检定指令
    - [x] .del  删除信息

- To Do

    - [ ] .kp   KP模式
    - [ ] .pc   多角色卡管理、转让
    - [ ] .rule 规则速查（优先级较低）
    - [ ] set 技能值设定、sa 组合检定
    - [ ] en 使用保存的技能数值

## 指令详解

以下指令中 `<expr>` 均指骰子表达式，`[xx]` 表示 int ，具体可以参照 [diro](https://github.com/abrahum/diro) 以及 [onedice](https://github.com/OlivOS-Team/onedice)

```
.r<expr>#[times] [anum]
```

- #：多轮投掷指令，# 后接数字即可设定多轮投掷。
- anum：检定数值（后续将会支持属性检定）

> 举几个栗子：
> - `.rdbba#2 70`：两次投掷 1D100 ，附加两个奖励骰，判定值为70；
> - `.ra2d8+10 70`：2D8+10，由于非D100，判定将被忽略。

```
.rh<expr>#<times> <anum>
```

除了是暗投，应该和 .r 完全一致

```
.sc <success>/<failure> [san_number]
```
- success：判定成功降低 san 值，支持 x 或 xdy 语法（ x 与 y 为数字）；
- failure：判定失败降低 san 值，支持语法如上；
- san_number：当前 san 值，缺省 san_number 将会自动使用保存的人物卡数据。

```
.en skill_level
```

- skill_level：需要成长的技能当前等级。

```
.coc [age]
```
- age：调查员年龄，缺省 age 默认年龄 20

> 交互式调查员创建功能计划中

```
.set [attr_name] [attr_num]
```
- attr_name：属性名称，例:name、名字、str、力量
- attr_num：属性值
- **可以单独输入 .set 指令，骰娘将自动读取最近一次 coc 指令结果进行保存**

| 属性名称 | 缩写  |
| :------: | :---: |
|   名称   | name  |
|   年龄   |  age  |
|   力量   |  str  |
|   体质   |  con  |
|   体型   |  siz  |
|   敏捷   |  dex  |
|   外貌   |  app  |
|   智力   |  int  |
|   意志   |  pow  |
|   教育   |  edu  |
|   幸运   |  luc  |
|   理智   |  san  |

```
.show[s] [@xxx]
```
- .shows 查看技能指令
- 查看指定调查员保存的人物卡，缺省 at 则查看自身人物卡

```
.sa [attr_name]
```
- attr_name：属性名称，例:name、名字、str、力量

```
.del [c|card|xxx]
```

- c：清空暂存的人物卡
- card：删除使用中的人物卡(慎用)
- xxx：其他任意技能名
- 以上指令支持多个混合使用，多个参数使用空格隔开

## Change Log

### 0.4.0

- use diro-py
- support OneBot V12

### 0.3.1

- fix dependencies #5

### 0.3.0

- 适配 Nonebot 2.0.0-beta.1

### 0.2.5

- 暗投错误的使用了 get_session_id，已修复使用 get_user_id。

### 0.2.4

- 临时紧急修复 sc 指令逻辑问题（竟然还有人用这个插件）
- 不保证修完没 bug
- 用了怎么也不 star （小声bb）

### 0.2.2

- 增加技能系统
- 增加 del 指令(总感觉 del 还有大 bug ···)

### 0.2.1

- 增加 set 、 show 、 sa 指令
- 帮助信息重构

## 特别鸣谢

[nonebot/nonebot2](https://github.com/nonebot/nonebot2/)：简单好用，扩展性极强的 Bot 框架

[Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：更新迭代快如疯狗的 [OneBot](https://github.com/howmanybots/onebot/blob/master/README.md) Golang 原生实现
