import json

import requests
import os

from base.base import BaseFunc


class EmotionalAnalysis:
    def __init__(self):
        self.token = 'ftfllnjrlgd5d7tasnu2i1lr9hp7iuij'

    def emotional_analysis(self, wechat, from_wxid, msg):
        api_data = self.get_apidata(msg)
        self.save_data(wechat, from_wxid, api_data)

    def get_apidata(self, text):
        try:
            url = 'https://eolink.o.apispace.com/wbqgfx/api/v1/forward/sentiment_anls'
            headers = {
                "X-APISpace-Token": "ftfllnjrlgd5d7tasnu2i1lr9hp7iuij",
                "Authorization-Type": "apikey"
            }
            payload = {
                'text': text
            }

            response = requests.request('GET', url, params=payload, headers=headers).json()
            print(response)
            if response['code'] == 200:
                return response['data']
            else:
                print(response['code'])
                print(response['message'])
                return
        except Exception as e:
            print(e)
            return

    # 保存数据到json
    def save_data(self, wechat, from_wxid, api_data):
        try:
            if api_data is None:
                return

            dir_name = 'data'
            file_name = 'data/emotional_analysis.json'
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
                print('创建文件夹成功')
            if not os.path.isfile(file_name):
                with open(file_name, 'w', encoding='utf-8') as f:
                    init_list = self.creat_file(wechat)
                    res = json.dumps(init_list, ensure_ascii=False)
                    f.write(res)
                    print('创建文件成功')

            with open(file_name, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                # print(loaded_data)
            data = self.data_deal(api_data
                                  , loaded_data, from_wxid)
            print(data)
            result = json.dumps(data, ensure_ascii=False)
            # print(result)
            with open(file_name, 'w', encoding='utf-8') as f_w:
                f_w.write(result)
            print('数据保存成功')
        except Exception as e:
            print(e)

    # 初始化文件
    def creat_file(self, wechat):
        bf = BaseFunc()
        rooms = bf.get_rooms(wechat)

        # rooms = [{'avatar': 'http://wx.qlogo.cn/mmcrhead/8kZ3Gu8u0zZEia9Ewy0z2fCmTGhlUSXTQvJLvBLtYGTyGhnbMnGgHUcePbZ4WjYic4IjxlUoPQ0nZRcU1gmf8mXPQiaLOMpUDEc/0', 'is_manager': 0, 'manager_wxid': 'wxid_rbq4p73yvv0312', 'member_list': ['wxid_rbq4p73yvv0312', 'wxid_2xe76q5yl34k22', 'wxid_lo73nhg1rw0322', 'wxid_2ugano9m3lwl22'], 'nickname': 'cch', 'total_member': 4, 'wxid': '24928809083@chatroom'}, {'avatar': 'http://wx.qlogo.cn/mmcrhead/gWicbXPiajJniblHYcNtlzg58T5MCNz3Vac4OiaickHsxU1icz2Y12BHwlsZNe93d6ZmppRBc7Iicy2m199z2v5DXwy539LYRM6Gmr8/0', 'is_manager': 0, 'manager_wxid': 'wxid_a5v0xhouyi7v12', 'member_list': ['wxid_a5v0xhouyi7v12', 'wxid_l2j75kupc3an22', 'wxid_oe9515igvdoa21', 'wxid_lo73nhg1rw0322', 'wxid_rbq4p73yvv0312', 'wxid_fn4hhweo3fy022', 'wxid_2ugano9m3lwl22', 'wxid_9jb1p73eujsk12', 'wxid_p8zwf6yfxrwl21'], 'nickname': '仓鼠王特工队', 'total_member': 9, 'wxid': '20802233439@chatroom'}, {'avatar': 'http://wx.qlogo.cn/mmcrhead/OpISibvs8ES9XQ6VOiaQxukFlnvbXhxe3RzUXS1MW0SnwEJQu7w1KAlIkhvrOkrfH6M8XWftUp6dqlvFy6Bza8NuSQ0akOdBbl/0', 'is_manager': 0, 'manager_wxid': 'wxid_rbq4p73yvv0312', 'member_list': ['wxid_rbq4p73yvv0312', 'wxid_2ugano9m3lwl22'], 'nickname': '调试', 'total_member': 2, 'wxid': '17418658670@chatroom'}, {'avatar': 'http://wx.qlogo.cn/mmcrhead/V8yEicBeCu3A1n8fSNgXiavbuDGBiaF3ho7BZtuOBHj83hJ3emuDxia5B6llAicibV2ZTz2LWMJaoHC20FxR6vZo8iad1wibykx2WCFR/0', 'is_manager': 0, 'manager_wxid': 'wxid_qnccx4vnswxe22', 'member_list': ['wxid_qnccx4vnswxe22', 'wxid_2xe76q5yl34k22', 'wxid_rbq4p73yvv0312', 'wxid_lzedtxou05t122', 'wxid_3789567893112', 'wxid_zhllez9lz7x821', 'wxid_3o5pfaiv3y6922', 'rzx670440932', 'wxid_2ugano9m3lwl22'], 'nickname': '磊磊宝宝妈妈们可以！！！（小心xf', 'total_member': 9, 'wxid': '4654915424@chatroom'}, {'avatar': 'http://wx.qlogo.cn/mmcrhead/iaLxDYjaWtTdtwJSx8jsA8oANw4NBvTmDsmctYsIKcOQNmrgKFE3DfF1Cdrhh0J9UcYNf5NCPVSS0TeDEz6bicCrsvVHjpEcFN/0', 'is_manager': 0, 'manager_wxid': 'wxid_rbq4p73yvv0312', 'member_list': ['wxid_rbq4p73yvv0312', 'wxid_o0ho6rvhtcqw22', 'wxid_lo73nhg1rw0322', 'wxid_2ugano9m3lwl22'], 'nickname': '我没说你可以走了', 'total_member': 4, 'wxid': '22817919155@chatroom'}]

        init_list = []
        for i in range(len(rooms)):
            member_list = rooms[i]['member_list']
            for j in range(len(member_list)):
                wxid = member_list[j]
                init_dict = {
                    'wxid': wxid,
                    'times': 0,
                    'data': {
                        'positive_prob': 0.00,
                        'negative_prob': 0.00,
                        'part_of_speech': 0.00,
                        'sentiments': 0.00,
                        'good': 0,
                        'happiness': 0,
                        'sadness':  0,
                        'anger':  0,
                        'fear':  0,
                        'wickedness':  0,
                        'shock':  0
                    }
                }
                init_list.append(init_dict)
        data_lists = self.remove_duplicate(init_list)
        return data_lists

    def remove_duplicate(self, list1):
        """
        列表套字典去重复
        :param list1: 输入一个有重复值的列表
        :return: 返回一个去掉重复的列表
        """
        newlist = []
        for i in list1:  # 先遍历原始字典
            flag = True
            if newlist == []:  # 如果是空的列表就不会有重复，直接往里添加
                pass
            else:
                for j in newlist:
                    count = len(i.keys())
                    su = 0
                    for key in i.keys():
                        if i[key] == j[key]:
                            su += 1
                    if su == count:
                        flag = False
            if flag:
                newlist.append(i)
        return newlist

    def data_deal(self, api_data, saved_data, from_wxid):
        api_positive_prob = api_data['positive_prob']  # 积极类别的概率
        api_negative_prob = api_data['negative_prob']  # 消极类别的概率
        api_part_of_speech = api_data['part_of_speech']  # 词性标注、分析
        api_sentiments = api_data['sentiments']  # 表示情感极性分类结果的概率
        api_good = api_data['好']
        api_happiness = api_data['乐']
        api_sadness = api_data['哀']
        api_anger = api_data['怒']
        api_fear = api_data['惧']
        api_wickedness = api_data['恶']
        api_shock = api_data['惊']



        for i in range(len(saved_data)):
            wxid = saved_data[i]['wxid']
            if wxid == from_wxid:
                times = saved_data[i]['times']
                loaded_data = saved_data[i]['data']

                loaded_positive_prob = loaded_data['positive_prob']  # 积极类别的概率
                loaded_negative_prob = loaded_data['negative_prob']  # 消极类别的概率
                loaded_part_of_speech = loaded_data['part_of_speech']  # 词性标注、分析
                loaded_sentiments = loaded_data['sentiments']  # 表示情感极性分类结果的概率
                loaded_good = loaded_data['good']
                loaded_happiness = loaded_data['happiness']
                loaded_sadness = loaded_data['sadness']
                loaded_anger = loaded_data['anger']
                loaded_fear = loaded_data['fear']
                loaded_wickedness = loaded_data['wickedness']
                loaded_shock = loaded_data['shock']

                times += 1

                loaded_data['positive_prob'] = (loaded_positive_prob * (times-1) + api_positive_prob) / times
                loaded_data['negative_prob'] = (loaded_negative_prob * (times-1) + api_negative_prob) / times
                loaded_data['sentiments'] = (loaded_sentiments * (times-1) + api_sentiments) / times
                loaded_data['good'] = (loaded_good * (times-1) + api_good) / times
                loaded_data['happiness'] = (loaded_happiness * (times-1) + api_happiness) / times
                loaded_data['sadness'] = (loaded_sadness * (times-1) + api_sadness) / times
                loaded_data['anger'] = (loaded_anger * (times-1) + api_anger) / times
                loaded_data['fear'] = (loaded_fear * (times-1) + api_fear) / times
                loaded_data['wickedness'] = (loaded_wickedness * (times-1) + api_wickedness) / times
                loaded_data['shock'] = (loaded_shock * (times-1) + api_shock) / times

                saved_data[i]['times'] = times
                #
                # print(f'times:{times}')
                # print(f'saved_data[i]["times"]:{saved_data[i]["times"]}')
                #
                # print(f'loaded_positive_prob:{loaded_positive_prob}')
                # print(f'loaded_data["positive_prob"]:{loaded_data["positive_prob"]}')
                #
                # print(saved_data)
                return saved_data

if __name__ == '__main__':
    ea = EmotionalAnalysis()
    # text = '自动判断'
    # data = EmotionalAnalysis().emotional_analysis(text)
    api_data = {'positive_prob': 0.08, 'negative_prob': 0.04, 'part_of_speech': [['自动', 'd'], ['判断', 'v'], ['该', 'r'], ['文本', 'n'], ['的', 'u'], ['情感', 'n'], ['极性', 'vn'], ['类别', 'n'], ['并', 'c'], ['给出', 'v'], ['相应', 'v'], ['的置信', 'm'], ['度', 'q'], ['，', 'w'], ['情感', 'n'], ['极性', 'Dg'], ['分为', 'v'], ['积极', 'a'], ['、', 'w'], ['消极', 'a'], ['、', 'w'], ['中性', 'n'], ['。', 'w']], 'sentiments': 0.99996471967906, 'words': 23, 'sentences': 2, '好': 1, '乐': 0, '哀': 2, '怒': 0, '惧': 0, '恶': 1, '惊': 0}

    ea.save_data('wechat', 'wxid_rbq4p73yvv0312', api_data)
