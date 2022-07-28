import nonebot

if nonebot.get_driver()._adapters.get("OneBot V12"):
    from nonebot.adapters.onebot.v12 import Bot, MessageEvent, GroupMessageEvent
else:
    from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
