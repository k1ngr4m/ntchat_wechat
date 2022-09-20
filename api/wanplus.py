import time
from datetime import datetime
from dateutil.parser import parse
import requests


class WanPlus:

    def get_scheduleList_request(self, match_time, match_name):
        time_stamp = int(time.mktime(time.strptime(match_time, "%Y-%m-%d")))
        # print(time_stamp)
        match_list = {
            '比赛': '1114,1116,1100',
            '资格赛': '1114',
            '冒泡赛': '1114',
            '入围赛': '1116',
            '夏季赛': '1100'}
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
                          'Safari/537.36 ',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = {
            '_gtk': 259095920,
            'game': 2,
            'time': time_stamp,
            'eids': match_list[match_name]
        }
        url = 'https://www.wanplus.cn/ajax/schedule/list'
        response = requests.post(url, headers=headers, data=data)
        data = response.json()
        # print(data)
        return data

    def get_scheduleList_by_week(self, match_time, match_name):
        data = WanPlus().get_scheduleList_request(match_time, match_name)
        code = data['code']
        if code == 0:
            datas = data['data']
            schedule_dict = datas['scheduleList']
            schedule_list = list(schedule_dict)
            # print(schedule_dict)
            # print(schedule_list)
            msg = ''
            for i in range(len(schedule_list)):
                daytime = schedule_list[i]  # 20220919
                schedule_time = schedule_dict[daytime]  # {"time": 1661961600,"date": "9-01","week": "周四","list": false,"lDate": "09-01 星期四","filterdate": "2022-09-01","selected": true}
                match_list = schedule_time['list']
                if match_list:
                    for j in range(len(match_list)):
                        match_id = match_list[j]['scheduleid']
                        team_a = match_list[j]['oneseedname']
                        team_b = match_list[j]['twoseedname']
                        start_time = match_list[j]['starttime']
                        match_date = match_list[j]['date']
                        match_name = match_list[j]['ename']
                        group_name = match_list[j]['groupname']
                        msg = msg + f'{match_date}\t{start_time}\n{match_name} {group_name}\n{team_a} VS {team_b}\n'
                else:
                    msg = msg + f'{daytime}没有比赛。\n'
            print(msg)
            return msg
        else:
            msg = data['msg']
            print(msg)
            return msg

    def get_scheduleList_by_day(self, match_time, match_name):
        if match_time == '今天':
            match_time = datetime.now().strftime('%Y-%m-%d')
            print(datetime.now().strftime('%Y-%m-%d'))
        data = WanPlus().get_scheduleList_request(match_time, match_name)
        code = data['code']
        if code == 0:
            datas = data['data']
            schedule_dict = datas['scheduleList']
            schedule_list = list(schedule_dict)
            msg = ''
            for i in range(len(schedule_list)):
                daytime = schedule_list[i]
                schedule_time = schedule_dict[daytime]
                match_list = schedule_time['list']
                filterdate = schedule_time['filterdate']
                if match_time == filterdate:
                    if match_list:
                        for j in range(len(match_list)):
                            match_id = match_list[j]['scheduleid']
                            team_a = match_list[j]['oneseedname']
                            team_b = match_list[j]['twoseedname']
                            start_time = match_list[j]['starttime']
                            match_date = match_list[j]['date']
                            match_name = match_list[j]['ename']
                            group_name = match_list[j]['groupname']
                            msg = msg + f'{match_date}\t{start_time}\n{match_name} {group_name}\n{team_a} VS {team_b}\n'
                    else:
                        msg = msg + f'{match_time}没有{match_name}。\n'
            print(msg)
            return msg
        else:
            msg = data['msg']
            print(msg)
            return msg

    def filter_msg(self, msg):
        msg = msg.replace('查询比赛', '')
        msg_list = msg.split(' ')
        print(len(msg_list))
        match_time = ''
        match_name = ''
        if len(msg_list) == 3:
            match_time = msg_list[1]
            match_name = msg_list[2]
        elif len(msg_list) == 2:
            try:
                match_time = parse(msg).strftime('%Y-%m-%d')
            except:
                res = '日期出错'
                return res
            match_name = '比赛'
        elif len(msg_list) == 1:
            match_time = '今天'
            match_name = '比赛'
        res = WanPlus().get_scheduleList_by_day(match_time, match_name)
        return res