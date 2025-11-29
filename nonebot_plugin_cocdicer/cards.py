from typing import Dict, List, Optional
from .investigator import Investigator
from .util import MessageEvent, GroupMessageEvent
from .messages import help_messages
from .dices import expr
from pydantic import BaseModel
from nonebot import require

import re
import diro

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as localstore  # noqa: E402

# localstore.get_plugin_data_dir() / "cards.json" = localstore.get_plugin_data_dir() / "cards.json"


def get_group_id(event: MessageEvent):
    if type(event) is GroupMessageEvent:
        return str(event.group_id)
    else:
        return "0"


class Cards(BaseModel):
    data: Dict[str, Dict[str, Investigator]] = {}  # group_id: {user_id: investigator}

    def __init__(self, **data) -> None:
        super().__init__(**data)

    def save(self) -> None:
        with open(
            localstore.get_plugin_data_dir() / "cards.json", "w", encoding="utf-8"
        ) as f:
            f.write(self.model_dump_json(ensure_ascii=False, by_alias=True))

    def load(self) -> None:
        with open(
            localstore.get_plugin_data_dir() / "cards.json", "r", encoding="utf-8"
        ) as f:
            readed = Cards.model_validate_json(f.read())
            self.data = readed.data

    def update(
        self, event: MessageEvent, inv: Investigator, qid: str = "", save: bool = True
    ):
        group_id = get_group_id(event)
        if not self.data.get(group_id):
            self.data[group_id] = {}
        self.data[group_id].update({qid if qid else str(event.sender.user_id): inv})
        if save:
            self.save()

    def get_by_event(
        self, event: MessageEvent, qid: str = ""
    ) -> Optional[Investigator]:
        group_id = get_group_id(event)
        if self.data.get(group_id):
            if self.data[group_id].get(qid if qid else str(event.sender.user_id)):
                return self.data[group_id].get(
                    qid if qid else str(event.sender.user_id)
                )
        else:
            return None

    def delete(self, event: MessageEvent, qid: str = "", save: bool = True) -> bool:
        if self.get_by_event(event, qid=qid):
            if self.data[get_group_id(event)].get(
                qid if qid else str(event.sender.user_id)
            ):
                self.data[get_group_id(event)].pop(
                    qid if qid else str(event.sender.user_id)
                )
            if save:
                self.save()
            return True
        return False

    def delete_skill(
        self, event: MessageEvent, skill_name: str, qid: str = "", save: bool = True
    ) -> bool:
        if self.get_by_event(event, qid=qid):
            inv = self.get_by_event(event, qid=qid)
            if inv and inv.skills.get(skill_name):
                inv.skills.pop(skill_name)
                self.update(event, inv, qid=qid, save=save)
                return True
        return False


cards = Cards()
cache_cards = Cards()
attrs_dict: Dict[str, List[str]] = {
    "名字": ["name", "名字", "名称"],
    "年龄": ["age", "年龄"],
    "力量": ["str_field", "str", "力量"],
    "体质": ["con", "体质"],
    "体型": ["siz", "体型"],
    "敏捷": ["dex", "敏捷"],
    "外貌": ["app", "外貌"],
    "智力": ["int_field", "int", "智力", "灵感"],
    "意志": ["pow", "意志"],
    "教育": ["edu", "教育"],
    "幸运": ["luc", "幸运"],
    "理智": ["san", "理智"],
}


def set_handler(event: MessageEvent, arg: str):
    if not arg:
        if cache_cards.get_by_event(event):
            inv = cache_cards.get_by_event(event)
            if inv:
                cards.update(event, inv=inv)
                return "成功从缓存保存人物卡属性：\n" + inv.output()
        else:
            return "未找到缓存数据，请先使用coc指令生成角色"
    else:
        args = arg.split(" ")
        if cards.get_by_event(event):
            inv = cards.get_by_event(event)
        else:
            return "未找到已保存数据，请先使用空白set指令保存角色数据"
        if len(args) >= 2:
            for attr, alias in attrs_dict.items():
                if args[0] in alias and inv:
                    if attr == "名字":
                        inv.__dict__[alias[0]] = args[1]
                    else:
                        try:
                            inv.__dict__[alias[0]] = int(args[1])
                        except ValueError:
                            return "请输入正整数属性数据"
                    # cards.update(event, inv=inv)
                    return "设置调查员%s为：%s" % (attr, args[1])
            try:
                if inv:
                    inv.skills[args[0]] = int(args[1])
                    # cards.update(event, inv)
                    return "设置调查员%s技能为：%s" % (args[0], args[1])
            except ValueError:
                return "请输入正整数技能数据"


def show_handler(event: MessageEvent, args: str):
    r = []
    if not args:
        if cards.get_by_event(event):
            inv = cards.get_by_event(event)
            if inv:
                r.append("使用中人物卡：\n" + inv.output())
        if cache_cards.get_by_event(event):
            inv = cache_cards.get_by_event(event)
            if inv:
                r.append("已暂存人物卡：\n" + inv.output())
    elif args == "s":
        if cards.get_by_event(event):
            inv = cards.get_by_event(event)
            if inv:
                r.append(inv.skills_output())
    elif re.search(r"\[cq:at,qq=\d+\]", args):
        search_result = re.search(r"\[cq:at,qq=\d+\]", args)
        if search_result:
            qid = search_result.group()[10:-1]
            if cards.get_by_event(event, qid=qid):
                inv = cards.get_by_event(event, qid=qid)
                if inv:
                    r.append("查询到人物卡：\n" + inv.output())
                    if args[0] == "s":
                        r.append(inv.skills_output())
    if not r:
        r.append("无保存/暂存信息")
    return r


def del_handler(event: MessageEvent, arg: str):
    r = []
    args = arg.split(" ")
    for arg in args:
        if not arg:
            pass
        elif arg == "c" and cache_cards.get_by_event(event):
            if cache_cards.delete(event, save=False):
                r.append("已清空暂存人物卡数据")
        elif arg == "card" and cards.get_by_event(event):
            if cards.delete(event):
                r.append("已删除使用中的人物卡！")
        else:
            if cards.delete_skill(event, arg):
                r.append("已删除技能" + arg)
            else:
                r.append("未找到人物卡或技能" + arg)
    if not r:
        r.append(help_messages.del_)
    return r


def sa_handler(event: MessageEvent, arg: str) -> str:
    if not arg:
        return help_messages.sa
    elif not cards.get_by_event(event):
        return "请先使用set指令保存人物卡后再使用快速检定功能。"
    for _, alias in attrs_dict.items():
        if arg in alias:
            arg = alias[0]
            card_data = cards.get_by_event(event)
            dices = diro.parse("")
            return expr(dices, card_data.__dict__[arg])
    return "未找到属性%s，请检查输入是否正确。" % arg
