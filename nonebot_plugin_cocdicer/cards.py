from .investigator import Investigator
from .dices import Dices
from nonebot.adapters.cqhttp import Event
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from .messages import help_messages

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

    def load(self) -> None:
        with open(_cachepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def update(self, event: Event, inv_dict: dict, qid: str = "", save: bool = True):
        group_id = get_group_id(event)
        if not self.data.get(group_id):
            self.data[group_id] = {}
        self.data[group_id].update(
            {qid if qid else str(event.sender.user_id): inv_dict})
        if save:
            self.save()

    def get(self, event: Event, qid: str = "") -> dict:
        group_id = get_group_id(event)
        if self.data.get(group_id):
            if self.data[group_id].get(qid if qid else str(event.sender.user_id)):
                return self.data[group_id].get(qid if qid else str(event.sender.user_id))
        else:
            return None

    def delete(self, event: Event, qid: str = "", save: bool = True) -> bool:
        if self.get(event, qid=qid):
            if self.data[get_group_id(event)].get(qid if qid else str(event.sender.user_id)):
                self.data[get_group_id(event)].pop(
                    qid if qid else str(event.sender.user_id))
            if save:
                self.save()
            return True
        return False

    def delete_skill(self, event: Event, skill_name: str, qid: str = "", save: bool = True) -> bool:
        if self.get(event, qid=qid):
            data = self.get(event, qid=qid)
            if data["skills"].get(skill_name):
                data["skills"].pop(skill_name)
                self.update(event, data, qid=qid, save=save)
                return True
        return False


cards = Cards()
cache_cards = Cards()
attrs_dict: dict = {
    "名字": ["name", "名字", "名称"],
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
            cards.update(event, inv_dict=card_data)
            inv = Investigator().load(card_data)
            return "成功从缓存保存人物卡属性：\n" + inv.output()
        else:
            return "未找到缓存数据，请先使用coc指令生成角色"
    else:
        args = args.split(" ")
        if cards.get(event):
            card_data = cards.get(event)
            inv = Investigator().load(card_data)
        else:
            return "未找到已保存数据，请先使用空白set指令保存角色数据"
        if len(args) >= 2:
            for attr, alias in attrs_dict.items():
                if args[0] in alias:
                    if attr == "名字":
                        inv.__dict__[alias[0]] = args[1]
                    else:
                        try:
                            inv.__dict__[alias[0]] = int(args[1])
                        except ValueError:
                            return "请输入正整数属性数据"
                    cards.update(event, inv.__dict__)
                    return "设置调查员%s为：%s" % (attr, args[1])
            try:
                inv.skills[args[0]] = int(args[1])
                cards.update(event, inv.__dict__)
                return "设置调查员%s技能为：%s" % (args[0], args[1])
            except ValueError:
                return "请输入正整数技能数据"


def show_handler(event: Event, args: str):
    r = []
    if not args:
        if cards.get(event):
            card_data = cards.get(event)
            inv = Investigator().load(card_data)
            r.append("使用中人物卡：\n" + inv.output())
        if cache_cards.get(event):
            card_data = cache_cards.get(event)
            inv = Investigator().load(card_data)
            r.append("已暂存人物卡：\n" + inv.output())
    elif args == "s":
        if cards.get(event):
            card_data = cards.get(event)
            inv = Investigator().load(card_data)
            r.append(inv.skills_output())
    elif re.search(r"\[cq:at,qq=\d+\]", args):
        qid = re.search(r"\[cq:at,qq=\d+\]", args).group()[10:-1]
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            inv = Investigator().load(card_data)
            r.append("查询到人物卡：\n" + inv.output())
            if args[0] == "s":
                r.append(inv.skills_output())
    if not r:
        r.append("无保存/暂存信息")
    return r


def del_handler(event: Event, args: str):
    r = []
    args = args.split(" ")
    for arg in args:
        if not arg:
            pass
        elif arg == "c" and cache_cards.get(event):
            if cache_cards.delete(event, save=False):
                r.append("已清空暂存人物卡数据")
        elif arg == "card" and cards.get(event):
            if cards.delete(event):
                r.append("已删除使用中的人物卡！")
        else:
            if cards.delete_skill(event, arg):
                r.append("已删除技能"+arg)
    if not r:
        r.append(help_messages.del_)
    return r


def sa_handler(event: Event, args: str):
    if not args:
        return help_messages.sa
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
