import json
import random
# import pandas as pd
# import numpy as np
from base.base import BaseFunc

"""
出蓝的概率是79.91%
出紫的概率是15.98%
开出粉色的概率大概是3.2%
开出红色的概率大概是0.65%
开出金的概率大概是0.26%
"""


class Csgo(BaseFunc):
    def rand_weapon_from_json(self, case_name):
        # self.excel_to_json()
        with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\case.json', encoding='utf-8') as a:
            result = json.load(a)
            is_find = False
            for j in range(len(result)):
                case_name_res = result[j]['case_name']
                if case_name_res == case_name:
                    contains = result[j]['contains']
                    is_find = True
                else:
                    pass
            if not is_find:
                jsons = {'weapon_name': '输入名称有误！'}
                return jsons
            blue_list = []
            purple_list = []
            pink_list = []
            red_list = []
            gold_list = []

            for i in range(len(contains)):
                type = contains[i]['type']
                if type == 'blue':
                    blue_list.append(contains[i])
                elif type == 'purple':
                    purple_list.append(contains[i])
                elif type == 'pink':
                    pink_list.append(contains[i])
                elif type == 'red':
                    red_list.append(contains[i])
                elif type == 'gold':
                    gold_list.append(contains[i])
                else:
                    pass
            a.close()
            # print('列表创建完毕')
            rand_percent = random.random()
            weapon_content = {}
            # 军规（蓝）
            if rand_percent <= 0.7991:
                randint = random.randint(0, len(blue_list) - 1)
                weapon_content['weapon_name'] = blue_list[randint]['name']
                lowest_price = blue_list[randint]['lowest_price']
                highest_price = blue_list[randint]['highest_price']
                weapon_content['weapon_price'] = round(random.uniform(lowest_price, highest_price), 2)
                weapon_content['weapon_type'] = '蓝'
                weapon_content['pic_url'] = blue_list[randint]['pic_url']
            # 受限（紫）
            elif 0.7991 < rand_percent <= 0.9589:
                randint = random.randint(0, len(purple_list) - 1)
                weapon_content['weapon_name'] = purple_list[randint]['name']
                lowest_price = purple_list[randint]['lowest_price']
                highest_price = purple_list[randint]['highest_price']
                weapon_content['weapon_price'] = round(random.uniform(lowest_price, highest_price), 2)
                weapon_content['weapon_type'] = '紫'
                weapon_content['pic_url'] = purple_list[randint]['pic_url']
            # 保密（粉）
            elif 0.9589 < rand_percent <= 0.9909:
                randint = random.randint(0, len(pink_list) - 1)
                weapon_content['weapon_name'] = pink_list[randint]['name']
                lowest_price = pink_list[randint]['lowest_price']
                highest_price = pink_list[randint]['highest_price']
                weapon_content['weapon_price'] = round(random.uniform(lowest_price, highest_price), 2)
                weapon_content['weapon_type'] = '粉'
                weapon_content['pic_url'] = pink_list[randint]['pic_url']
            # 隐秘（红）
            elif 0.9909 < rand_percent <= 0.9974:
                randint = random.randint(0, len(red_list) - 1)
                weapon_content['weapon_name'] = red_list[randint]['name']
                lowest_price = red_list[randint]['lowest_price']
                highest_price = red_list[randint]['highest_price']
                weapon_content['weapon_price'] = round(random.uniform(lowest_price, highest_price), 2)
                weapon_content['weapon_type'] = '红'
                weapon_content['pic_url'] = red_list[randint]['pic_url']
            # 金
            else:
                randint = random.randint(0, len(gold_list) - 1)
                weapon_content['weapon_name'] = gold_list[randint]['name']
                lowest_price = gold_list[randint]['lowest_price']
                highest_price = gold_list[randint]['highest_price']
                weapon_content['weapon_price'] = round(random.uniform(lowest_price, highest_price), 2)
                weapon_content['weapon_type'] = '金'
                weapon_content['pic_url'] = gold_list[randint]['pic_url']
            # print(weapon_content)
            return weapon_content

    def open_case_fron_json(self, case_count, case_name):
        lists = []
        price = 0.00
        pic_url = []
        # case_count = int(case_count)
        for i in range(0, case_count):
            # print(f'正在开第{i+1}')
            weapon_content = self.rand_weapon_from_json(case_name)
            if weapon_content['weapon_name'] == '输入名称有误！':
                return weapon_content['weapon_name']
            # print(weapon_content)

            weapon_price = weapon_content['weapon_price']
            price = round(price + weapon_price, 2)
            # print('有价格了')
            weapon_content.pop('weapon_price')
            weapon_content.pop('pic_url')
            lists.append(weapon_content)

        nl = []
        tl = [str(r) for r in lists]
        for record in set(tl):
            n = eval(record)
            n.update({"rqs": tl.count(record)})
            nl.append(n)
        cost = 16 * case_count
        diff = round(price - cost, 2)
        msg = '抽到了：\n'
        for i in range(len(nl)):
            if nl[i]['weapon_type'] != '金':
                msg = msg + f'{nl[i]["rqs"]} × 【{nl[i]["weapon_type"]}】：“{nl[i]["weapon_name"]}”\n'
            else:
                msg = msg + f'哇哦，金色传说！！恭喜你，开到了一件极其罕见的物品“{nl[i]["weapon_name"]}”！！\n'
        if diff >= 0:
            msg = msg + f'此次您共花费了{cost}元，所开出的武器价值估算为{price}元，共盈利{diff}元'
        else:
            msg = msg + f'此次您共花费了{cost}元，所开出的武器价值估算为{price}元，共亏损{abs(diff)}元'
        print(msg)
        # print(pic_url)
        return msg, diff

    # def excel_to_json(self):
    #     data = pd.read_excel('./case_data.xls', sheet_name='Sheet1')
    #     json_list = []
    #     for case_name in data['case_name'].unique():
    #         case_dict = {'case_name': case_name, 'contains': []}
    #         case_data = data[data['case_name'] == case_name]
    #
    #         for kind in case_data['name'].unique():
    #             info = {'name': kind}
    #             kind_data = case_data[case_data['name'] == kind]
    #
    #             for type in kind_data['type'].unique():
    #                 info['type'] = type
    #
    #             for low in kind_data['lowest_price'].unique():
    #                 info['lowest_price'] = low
    #
    #             for high in kind_data['highest_price'].unique():
    #                 info['highest_price'] = high
    #             case_dict['contains'].append(info)
    #         json_list.append(case_dict)
    #
    #     print(json_list)
    #     data_dict = json.dumps(json_list, ensure_ascii=False)
    #     with open('case.json', 'w', encoding='utf-8') as f_w:
    #         f_w.write(data_dict)

    def open_cases(self, from_wxid, case_count, case_name):
        try:
            with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', encoding='utf-8') as ml:
                res = json.load(ml)
                ml.close()
                for i in range(len(res)):
                    # 读取user的money
                    if from_wxid == res[i]['from_wxid']:
                        money = res[i]['money']
                        print(f'user_money:{money}')
                        case_money = case_count * 16
                        # 钱够了
                        if money >= case_money:
                            msg_1, diff = self.open_case_fron_json(case_count, case_name)
                            remaining_money = round(money + diff, 2)
                            remaining_case = int(remaining_money / 16)
                            msg_2 = f'您账户余额为：{remaining_money}元，还能开{remaining_case}个箱子'
                            msg = f'{msg_1}\n{msg_2}'
                            res[i]['money'] = remaining_money
                            with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', 'w', encoding='utf-8') as f_w:
                                result = json.dumps(res, ensure_ascii=False)
                                f_w.write(result)
                                f_w.close()
                            return msg
                        # 钱不够
                        else:
                            msg = f'您账户余额为{money}元。\n余额不足，请明天再试。'
                            return msg
            ml.close()
        except Exception as e:
            print(e)

    def check_balance(self, from_wxid):
        with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', encoding='utf-8') as ml:
            res = json.load(ml)
            for i in range(len(res)):
                # 读取user的money
                if from_wxid == res[i]['from_wxid']:
                    money = res[i]['money']
                    return money

    def add_all_money(self):
        with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', encoding='utf-8') as ml:
            res = json.load(ml)
            ml.close()
            for i in range(len(res)):
                money = res[i]['money']
                if money <= 16000:
                    res[i]['money'] = money + 5000
                else:
                    res[i]['money'] = money + 1000
        with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', 'w', encoding='utf-8') as f_w:
            result = json.dumps(res, ensure_ascii=False)
            f_w.write(result)
            f_w.close()

    def print_user_money(self, wechat, room_wxid):
        data = wechat.get_room_members(room_wxid)
        member_list = data['member_list']
        print(member_list)
        msg = '所有成员余额如下：\n'
        for i in range(len(member_list)):
            nick_name = member_list[i]['nickname']
            wxid = member_list[i]['wxid']
            print(nick_name + ' ' + wxid)
            with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', encoding='utf-8') as ml:
                res = json.load(ml)
                for j in range(len(res)):
                    user_wxid = res[j]['from_wxid']
                    user_money = res[j]['money']
                    if wxid == user_wxid:
                        msg = msg + f'{nick_name}：{user_money}元\n'
        return msg

    def add_money(self, add_money):
        try:
            with open(r'C:\py\git\PythonProject\ntchat_wechat\csgo\user_money.json', 'w+', encoding='utf-8') as ml:
                res = json.load(ml)
                print(add_money)
                for i in range(len(res)):
                    if res[i]['from_wxid'] == self.ckd_id:
                        money = [res][i]['money']
                        res[i][money] = money + int(add_money)
                ml.write(res)
        except Exception as e:
            print(e)