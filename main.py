# -*- coding: utf-8 -*-
import json
import re
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
from csgo.csgo import Csgo

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
    at_user_list = data["at_user_list"]

    if from_wxid == self_wxid:
        return
    # print(msg)
    nickname = "@菲菲\u2005"

    # ckd说的话
    if from_wxid == bf.ckd_id:
        if msg == 'get_room_member_wxid':
            bf.get_room_member_wxid(wechat, room_wxid)
        # elif msg == 'print_user_money':
        #     msg = Csgo().print_user_money(wechat, room_wxid)
        #     bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
        elif 'add_money' in msg:
            add_money = msg.split(' ')[1]
            Csgo().add_money(add_money)
            msg_1 = f'已为您添加{add_money}元。\n'
            print()
            msg_2 = Csgo().check_balance(from_wxid)
            msg = msg_1 + msg_2
            bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

    # 大家说的话
    if '电影' in msg and bf.movie_signal:
        res = '买电影票找@崔崔\u2005'
        bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        bf.movie_signal = False

    elif '@菲菲\u2005好的！' in msg:
        bf.movie_signal = True

    elif msg == 'print_user_money':
        msg = Csgo().print_user_money(wechat, room_wxid)
        bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

    elif msg == '模拟 龙狙':
        msg = Csgo().sim()
        bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

    elif '转账' in msg:
        try:
            print(at_user_list)
            number = re.findall(r"\b\d+\b", msg)
            msgs = Csgo().transfer_accounts(from_wxid, at_user_list, number)
        except Exception as e:
            msgs = e
        bf.send_textmsg(wechat, room_wxid, from_wxid, msgs, msgs)

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

    # @菲菲的话
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
            max_count = 5000
            if temp_msg == '开箱' or temp_msg == '开箱帮助':
                msg = f'欢迎来到模拟开箱，请@菲菲并输入开箱数量（不得大于{max_count}）以及武器箱名！\n' \
                      '例如：@菲菲\u2005开箱 100 命悬一线\n' \
                      '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' \
                      '目前支持的武器箱有：命悬一线、梦魇、古堡\n' \
                      '菲菲支持转账啦！\n输入"转账"并@你心爱的他 加上要转账的资金就可以啦！\n' \
                      '祝玩的开心！'
                bf.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
                # msg_1 = '抵制不良游戏，拒绝盗版游戏。\n' \
                #         '注意自我保护，谨防受骗上当。\n' \
                #         '适度游戏益脑，沉迷游戏伤身。\n' \
                #         '合理安排时间，享受健康生活。'
                # bf.send_textmsg(wechat, room_wxid, from_wxid, msg_1, msg_1)
            else:
                try:
                    temp = temp_msg.split(' ')
                    if len(temp) == 3:
                        print(temp)
                        case_count = int(temp[1])
                        case_name = temp[2]
                        print(case_name)
                        if 0 < case_count <= max_count:
                            # msg = '菲菲正在维护'
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
            res = Csgo().check_balance(from_wxid)

            bf.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif temp_msg == '测试':
            pass

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


def add_money_everyday():
    Csgo().add_all_money()
    msg = '今日份免费余额奖励已送达。\n请发送“@菲菲 查询余额”查收'
    wechat.send_text(to_wxid=bf.cch_room, content=msg)
    wechat.send_text(to_wxid=bf.leibao_room,content=msg)


schedule.every().day.at('08:00').do(send_morning_msg)
schedule.every().day.at('11:20').do(send_noon_msg)
schedule.every().day.at('15:00').do(send_everyday_a_song)
schedule.every().monday.at('16:20').do(send_afternoon_msg)
schedule.every().tuesday.at('16:20').do(send_afternoon_msg)
schedule.every().wednesday.at('16:20').do(send_afternoon_msg)
schedule.every().thursday.at('16:20').do(send_afternoon_msg)
schedule.every().friday.at('16:20').do(send_afternoon_msg)
schedule.every().day.at('00:00').do(add_money_everyday)

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
