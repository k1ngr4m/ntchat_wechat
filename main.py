# -*- coding: utf-8 -*-
import random
import sys
import time
from datetime import datetime

import ntchat
import schedule

import api
from api import op_gg
from api.free import FreeApi
from api.hefeng import HefengApi
from api.muxiaoguo import MuxiaoguoApi
from api.qingyunke import get_reply
from api.tianapi import TianApi
from base.base import BaseFunc
from api.csgo import Csgo

wechat = ntchat.WeChat()
wechat.open(smart=True)
wechat.wait_login()
bf = BaseFunc()


@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat: ntchat.WeChat, message):
    # print(message)
    data = message["data"]
    msg = data["msg"]
    from_wxid = data["from_wxid"]
    room_wxid = data["room_wxid"]
    self_wxid = wechat.get_login_info()["wxid"]

    if from_wxid == self_wxid:
        return
    # print(msg)
    nickname = "@菲菲\u2005"

    # if (from_wxid == bf.hrj_id or from_wxid == bf.cst_id) and msg != '@菲菲\u2005开个命悬一线':
    #     at_list = [from_wxid]
    #     randint = random.randint(0, 100)
    #     print(randint)
    #     if randint <= 10:
    #         caihongpi = MuxiaoguoApi().caihongpi()
    #         wechat.send_room_at_msg(room_wxid, caihongpi, at_list)
    #         wechat.send_pat(room_wxid, from_wxid)
    #     else:
    #         pass

    if '电影' in msg and bf.movie_signal:
        res = '买电影票找@崔崔\u2005'
        bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        bf.movie_signal = False

    elif '@菲菲\u2005好的！' in msg:
        bf.movie_signal = True

    # elif 'rzx' in msg:
    #     res = 'rzx大帅逼！'
    #     bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)
    #     caihongpi = MuxiaoguoApi().caihongpi()
    #     bf.send_textmsg(wechat, room_wxid, from_wxid, caihongpi, caihongpi)
    #     wechat.send_pat(room_wxid, 'rzx670440932')
    #
    # elif '崔总' in msg:
    #     res = 'cst大帅逼'
    #     bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)
    #     caihongpi = MuxiaoguoApi().caihongpi()
    #     bf.send_textmsg(wechat, room_wxid, from_wxid, caihongpi, caihongpi)
    #     wechat.send_pat(room_wxid, bf.cst_id)

    elif nickname in msg:
        temp_msg = bf.delete_head(msg, nickname)
        # print(temp_msg)
        if temp_msg[0:2] == '功能':
            res = '天气(杭州天气)'
            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif '大乱斗' in temp_msg:
            op_gg.get_opgg(wechat, temp_msg, room_wxid, from_wxid)

        elif temp_msg == '热搜' or temp_msg == '热搜安卓':
            hot_search_url = 'https://weibo.com/hot/search'
            pic_url = 'https://www.somode.com/uploadimg/ico/2022/0810/1660120968235761.jpg'
            res = TianApi().hotSearch(temp_msg)
            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif temp_msg == '游戏资讯':
            res = TianApi().gameNews()
            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif temp_msg == '狗狗' or temp_msg == '猫猫':
            if temp_msg == '狗狗':
                filename = FreeApi().random_dog()
            else:
                filename = FreeApi().random_cat()
            bf.send_imagemsg(wechat, room_wxid, from_wxid, filename, filename)

        elif temp_msg == '百科题库':
            res = '此功能还在开发中'
            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)
            # TianApi().BaikeTiku(wechat, room_wxid, from_wxid)

        elif temp_msg == '来首网易云':
            songName, songPic, songArtists, mp3url, content = MuxiaoguoApi().wangyiyun()
            wechat.send_text(to_wxid=room_wxid, content=msg)
            wechat.send_link_card(to_wxid=room_wxid, title=songName, desc=songArtists, url=mp3url,
                                  image_url=songPic)
            wechat.send_text(to_wxid=room_wxid, content=content)

        elif '开箱' in temp_msg:
            print(temp_msg)
            max_count = 1000
            if temp_msg == '开箱' or temp_msg == '开箱帮助':
                msg = f'欢迎来到模拟开箱，请@菲菲并输入开箱数量（不得大于{max_count}）以及武器箱名！\n' \
                      '例如：@菲菲\u2005开箱 100 命悬一线\n' \
                      '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' \
                      '目前支持的武器箱有：命悬一线、梦魇\n' \
                      '单抽出金@崔崔，奖励五块现金红包\n' \
                      '祝玩的开心！'
                bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
                msg_1 = '抵制不良游戏，拒绝盗版游戏。\n' \
                        '注意自我保护，谨防受骗上当。\n' \
                        '适度游戏益脑，沉迷游戏伤身。\n' \
                        '合理安排时间，享受健康生活。'
                bf.send_textmsg(wechat, room_wxid, from_wxid, msg_1, msg_1)
            else:
                try:
                    temp = temp_msg.split(' ')
                    if len(temp) == 3:
                        print(temp)
                        case_count = int(temp[1])
                        case_name = temp[2]
                        print(case_name)
                        if 0 < case_count <= max_count:
                            msg = Csgo().open_cases(from_wxid, case_count, case_name)
                        else:
                            msg = f'您输入的数量有误！当前仅支持1-{max_count}'
                    else:
                        msg = '输入有误！'
                    bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
                    # wechat.send_pat(room_wxid, from_wxid)
                except Exception as e:
                    bf.send_textmsg(wechat, room_wxid, from_wxid, e, e)

        elif temp_msg == '查询余额':
            money = Csgo().check_balance(from_wxid)
            can_open = int(money / 16)
            res = f'您的余额为：{money}元，还能开{can_open}个箱子'
            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif temp_msg == '测试':
            mp3_url = 'http://m801.music.126.net/20220915142742/0b265f7e748029994495a8d09f5567cc/jdymusic/obj/wo3DlMOGwrbDjj7DisKw/14096450557/29ab/ac4c/10ba/22ee7a09879bc9cc03e66b50fabbab5f.mp3'
            wechat.send_link_card(room_wxid, 'song', 'songid', mp3_url, r'C:/img/temp.jpg')

        else:
            res = api.qingyunke.get_reply(temp_msg)
            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)

    else:
        pass


#     msg = '各位老船长：\n1. 本周摸鱼🐟情况汇总\n2. 下周摸鱼🐟计划\n3. 需协同撒网事项(需协同)\n4. 摸鱼心得(工作心得)\n5. 船长养成计划(学习心得)'
def send_morning_msg():
    msg = '各位打工人们，早上好！\n'
    today = datetime.now().strftime('%Y-%m-%d')
    morning_msg = TianApi().holiday(today)
    weather_msg = HefengApi().weather_now('宁波')
    life_tip = TianApi().lifeTips()

    msg = msg + morning_msg + weather_msg + life_tip

    wechat.send_text(to_wxid='20802233439@chatroom', content=msg)
    # wechat.send_text(to_wxid='4654915424@chatroom', content=msg)


def send_everyday_a_song():
    songName, songPic, songArtists, mp3url, content = MuxiaoguoApi().wangyiyun()
    time.sleep(1)
    msg = f'菲菲每日一曲：\n今天给大家带来的是：《{songName}》'
    wechat.send_text(to_wxid=bf.dadaji_room, content=msg)
    wechat.send_link_card(to_wxid=bf.dadaji_room, title=songName, desc=songArtists, url=mp3url, image_url=songPic)
    wechat.send_text(to_wxid=bf.dadaji_room, content=content)
    # time.sleep(1)
    # wechat.send_text(to_wxid=bf.leibao_room, content=msg)
    # wechat.send_link_card(to_wxid=bf.leibao_room, title=songName, desc=songArtists, url=mp3url, image_url=songPic)
    # wechat.send_text(to_wxid=bf.leibao_room, content=content)


def send_noon_msg():
    noon_msg = '还有10分钟就要吃午餐了！'
    wechat.send_text(to_wxid='20802233439@chatroom', content=noon_msg)


def send_afternoon_msg():
    afternoon_msg = '还有10分钟就要下班了！今天也辛苦啦~'
    wechat.send_text(to_wxid=bf.dadaji_room, content=afternoon_msg)


schedule.every().day.at('08:00').do(send_morning_msg)
schedule.every().day.at('11:20').do(send_noon_msg)
schedule.every().day.at('15:00').do(send_everyday_a_song)
schedule.every().monday.at('16:20').do(send_afternoon_msg)
schedule.every().tuesday.at('16:20').do(send_afternoon_msg)
schedule.every().wednesday.at('16:20').do(send_afternoon_msg)
schedule.every().thursday.at('16:20').do(send_afternoon_msg)
schedule.every().friday.at('16:20').do(send_afternoon_msg)

# schedule.every(5).seconds.do(send_everyday_a_song)
"""
# 每小时执行
schedule.every().hour.do(job)
# 每天12:25执行
schedule.every().day.at("12:25").do(job)
# 每2到5分钟时执行
schedule.every(5).to(10).minutes.do(job)
# 每星期4的19:15执行
schedule.every().thursday.at("19:15").do(job)
# 每第17分钟时就执行
schedule.every().minute.at(":17").do(job)
"""
try:
    while True:
        schedule.run_pending()
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
