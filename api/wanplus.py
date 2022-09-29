import time
from datetime import datetime, date, timedelta
from dateutil.parser import parse
import requests


class WanPlus:
    def __init__(self):
        self.team_list = ['RNG', 'EDG', 'TES', 'JDG']

    def get_scheduleList_request(self, match_time, match_name):
        try:
            time_stamp = int(time.mktime(time.strptime(match_time, "%Y-%m-%d")))
            # print(time_stamp)
            match_list = {
                '全部比赛': '1114,1116,1117,1100',
                '资格赛': '1114',
                '冒泡赛': '1114',
                '入围赛': '1116',
                '夏季赛': '1100',
                '小组赛': '1117'}
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
        except Exception as e:
            print(e)
            return

    def get_scheduleList_by_week(self, match_time, match_name, team_name):
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
                schedule_time = schedule_dict[
                    daytime]  # {"time": 1661961600,"date": "9-01","week": "周四","list": false,"lDate": "09-01 星期四","filterdate": "2022-09-01","selected": true}
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
                        if team_a == team_name or team_b == team_name:
                            msg = msg + f'{match_date}\t{start_time}\n{match_name} {group_name}\n{team_a} VS {team_b}\n\n'
                # else:
                #     msg = msg + f'{daytime}没有比赛。\n'
            # print(msg)
            return msg
        else:
            msg = data['msg']
            # print(msg)
            return msg

    def get_scheduleList_by_day(self, match_time, match_name, team_name='all'):
        match_time = str(match_time)
        print(match_time)
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
                            if team_name != 'all':
                                if team_a == team_name or team_b == team_name:
                                    msg = msg + f'{match_date}\t{start_time}\n{match_name} {group_name}\n{team_a} VS {team_b}\n\n'
                            else:
                                msg = msg + f'{match_date}\t{start_time}\n{match_name} {group_name}\n{team_a} VS {team_b}\n\n'
                    else:
                        if team_name != 'all':
                            msg = msg + f'{match_time}没有{team_name}比赛。\n'
                        else:
                            msg = msg + f'{match_time}没有比赛。\n'
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
                match_time = msg_list[1]
                if match_time == '今天':
                    match_time = date.today()
                elif match_time == '明天':
                    match_time = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
                elif match_time == '昨天':
                    match_time = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
                else:
                    match_time = parse(msg).strftime('%Y-%m-%d')
            except:
                res = '日期出错'
                return res
            match_name = '全部比赛'
        elif len(msg_list) == 1:
            match_time = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
            match_name = '全部比赛'
        res = WanPlus().get_scheduleList_by_day(match_time, match_name)
        return res

    def lpl_game(self):
        # team_list = ['RNG', 'EDG', 'TES', 'JSG']
        msgs = ''
        for i in range(len(self.team_list)):
            for j in range(0, 5):
                x = 7 * j
                match_time = (date.today() + timedelta(days=x)).strftime("%Y-%m-%d")
                msg = self.get_scheduleList_by_week(str(match_time), '全部比赛', self.team_list[i])

                if msg:
                    msgs = msgs + msg
        print(msgs)
        return msgs

    def send_tomorrow_lpl_game(self):
        match_time = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        msg = ''
        for i in range(len(self.team_list)):
            msg = msg + self.get_scheduleList_by_day(match_time, '全部比赛', team_name=self.team_list[i])
        return msg
