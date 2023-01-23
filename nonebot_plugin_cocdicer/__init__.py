from __future__ import annotations

from nonebot import get_bot, get_driver
from nonebot.adapters import Bot as Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v12 import Bot as V12Bot
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith
from nonebot.rule import Rule

from .cards import Cards
from .constant import help_main, helps
from .deck import draw
from .investigator import Investigator
from .pc import coc6, coc6d, coc7, coc7d, dnd
from .rd import dhr, en, expr, long_insane, rd0, roll_success_level, st, temp_insane
from .util import GroupMessageEvent, MessageEvent

driver = get_driver()
coc_cards = Cards("data/coc_cards.json")


@driver.on_startup
async def _():  # 角色卡暂存目录初始化
    coc_cards.load()


@driver.on_shutdown
async def _():
    coc_cards.save()


def is_group_message() -> Rule:
    async def _is_group_message(bot: Bot, event: MessageEvent) -> bool:
        return type(event) is GroupMessageEvent

    return Rule(_is_group_message)


def get_level_uid(event: MessageEvent) -> tuple[str, int]:
    return (
        str(event.group_id) if isinstance(event, GroupMessageEvent) else "0",
        event.sender.user_id or 0,
    )


rdhelp = on_startswith(".help", priority=2, block=True)
drawcommand = on_startswith(".draw", priority=2, block=True)
stcommand = on_startswith(".st", priority=2, block=True)
encommand = on_startswith(".en", priority=2, block=True)
ticommand = on_startswith(".ti", priority=2, block=True)
licommand = on_startswith(".li", priority=2, block=True)
dndcommand = on_startswith(".dnd", priority=2, block=True)
coccommand = on_startswith(".coc", priority=2, block=True)
wcoccommand = on_startswith(".wcoc", priority=2, block=True)
sccommand = on_startswith(".sc", priority=2, block=True)
racommand = on_startswith(".ra", priority=5, block=True)
rhcommand = on_startswith(".rh", priority=3, block=True)
rdcommand = on_startswith(".r", priority=4, block=True)
setcommand = on_startswith(".set", priority=5, block=True)
showcommand = on_startswith(".show", priority=5, block=True)
delcommand = on_startswith(".del", priority=5, block=True)


@rdhelp.handle()
async def rdhelphandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip()
    await matcher.finish(helps.get(args, help_main))


@stcommand.handle()
async def stcommandhandler(matcher: Matcher):
    await matcher.finish(st())


@encommand.handle()
async def enhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip()
    await matcher.finish(en(int(args)))


@drawcommand.handle()
async def drawhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip().split(" ")
    key = args.pop(0) if args else ""
    cnt = int(args[0]) if args and args[0].isdigit() else None
    await matcher.finish(draw(key, cnt))


@racommand.handle()
async def rahandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip().lower().split(" ")
    level, uid = get_level_uid(event)
    name = args.pop(0) if args else ""
    exp = int(args[0]) if args and args[0].isdigit() else -1
    await matcher.finish(coc_cards.ra_handler(name, exp, level, uid))


@rhcommand.handle()
async def rhcommandhandler(bot: Bot, event: GroupMessageEvent):
    args = str(event.get_message())[3:].strip()
    uid = event.get_user_id()
    if args and "." not in args:
        print("get here")
        _args = args.lower().split(" ")
        pat = _args.pop(0)
        anum = int(_args[0]) if _args else None
        if isinstance(bot, V12Bot):
            from nonebot.adapters.onebot.v12 import MessageSegment

            await bot.send_message(
                detail_type="private",
                user_id=uid,
                message=[MessageSegment.text(rd0(pat, anum))],
            )
        elif isinstance(bot, V11Bot):
            await bot.send_private_msg(user_id=uid, message=rd0(pat, anum))


@rdcommand.handle()
async def rdcommandhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[2:].strip()
    if args and "." not in args:
        _args = args.lower().split(" ")
        pat = _args.pop(0)
        anum = int(_args[0]) if _args else None
        await matcher.finish(rd0(pat, anum))


@dndcommand.handle()
async def dndhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip()
    val = int(args) if args else 1
    await matcher.finish(dnd(val))


@coccommand.handle()
async def cochandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().split(" ")
    pat = args.pop(0)
    val = int(args[0]) if args else 1
    if pat.endswith("d"):
        if pat.startswith("6"):
            await matcher.finish(coc6d())
        else:
            await matcher.finish(coc7d())
    elif pat.startswith("6"):
        await matcher.finish(coc6(val))
    else:
        await matcher.finish(coc7(val))


@wcoccommand.handle()
async def wcochandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip()
    try:
        args = int(args)
    except ValueError:
        args = 20
    inv = Investigator()
    await matcher.send(inv.age_change(args))
    if 15 <= args < 90:
        level, uid = get_level_uid(event)
        coc_cards.cache_update(inv.dump(), level, uid)
        await matcher.finish(inv.output())


@ticommand.handle()
async def ticommandhandler(
    matcher: Matcher,
):
    await matcher.finish(temp_insane())


@licommand.handle()
async def licommandhandler(
    matcher: Matcher,
):
    await matcher.finish(long_insane())


@sccommand.handle()
async def schandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip().lower().split(" ")
    level, uid = get_level_uid(event)
    sf = args.pop(0)
    san = int(args[0]) if args else None
    await matcher.finish(coc_cards.sc_handler(sf, san, level, uid))


@setcommand.handle()
async def sethandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().lower().split(" ")
    level, uid = get_level_uid(event)
    name = args.pop(0) if args else None
    num = args[0] if args and args[0].isdigit() else None
    await matcher.finish(coc_cards.set_handler(name, num, level, uid))


@showcommand.handle()
async def showhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip().lower()
    level, uid = get_level_uid(event)
    if args.startswith("s"):
        await matcher.finish(coc_cards.show_skill_handler(level, uid))
    else:
        for msg in coc_cards.show_handler(level, uid):
            await matcher.send(msg)


@delcommand.handle()
async def delhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().lower().split(" ")
    level, uid = get_level_uid(event)
    for msg in coc_cards.del_handler(args, level, uid):
        await matcher.send(msg)
