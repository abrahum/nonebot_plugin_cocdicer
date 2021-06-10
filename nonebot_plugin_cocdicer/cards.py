from .investigator import Investigator
from .dices import Dices
from nonebot.adapters.cqhttp import Event
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from .messages import sa_help_message

import ujson as json

import os
import re
_cachepath = os.path.join("data", "coc_cards.json")


def get_group_id(event: Event):
    if type(event) is GroupMessageEvent:
        return str(event.group_id)
    else:
        return "0"


class Cards():
    def __init__(self) -> None:
        self.data: dict = {}

    def save(self) -> None:
        with open(_cachepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)

    def update(self) -> None:
        with open(_cachepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def update_cards(self, event: Event, inv_dict: dict):
        group_id = get_group_id(event)
        if not self.data.get(group_id):
            self.data[group_id] = {}
        self.data[group_id].update({str(event.sender.user_id): inv_dict})
        self.save()

    def get(self, event: Event, qid: str = "") -> dict:
        group_id = get_group_id(event)
        if self.data.get(group_id):
            if self.data[group_id].get(qid if qid else str(event.sender.user_id)):
                return self.data[group_id].get(qid if qid else str(event.sender.user_id))
        else:
            return None

    def delete(self, event: Event):
        if self.get(event):
            self.data[get_group_id(event)] = {}


cards = Cards()
cache_cards = Cards()
attrs_dict: dict = {
    "名字": ["name", "名字"],
    "年龄": ["age", "年龄"],
    "力量": ["str", "力量"],
    "体质": ["con", "体质"],
    "体型": ["siz", "体型"],
    "敏捷": ["dex", "敏捷"],
    "外貌": ["app", "外貌"],
    "智力": ["int", "智力", "灵感"],
    "意志": ["pow", "意志"],
    "教育": ["edu", "教育"],
    "幸运": ["luc", "幸运"],
    "理智": ["san", "理智"],
}


def set_handler(event: Event, args: str):
    if not args:
        if cache_cards.get(event):
            card_data = cache_cards.get(event)
            cards.update_cards(event, inv_dict=card_data)
            inv = Investigator().load(card_data)
            return "成功从缓存保存人物卡属性：\n" + inv.output()
        else:
            return "未找到缓存数据，请先使用coc指令生成角色。"
    else:
        args = args.split(" ")
        if cards.get(event):
            card_data = cards.get(event)
            inv = Investigator().load(card_data)
        else:
            return "未找到已保存数据，请先使用空白set指令保存角色数据。"
        if len(args) >= 2:
            for attr, alias in attrs_dict.items():
                if args[0] in alias:
                    if attr == "名字":
                        inv.__dict__[alias[0]] = args[1]
                    else:
                        try:
                            inv.__dict__[alias[0]] = int(args[1])
                        except ValueError:
                            return "请输入正整数属性数据。"
                    cards.update_cards(event, inv.__dict__)
                    return "设置调查员%s为：%s" % (attr, args[1])


def show_handler(event: Event, args: str):
    r = []
    if not args:
        if cards.get(event):
            card_data = cards.get(event)
            inv = Investigator().load(card_data)
            r.append("已保存人物卡：\n" + inv.output())
        if cache_cards.get(event):
            card_data = cache_cards.get(event)
            inv = Investigator().load(card_data)
            r.append("已暂存人物卡：\n" + inv.output())
    elif re.search(r"\[CQ:at,qq=\d+\]", args):
        qid = re.search(r"\[CQ:at,qq=\d+\]", args).group()[10:-1]
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            inv = Investigator().load(card_data)
            r.append("查询到人物卡：\n" + inv.output())
    if not r:
        r.append("无保存/暂存信息。")
    return r


def sa_handler(event: Event, args: str):
    if not args:
        return sa_help_message
    elif not cards.get(event):
        return "请先使用set指令保存人物卡后再使用快速检定功能。"
    for attr, alias in attrs_dict.items():
        if args in alias:
            arg = alias[0]
            break
    card_data = cards.get(event)
    dices = Dices()
    dices.a = True
    dices.anum = card_data[arg]
    return dices.roll()
