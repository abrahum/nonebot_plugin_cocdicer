from .util import MessageEvent, GroupMessageEvent
from .dices import help_message, st, en, rd0
from .madness import ti, li
from .investigator import Investigator
from .san_check import sc
from .cards import (
    cards,
    cache_cards,
    set_handler,
    show_handler,
    sa_handler,
    del_handler,
)

from nonebot import get_driver, require
from nonebot.rule import Rule
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith, PluginMetadata
from nonebot.adapters import Bot as Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v12 import Bot as V12Bot

__plugin_meta__ = PluginMetadata(
    name="CoC骰娘",
    description="CoC相关指令插件，包含属性骰、技能骰、理智检查、角色卡管理等功能。",
    usage=""".help 查看帮助信息
.st 属性骰
.en 技能骰 [技能值]
.ti 进行理智检查
.li 进行理智恢复
.coc [年龄] 生成调查员角色卡
.sc [检定内容] 进行San值检查
.rh [检定内容] 私聊进行属性/技能检定
.r [检定内容] 进行属性/技能检定
.set [属性/技能] [数值] 设置角色卡属性或技能值
.show [属性/技能] 显示角色卡属性或技能值
.sa [属性/技能] 显示所有符合条件的属性或技能值
.del [属性/技能] 删除角色卡中的某项属性或技能值
""",
    author="AbrahumLink",
    license="GPL-3.0",
    type="application",
    homepage="https://github.com/abrahum/nonebot_plugin_cocdicer",
    supported_adapters={"~onebot.v11", "~onebot.v12"},
)

driver = get_driver()

require("nonebot_plugin_localstore")


@driver.on_startup
async def _():
    cards.load()


def is_group_message() -> Rule:
    async def _is_group_message(bot: Bot, event: MessageEvent) -> bool:
        return True if type(event) is GroupMessageEvent else False

    return Rule(_is_group_message)


rdhelp = on_startswith(".help", priority=2, block=True)
stcommand = on_startswith(".st", priority=2, block=True)
encommand = on_startswith(".en", priority=2, block=True)
ticommand = on_startswith(".ti", priority=2, block=True)
licommand = on_startswith(".li", priority=2, block=True)
coccommand = on_startswith(".coc", priority=2, block=True)
sccommand = on_startswith(".sc", priority=2, block=True)
rhcommand = on_startswith(".rh", priority=3, block=True)
rdcommand = on_startswith(".r", priority=4, block=True)
setcommand = on_startswith(".set", priority=5, block=True)
showcommand = on_startswith(".show", priority=5, block=True)
sacommand = on_startswith(".sa", priority=5, block=True)
delcommand = on_startswith(".del", priority=5, block=True)


@rdhelp.handle()
async def rdhelphandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip()
    await matcher.finish(help_message(args))


@stcommand.handle()
async def stcommandhandler(matcher: Matcher):
    await matcher.finish(st())


@encommand.handle()
async def enhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip()
    await matcher.finish(en(args))


@rhcommand.handle()
async def rhcommandhandler(bot: Bot, event: GroupMessageEvent):
    args = str(event.get_message())[3:].strip()
    uid = event.get_user_id()
    if args and "." not in args:
        print("get here")
        if isinstance(bot, V12Bot):
            from nonebot.adapters.onebot.v12 import MessageSegment

            await bot.send_message(
                detail_type="private",
                user_id=uid,
                message=[MessageSegment.text(rd0(args))],
            )
        elif isinstance(bot, V11Bot):
            await bot.send_private_msg(user_id=uid, message=rd0(args))


@rdcommand.handle()
async def rdcommandhandler(event: MessageEvent):
    args = str(event.get_message())[2:].strip()
    if args and "." not in args:
        await rdcommand.finish(rd0(args))


@coccommand.handle()
async def cochandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip()
    try:
        args = int(args)
    except ValueError:
        args = 20
    inv = Investigator()
    await matcher.send(inv.age_change(args))
    if 15 <= args < 90:
        cache_cards.update(event, inv.__dict__, save=False)
        await matcher.finish(inv.output())


@ticommand.handle()
async def ticommandhandler(
    matcher: Matcher,
):
    await matcher.finish(ti())


@licommand.handle()
async def licommandhandler(
    matcher: Matcher,
):
    await matcher.finish(li())


@sccommand.handle()
async def schandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip().lower()
    await matcher.finish(sc(args, event=event))


@setcommand.handle()
async def sethandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().lower()
    await matcher.finish(set_handler(event, args))


@showcommand.handle()
async def showhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip().lower()
    for msg in show_handler(event, args):
        await matcher.send(msg)


@sacommand.handle()
async def sahandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip().lower()
    await matcher.finish(sa_handler(event, args))


@delcommand.handle()
async def delhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().lower()
    for msg in del_handler(event, args):
        await matcher.send(msg)
