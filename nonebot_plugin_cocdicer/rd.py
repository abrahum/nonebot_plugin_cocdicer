# 参考[OlivaDiceDocs](https://oliva.dicer.wiki/userdoc)实现的nonebot2骰娘插件
import contextlib
import random
from typing import Optional
import diro
from .constant import *


def to_circled(num: int, c: int) -> str:
    if num < 1 or num > 10:
        return "?"
    return str(num) if num < c else chr(0xA2) + chr(0xD8 + num)


def roll_success_level(res: int, rate: int, rule: int = 0) -> int:
    """
    成功等级, 0-大失败，1-失败，2-成功，3-困难成功，4-极难成功，5-大成功

    Args:
        res: 骰子结果
        rate: 检测值
        rule: 规则
    """
    if rule == 0:
        return _roll_success_level_rule0(res, rate)
    elif rule == 1:
        return _roll_success_level_rule1(res, rate)
    elif rule == 2:
        return _roll_success_level_rule2(res, rate)
    elif rule == 3:
        return _roll_success_level_rule3(res, rate)
    elif rule == 4:
        return _roll_success_level_rule4(res, rate)
    elif rule == 5:
        return _roll_success_level_rule5(res, rate)
    elif rule == 6:
        if res > rate:
            return 0 if res == 100 or res % 11 == 0 else 1
        else:
            return 5 if res == 1 or res % 11 == 0 else 2
    else:
        return -1


def _roll_success_level_rule5(res, rate):
    if res >= 99:
        return 0
    if res <= 2 and res < rate / 10:
        return 5
    if res <= rate / 5:
        return 4
    if res <= rate / 2:
        return 3
    if res <= rate:
        return 2
    return 1 if rate >= 50 or res < 96 else 0


def _roll_success_level_rule4(res, rate):
    if res == 100:
        return 0
    if res <= 5 and res <= rate / 10:
        return 5
    if res <= rate / 5:
        return 4
    if res <= rate / 2:
        return 3
    if res <= rate:
        return 2
    return 1 if rate >= 50 or res < 96 + rate / 10 else 0


def _roll_success_level_rule3(res, rate):
    if res >= 96:
        return 0
    if res <= 5:
        return 5
    if res <= rate / 5:
        return 4
    if res <= rate / 2:
        return 3
    return 2 if res <= rate else 1


def _roll_success_level_rule2(res, rate):
    if res == 100:
        return 0
    if res <= 5 and res <= rate:
        return 5
    if res <= rate / 5:
        return 4
    if res <= rate / 2:
        return 3
    if res <= rate:
        return 2
    return 1 if res < 96 else 0


def _roll_success_level_rule1(res, rate):
    if res == 100:
        return 0
    if res == 1 or (res <= 5 and rate >= 50):
        return 5
    if res <= rate / 5:
        return 4
    if res <= rate / 2:
        return 3
    if res <= rate:
        return 2
    return 1 if rate >= 50 or res < 96 else 0


def _roll_success_level_rule0(res, rate):
    if res == 100:
        return 0
    if res == 1:
        return 5
    if res <= rate / 5:
        return 4
    if res <= rate / 2:
        return 3
    if res <= rate:
        return 2
    return 1 if rate >= 50 or res < 96 else 0


def long_insane():
    sym_res = random.randint(1, 10)
    res = f"调查员的疯狂发作-总结症状:1D10={sym_res}\n症状: \n"
    fmap = {"dur" : f"1D10={random.randint(1, 10)}"}
    j = random.randint(1, 100)
    if sym_res == 10:
        fmap["detail_roll"] = f"1D100={j}"
        fmap["detail"] = Panic[j]
    elif sym_res == 9:
        fmap["detail_roll"] = f"1D100={j}"
        fmap["detail"] = Fear[j]
    return f"{res}{LongInsanity[sym_res].format(**fmap)}"


def temp_insane():
    sym_res = random.randint(1, 10)
    res = f"调查员的疯狂发作-临时症状:1D10={sym_res}\n症状: \n"
    fmap = {"dur" : f"1D10={random.randint(1, 10)}"}
    j = random.randint(1, 100)
    if sym_res == 10:
        fmap["detail_roll"] = f"1D100={j}"
        fmap["detail"] = Panic[j]
    elif sym_res == 9:
        fmap["detail_roll"] = f"1D100={j}"
        fmap["detail"] = Fear[j]
    return f"{res}{TempInsanity[sym_res].format(**fmap)}"

def dhr(t, o):
    return 100 if t == 0 and o == 0 else t * 10 + o

def st():
    result = random.randint(1, 20)
    if result < 4:
        rstr = "右腿"
    elif result < 7:
        rstr = "左腿"
    elif result < 11:
        rstr = "腹部"
    elif result < 16:
        rstr = "胸部"
    elif result < 18:
        rstr = "右臂"
    elif result < 20:
        rstr = "左臂"
    else:
        rstr = "头部"
    return f"D20={result}: 命中了{rstr}"


def en(arg: int) -> str:
    check = random.randint(1, 100)
    if check <= arg and check <= 95:
        return f"判定值{check}，判定失败，技能无成长。"
    plus = random.randint(1, 10)
    r = f"判定值1D100={check}，判定成功，技能成长{arg}+{plus}={arg + plus}"
    return r + "\n温馨提示：如果技能提高到90%或更高，增加2D6理智点数。"


def expr(d: diro.Diro, anum: Optional[int], rule: int = 0) -> str:
    d.roll()
    result = d.calc()
    s = f"{d.expr()}={(d.detail_expr())}={result}"
    if anum:
        sl = roll_success_level(result, anum, rule)
        s += f"\n检定值 {anum}, {SuccessLevel[sl]}"
    return s


def rd0(pattern: str, anum: Optional[int] = None, rule: int = 0) -> str:
    d_str = pattern.lower().split("#")
    rd = diro.parse(d_str.pop(0))
    time = 1
    if d_str:
        with contextlib.suppress(ValueError):
            time = int(d_str[0])
    r = expr(rd, anum, rule)
    for _ in range(time - 1):
        r += "\n"
        r += expr(rd, anum)
    return r
