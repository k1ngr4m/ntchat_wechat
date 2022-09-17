import sys

import ntchat
import requests

from base.base import BaseFunc


class TianApi(BaseFunc):
    def __init__(self):
        super().__init__()
        self.APIKEY = '78eecbde458746d29cb65407ef696781'

    # 微博热搜
    def hotSearch(self, msg):
        url = f"http://api.tianapi.com/weibohot/index?key={self.APIKEY}"
        response = requests.get(url)
        res = response.json()['newslist']
        news_list = '现在的热搜是：\n '
        for i in range(len(res)):
            news = res[i]['hotword']
            hotwordnum = res[i]['hotwordnum']  # 热搜指数
            hottag = res[i]['hottag']
            link = f"https://s.weibo.com/weibo?q={news}"
            if '安卓' in msg:
                news_list = news_list + f'[{i + 1}] {news} {link}\n'
            else:
                news_list = news_list + f'[{i + 1}] #{news} {hotwordnum} {hottag}\n '
        print(news_list)
        return news_list

    # 游戏资讯
    def gameNews(self):
        url = f'http://api.tianapi.com/game/index?key={self.APIKEY}&num=20'
        res = requests.get(url).json()
        newslist = res['newslist']
        code = res['code']
        if code == 200:
            msg = '今日游戏资讯：\n'
            for i in range(len(newslist)):
                ctime = newslist[i]['ctime']
                title = newslist[i]['title']
                description = newslist[i]['description']
                urls = newslist[i]['url']
                msg = msg + f'[{i + 1}] {title}\n'
                # msg = msg + f'[{i + 1}] {title}\n    {urls}\n'
                # print(f'[{i+1}] {ctime}\n    {title}\n    {description}\n    {urls}')
            return msg
        else:
            msg = '出错啦，找崔崔'
            return msg

    # 节假日
    def holiday(self, date):
        url = f'http://api.tianapi.com/jiejiari/index?key={self.APIKEY}&date={date}'
        res = requests.get(url).json()
        newslist = res['newslist'][0]
        code = res['code']
        if code == 200:
            print(newslist)
            cnweekday = newslist['cnweekday']
            info = newslist['info']
            holiday_name = newslist['name']
            if holiday_name == '':
                morning_msg = f'今天是{date}，{cnweekday}，{info}\n'
            else:
                morning_msg = f'今天是{date}，{cnweekday}，{info}，是“{holiday_name}\n”'
            return morning_msg

    # 生活小常识
    def lifeTips(self):
        url = f'http://api.tianapi.com/qiaomen/index?key={self.APIKEY}'
        response = requests.get(url)
        res = response.json()['newslist'][0]
        content = res['content']
        msg = f'生活小窍门：{content}'
        return msg

    # 百科题库
    def baikeTiku(self, wechat, room_wxid, from_wxid):
        url = f"http://api.tianapi.com/baiketiku/index?key={self.APIKEY}"
        response = requests.get(url)
        code = response.json()['code']
        newslist = response.json()['newslist'][0]
        if code == 200:
            title = newslist['title']
            answerA = newslist['answerA']
            answerB = newslist['answerB']
            answerC = newslist['answerC']
            answerD = newslist['answerD']
            answer = newslist['answer']
            answerlower = chr(ord(answer) + 32)
            analytic = newslist['analytic']
            send_msg = f"{title}\nA:{answerA}\nB:{answerB}\nC:{answerC}\nD:{answerD}"
            print(send_msg)
            print(f"answer:{answer}")
            self.send_textmsg(wechat, room_wxid, from_wxid, send_msg, send_msg)

            @wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
            def on_recv_text_msgs(wechat: ntchat.WeChat, message):
                data1 = message["data"]
                msg1 = data1["msg"]
                from_wxid1 = data1["from_wxid"]
                room_wxid1 = data1["room_wxid"]
                self_wxid1 = wechat.get_login_info()["wxid"]
                if from_wxid1 == self_wxid1:
                    return

                if room_wxid1 == room_wxid:
                    nickname = "@菲菲\u2005"
                    if nickname in msg1:
                        temp_msg = self.delete_head(msg1, nickname)
                        if temp_msg == answer or temp_msg == answerlower:
                            res = f"恭喜你，答对啦！正确的答案是{answer}！\n{analytic}"
                            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
                            return
                        elif temp_msg == "退出":
                            return
                        else:
                            res = f"猜错啦！不是{temp_msg}！"
                            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
                else:
                    pass
