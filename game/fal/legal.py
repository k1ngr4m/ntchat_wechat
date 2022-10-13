from cardtype import *


def legal(cards1, cards2):
    type1, number1 = cardtype(cards1)
    type2, number2 = cardtype(cards2)
    if type2 == "rocket":  # 火箭
        return True
    if type2 == "bomb":
        if type1 == "bomb":
            if number2[0] > number1[0]:
                return True
            else:
                return False
        else:
            return True
    if type1 == "single":  # 单牌
        if type2 == "single":
            if number2 > number1:
                return True
            else:
                return False
        else:
            return False
    if type1 == "pair":  # 对子    if type2 == "pair":
        if number2[0] > number1[0]:
            return True
        else:
            return False
    # else:
    #     return False
    if type1 == "3+1":  # 三带一
        if type2 == "3+1":
            if number2[0] > number1[0]:
                return True
            else:
                return False
        else:
            return False
    if type1 == "4+2":  # 4带2
        if type2 == "4+2":
            if number2[0] > number1[0]:
                return True
            else:
                return False
        else:
            return False
    if type1 == "straight":  # 顺子
        if type2 == "straight":
            if number2[1] == number1[1]:
                if number2[0] > number1[0]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False