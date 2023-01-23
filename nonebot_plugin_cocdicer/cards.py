from typing import Dict, List, Optional

import ujson

from .investigator import Investigator
from .constant import help_sc, help_del_, help_sa
from .rd import expr

import diro

from pathlib import Path

attrs_dict: Dict[str, List[str]] = {
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


class Cards:
    def __init__(self, filepath: str) -> None:
        self.path: Path = Path(filepath)
        self.data: Dict[str, Dict[str, dict]] = {}
        self.cache: Dict[str, Dict[str, dict]] = {}

    def save(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            ujson.dump(self.data, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w+", encoding="utf-8") as f:
                self.data = {}
                ujson.dump({}, f, ensure_ascii=False, indent=2)
        else:
            with self.path.open("r", encoding="utf-8") as f:
                self.data = ujson.load(f)

    def update(self, inv_dict: dict, level: str = '0', uid: int = 0, save: bool = True):
        uid = str(uid)
        data = self.data.setdefault(level, {})
        data.update({uid: inv_dict})
        if save:
            self.save()

    def get(self, level: str = '0', uid: int = 0) -> Optional[Dict[str, dict]]:
        return data.get(str(uid)) if (data := self.data.get(level)) else None

    def delete(self, level: str = '0', uid: int = 0, save: bool = True) -> bool:
        if inv := self.get(level, uid):
            inv.clear()
            self.data[level].pop(str(uid), None)
            if not self.data[level]:
                del self.data[level]
            if save:
                self.save()
            return True
        return False

    def delete_skill(self, skill_name: str, level: str = '0', uid: int = 0, save: bool = True) -> bool:
        if (inv := self.get(level, uid)) and inv.get("skills", {}).get(skill_name):
            del inv["skills"][skill_name]
            self.update(inv, level, uid, save=save)
            return True
        return False

    def cache_update(self, inv_dict: dict, level: str = '0', uid: int = 0):
        uid = str(uid)
        data = self.cache.setdefault(level, {})
        data.update({uid: inv_dict})

    def cache_get(self, level: str = '0', uid: int = 0) -> Optional[Dict[str, dict]]:
        return cache.get(str(uid)) if (cache := self.cache.get(level)) else None

    def cache_delete(self, level: str = '0', uid: int = 0) -> bool:
        if inv := self.cache_get(level, uid):
            inv.clear()
            self.cache[level].pop(str(uid), None)
            if not self.cache[level]:
                del self.cache[level]
            return True
        return False

    def cache_delete_skill(self, skill_name: str, level: str = '0', uid: int = 0) -> bool:
        if (inv := self.cache_get(level, uid)) and inv.get("skills", {}).get(skill_name):
            del inv["skills"][skill_name]
            self.cache_update(inv, level, uid)
            return True
        return False

    def set_handler(
        self,
        name: Optional[str] = None,
        num: Optional[str] = None,
        level: str = '0',
        uid: int = 0
    ):
        if not name and not num:
            if card_data := self.cache_get(level, uid):
                self.update(card_data, level, uid)
                inv = Investigator().load(card_data)
                return "成功从缓存保存人物卡属性：\n" + inv.output()
            return "未找到缓存数据，请先使用wcoc指令生成角色"
        else:
            if card_data := self.get(level, uid):
                inv = Investigator().load(card_data)
            else:
                return "未找到已保存数据，请先使用空白set指令保存角色数据"
            if not name or not num:
                return "缺少角色数据或者属性"
            for attr, alias in attrs_dict.items():
                if name in alias:
                    if attr == "名字":
                        inv.dump()[alias[0]] = num
                    elif num.isdigit():
                        inv.dump()[alias[0]] = int(num)
                    else:
                        return "请输入正整数属性数据"
                    self.update(inv.dump(), level, uid)
                    return f"设置调查员{attr}为：{num}"
            if num.isdigit():
                inv.skills[name] = int(num)
                self.update(inv.dump(), level, uid)
                return f"设置调查员{name}技能为：{num}"
            return "请输入正整数技能数据"

    def show_handler(self, level: str = "0", uid: int = 0):
        r = []
        if card_data := self.get(level, uid):
            inv = Investigator().load(card_data)
            r.append("查询到人物卡：\n" + inv.output())
        if card_cache := self.cache_get(level, uid):
            inv = Investigator().load(card_cache)
            r.append("已暂存人物卡：\n" + inv.output())
        if not r:
            r.append("无保存/暂存信息")
        return r

    def show_skill_handler(self, level: str = "0", uid: int = 0):
        if card_data := self.get(level, uid):
            return Investigator().load(card_data).skills_output()
        return "无保存/暂存信息"

    def del_handler(self, args: List[str], level: str = "0", uid: int = 0):
        r = []
        for arg in args:
            if not arg:
                continue
            if arg == "c" and self.cache_get(level, uid):
                if self.cache_delete(level, uid):
                    r.append("已清空暂存人物卡数据")
            elif arg == "card" and self.get(level, uid):
                if self.delete(level, uid):
                    r.append("已删除使用中的人物卡！")
            elif self.delete_skill(arg, level, uid):
                r.append(f"已删除技能{arg}")
        if not r:
            r.append(help_del_)
        return r

    def ra_handler(self, args: str, exp: int = -1, level: str = "0", uid: int = 0):
        if not args:
            return help_sa
        if card_data := self.get(level, uid):
            for attr, alias in attrs_dict.items():
                if args in alias:
                    arg = alias[0]
                    value = card_data[arg]
                    break
            else:
                inv = Investigator().load(card_data)
                if inv.skills.get(args):
                    value = inv.skills[args]
                elif exp < 0:
                    return "请输入正确的别名，或传入检定值"
                else:
                    value = exp
        elif exp < 0:
            return "请先使用set指令保存人物卡后使用快速检定功能，或传入检定值"
        else:
            value = exp
        dices = diro.parse("1D100")
        return f"{args}检定:\n{expr(dices, value)}" if isinstance(value, int) else "请输入正确的别名，或传入检定值"

    def sc_handler(self, sf: str, san: Optional[int] = None, level: str = "0", uid: int = 0) -> str:
        try:
            s_and_f = sf.split("/")
            success = diro.parse(s_and_f[0])
            success.roll()
            success = success.calc()
            failure = diro.parse(s_and_f[1])
            failure.roll()
            failure = failure.calc()
            if san:
                card = {"san": san, "name": "该调查员"}
                using_card = False
            else:
                card = self.get(level, uid)
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
                self.update(card, level, uid)
            return s
        except (IndexError, KeyError):
            return help_sc
