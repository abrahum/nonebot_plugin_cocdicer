from .dices import rd, help_message, st, en
from .madness import ti, li
from .investigator import Investigator
from .san_check import sc
from .cards import _cachepath, cards, cache_cards, set_handler, show_handler, sa_handler, del_handler

from nonebot import get_driver
from nonebot.rule import Rule
from nonebot.plugin import on_startswith, on_regex
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent

import os

driver = get_driver()


@driver.on_startup
async def _on_startup():  # 角色卡暂存目录初始化
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(_cachepath):
        with open(_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    cards.load()


def is_group_message() -> Rule:
    async def _is_group_message(bot: "Bot", event: "Event") -> bool:
        return True if type(event) is GroupMessageEvent else False
    return Rule(_is_group_message)


rdhelp = on_startswith(".help", priority=2, block=True)
stcommand = on_startswith(".st", priority=2, block=True)
encommand = on_startswith(".en", priority=2, block=True)
ticommand = on_startswith(".ti", priority=2, block=True)
licommand = on_startswith(".li", priority=2, block=True)
coccommand = on_startswith(".coc", priority=2, block=True)
sccommand = on_startswith(".sc", priority=2, block=True)
rdcommand = on_startswith(".r", priority=4, block=True)
setcommand = on_startswith(".set", priority=5, block=True)
showcommand = on_startswith(".show", priority=5, block=True)
sacommand = on_startswith(".sa", priority=5, block=True)
delcommand = on_startswith(".del", priority=5, block=True)


@rdhelp.handle()
async def rdhelphandler(bot: Bot, event: Event):
    args = str(event.get_message())[5:].strip()
    await rdhelp.finish(help_message(args))


@stcommand.handle()
async def stcommandhandler(bot: Bot):
    await rdhelp.finish(st())


@encommand.handle()
async def enhandler(bot: Bot, event: Event):
    args = str(event.get_message())[3:].strip()
    await encommand.finish(en(args))


@rdcommand.handle()
async def rdcommandhandler(bot: Bot, event: Event):
    args = str(event.get_message())[2:].strip()
    uid = event.get_session_id()
    if args and not("." in args):
        rrd = rd(args)
        if type(rrd) == str:
            await rdcommand.finish(rrd)
        elif type(rrd) == list:
            await bot.send_private_msg(user_id=uid, message=rrd[0])


@coccommand.handle()
async def cochandler(bot: Bot, event: Event):
    args = str(event.get_message())[4:].strip()
    try:
        args = int(args)
    except ValueError:
        args = 20
    inv = Investigator()
    await coccommand.send(inv.age_change(args))
    if 15 <= args < 90:
        cache_cards.update(event, inv.__dict__, save=False)
        await coccommand.finish(inv.output())


@ticommand.handle()
async def ticommandhandler(bot: Bot):
    await ticommand.finish(ti())


@licommand.handle()
async def licommandhandler(bot: Bot):
    await licommand.finish(li())


@sccommand.handle()
async def schandler(bot: Bot, event: Event):
    args = str(event.get_message())[3:].strip().lower()
    await sccommand.finish(sc(args, event=event))


@setcommand.handle()
async def sethandler(bot: Bot, event: Event):
    args = str(event.get_message())[4:].strip().lower()
    await setcommand.finish(set_handler(event, args))


@showcommand.handle()
async def showhandler(bot: Bot, event: Event):
    args = str(event.get_message())[5:].strip().lower()
    for msg in show_handler(event, args):
        await showcommand.send(msg)


@sacommand.handle()
async def sahandler(bot: Bot, event: Event):
    args = str(event.get_message())[3:].strip().lower()
    await sacommand.finish(sa_handler(event, args))


@delcommand.handle()
async def delhandler(bot: Bot, event: Event):
    args = str(event.get_message())[4:].strip().lower()
    for msg in del_handler(event, args):
        await delcommand.send(msg)
