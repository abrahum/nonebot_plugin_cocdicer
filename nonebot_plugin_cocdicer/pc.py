import diro
import math


def coc7(num: int) -> str:
    mans = ""
    _property = ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "幸运"]
    roll = ["3D6", "3D6", "2D6+6", "3D6", "3D6", "2D6+6", "3D6", "2D6+6", "3D6"]
    all_total = 0
    luc = 0
    while num:
        mans += "\n"
        for i in range(8):
            rd_coc = diro.parse(roll[i])
            rd_coc.roll()
            mans += f"{_property[i]}:{rd_coc.calc()*5} "
            all_total += rd_coc.calc() * 5
            luc = rd_coc.calc() * 5
        mans += f"共计:{all_total-luc}/{all_total}"
        all_total = 0
        num -= 1
    return mans[1:]


def coc6d():
    rd3d6 = diro.parse("3d6")
    rd2d6p6 = diro.parse("2d6+6")
    rd3d6p3 = diro.parse("3d6+3")
    rd1d10 = diro.parse("1d10")
    rd3d6.roll()
    mans = f"力量STR=3D6={str(STR := rd3d6.calc())}"
    mans += "\n"

    mans += "体质CON=3D6="
    rd3d6.roll()
    mans += str(CON := rd3d6.calc())
    mans += "\n"

    mans += "体型SIZ=2D6+6="
    rd2d6p6.roll()
    mans += str(SIZ := rd2d6p6.calc())
    mans += "\n"

    mans += "敏捷DEX=3D6="
    rd3d6.roll()
    mans += str(DEX := rd3d6.calc())
    mans += "\n"

    mans += "外貌APP=3D6="
    rd3d6.roll()
    mans += str(APP := rd3d6.calc())
    mans += "\n"

    mans += "智力INT=2D6+6="
    rd2d6p6.roll()
    mans += str(INT := rd2d6p6.calc())
    mans += "\n"

    mans += "意志POW=3D6="
    rd3d6.roll()
    mans += str(POW := rd3d6.calc())
    mans += "\n"

    mans += "教育EDU=3D6+3="
    rd3d6p3.roll()
    mans += str(EDU := rd3d6p3.calc())
    mans += "\n"

    mans += f"共计: {STR + CON + SIZ + APP + POW + EDU + DEX + INT}"
    mans += f"\n理智SAN=POW*5={POW * 5}"
    mans += f"\n灵感IDEA=INT*5={INT*5}"
    mans += f"\n幸运LUCK=POW*5={POW*5}"
    mans += f"\n知识KNOW=EDU*5={EDU*5}"
    mans += f"\n生命值HP=(CON+SIZ)/2={math.ceil((CON + SIZ) / 2)}"
    mans += f"\n魔法值MP=POW={POW}"
    mans += "\n伤害奖励DB="
    if 2 <= STR + SIZ <= 12:
        DB = "-1D6"
    elif 13 <= STR + SIZ <= 16:
        DB = "-1D4"
    elif 17 <= STR + SIZ <= 24:
        DB = "0"
    elif 25 <= STR + SIZ <= 32:
        DB = "1D4"
    elif 33 <= STR + SIZ <= 40:
        DB = "1D6"
    else:
        DB = "计算错误!"
    mans += DB
    mans += "\n"
    mans += "资产=1D10="
    rd1d10.roll()
    mans += str(rd1d10.calc())
    return mans

def coc7d():
    rd3d6 = diro.parse("3d6")
    rd2d6p6 = diro.parse("2d6+6")
    mans = "力量STR=3D6*5="
    rd3d6.roll()
    mans += f"{str(STR := rd3d6.calc() * 5)}/{STR // 2}/{STR // 5}"
    mans += "\n"

    mans += "体质CON=3D6*5="
    rd3d6.roll()
    mans += f"{str(CON := rd3d6.calc() * 5)}/{CON // 2}/{CON // 5}"
    mans += "\n"

    mans += "体型SIZ=(2D6+6)*5="
    rd2d6p6.roll()
    mans += f"{str(SIZ := rd2d6p6.calc() * 5)}/{SIZ // 2}/{SIZ // 5}"
    mans += "\n"

    mans += "敏捷DEX=3D6*5="
    rd3d6.roll()
    mans += f"{str(DEX := rd3d6.calc() * 5)}/{DEX // 2}/{DEX // 5}"
    mans += "\n"

    mans += "外貌APP=3D6*5="
    rd3d6.roll()
    mans += f"{str(APP := rd3d6.calc() * 5)}/{APP // 2}/{APP // 5}"
    mans += "\n"

    mans += "智力INT=(2D6+6)*5="
    rd2d6p6.roll()
    mans += f"{str(INT := rd2d6p6.calc() * 5)}/{INT // 2}/{INT // 5}"
    mans += "\n"

    mans += "意志POW=3D6*5="
    rd3d6.roll()
    mans += f"{str(POW := rd3d6.calc() * 5)}/{POW // 2}/{POW // 5}"
    mans += "\n"

    mans += "教育EDU=(2D6+6)*5="
    rd2d6p6.roll()
    mans += f"{str(EDU := rd2d6p6.calc() * 5)}/{EDU // 2}/{EDU // 5}"
    mans += "\n"

    mans += "幸运LUCK=3D6*5="
    rd3d6.roll()
    mans += f"{str(LUCK := rd3d6.calc() * 5)}/{LUCK // 2}/{LUCK // 5}"
    mans += "\n"

    _sum = STR + CON + SIZ + APP + POW + EDU + DEX + INT
    mans += f"共计:{_sum}/{_sum + LUCK}"

    mans += f"\n理智SAN=POW={POW}"
    mans += f"\n生命值HP=(SIZ+CON)/10={(SIZ + CON) // 10}"
    mans += f"\n魔法值MP=POW/5={POW // 5}"
    if 2 <= STR + SIZ <= 64:
        DB = "-2"
        build = -2
    elif 65 <= STR + SIZ <= 84:
        DB = "-1"
        build = -1
    elif 85 <= STR + SIZ <= 124:
        DB = "0"
        build = 0
    elif 125 <= STR + SIZ <= 164:
        DB = "1D4"
        build = 1
    elif 165 <= STR + SIZ <= 204:
        DB = "1d6"
        build = 2
    else:
        DB = "计算错误!"
        build = -10
    mans += f"\n伤害奖励DB={DB}\n体格={build if build != -10 else '计算错误'}"
    if DEX < SIZ and STR < SIZ:
        MOV = 7
    elif DEX > SIZ and STR > SIZ:
        MOV = 9
    else:
        MOV = 8
    mans += f"\n移动力MOV={MOV}"
    return mans

def dnd(num: int) -> str:
    output = ""
    rd_dnd = diro.parse("4d6k3")
    dnd_name = ["力量", "体质", "敏捷", "智力", "感知", "魅力"]
    add_space = num != 1
    all_total = 0
    while num:
        output += "\n"
        for i in range(6):
            rd_dnd.roll()
            output += f"{dnd_name[i]}:{rd_dnd.calc()} "
            if rd_dnd.calc() < 10 and add_space:
                output += "  "
            all_total += rd_dnd.calc()
        output += f"共计:{all_total}"
        all_total = 0
        num -= 1
    return output[1:]


def coc6(num: int) -> str:
    mans = ""
    _property = ["力量", "体质", "体型", "敏捷", "外貌", "智力", "意志", "教育", "资产"]
    roll = ["3D6", "3D6", "2D6+6", "3D6", "3D6", "2D6+6", "3D6", "3D6+3", "1D10"]
    add_space = num != 1
    all_total = 0
    while num:
        mans += "\n"
        for i in range(8):
            rd_coc = diro.parse(roll[i])
            rd_coc.roll()
            mans += f"{_property[i]}:{rd_coc.calc()} "
            if add_space and rd_coc.calc() < 10:
                mans += "  "
            all_total += rd_coc.calc()
        mans += f"共计:{all_total}"
        all_total = 0
        rd_coc = diro.parse(roll[8])
        rd_coc.roll()
        mans += f" {_property[8]}:{rd_coc.calc()}"
        num -= 1
    return mans[1:]


# class PlayerCard:
#     def __init__(self, name: str = "匿名调查员"):
#         self.name = name
#         self.skills = {}
#         self.age = 20