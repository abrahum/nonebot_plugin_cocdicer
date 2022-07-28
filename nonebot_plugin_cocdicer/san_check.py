from .messages import help_messages
from .cards import cards
from .util import MessageEvent

import diro


def sc(arg: str, event: MessageEvent) -> str:
    try:
        args = arg.split(" ")
        using_card = False
        s_and_f = args[0].split("/")
        success = diro.parse(s_and_f[0])
        success.roll()
        success = success.calc()
        failure = diro.parse(s_and_f[1])
        failure.roll()
        failure = failure.calc()
        if len(args) > 1:
            card = {"san": int(args[1]), "name": "该调查员"}
            using_card = False
        else:
            card = cards.get(event)
            using_card = True
        r = diro.Dice().roll()()
        s = f"San Check:{r}"
        down = success if r <= card["san"] else failure
        s += f"理智降低了{down}点"
        if down >= card["san"]:
            s += "\n%s陷入了永久性疯狂" % card["name"]
        elif down >= (card["san"] // 5):
            s += "\n%s陷入了不定性疯狂" % card["name"]
        elif down >= 5:
            s += "\n%s陷入了临时性疯狂" % card["name"]
        if using_card:
            card["san"] -= down
            cards.update(event, card)
        return s
    except:
        return help_messages.sc
