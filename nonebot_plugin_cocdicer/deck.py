from __future__ import annotations

import json
import random
from pathlib import Path

import diro

root = Path(__file__).parent / "assets"

with (root / "public_deck.json").open("r", encoding="utf-8") as f:
    p_deck: dict[str, list[str]] = json.load(f)


def find_deck(name: str) -> int:
    if name in p_deck:
        return 1
    return 2 if (name[0].isdigit() and len(name) < 3) or name == "100" else 0


def draw(key: str, cnt: int = 1) -> str:
    if not key:
        return ""  # TODO: draw_help
    if not find_deck(key):
        return f"未找到卡组{key}"
    pro = p_deck[key][:]
    res = []
    while cnt:
        res.append(draw_card(pro))
        if not pro:
            break
        cnt -= 1
    return "|".join(res)


def draw_expr(exp: str) -> str:
    tmp_list: dict[str, list[str]] = {}
    cnt = 0
    while (lq := exp.find("{", cnt)) > -1 and (rq := exp.find("}", lq)) > -1:
        if lq and exp[lq - 1] == "\\":
            exp = exp[: lq - 1]
            cnt = rq
            continue
        tmp = exp[lq + 1 : rq]
        if tmp not in p_deck:
            cnt = rq + 1
            continue
        if tmp not in tmp_list:
            res = draw_card(p_deck[tmp], True)
        else:
            if not tmp_list[tmp]:
                tmp_list[tmp] = p_deck[tmp][:]
            res = draw_card(tmp_list[tmp])
        exp = f"{exp[:lq]}{res}{exp[rq+1:]}"
        cnt = lq + len(res)
    cnt = 0
    while (lq := exp.find("[", cnt)) > -1 and (rq := exp.find("]", lq)) > -1:
        if lq and exp[lq - 1] == "\\":
            exp = exp[: lq - 1]
            cnt = rq
            continue
        roll = exp[lq + 1 : rq]
        cnt = rq + 1
        try:
            rd = diro.parse(roll)
        except ValueError:
            continue
        rd.roll()
        exp = f"{exp[:lq]}{rd.calc()}{exp[rq+1:]}"
        cnt = lq + len(str(rd.calc()))
    return exp


def draw_card(tmp: list[str], is_back: bool = False) -> str:
    parsed = tmp[:]
    if not tmp:
        return ""
    if len(tmp) == 1:
        reply = parsed[0]
        if not is_back:
            tmp.pop(0)
    else:
        index = random.randint(0, len(tmp) - 1)
        reply = parsed[index]
        if not is_back:
            tmp.pop(index)
    return draw_expr(reply)
