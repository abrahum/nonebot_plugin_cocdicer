import nonebot

if nonebot.get_driver()._adapters.get("OneBot V12"):
    from nonebot.adapters.onebot.v12 import (  # noqa
        Bot as Bot,
        MessageEvent as MessageEvent,
        GroupMessageEvent as GroupMessageEvent
    )
else:
    from nonebot.adapters.onebot.v11 import (  # noqa
        Bot as Bot,
        MessageEvent as MessageEvent,
        GroupMessageEvent as GroupMessageEvent
    )
