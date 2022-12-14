import time

from datetime import datetime
import api
from api import op_gg
from api.bilibili import Bilibili
from api.free import FreeApi
from api.hefeng import HefengApi
from api.hupu import Hupu
from api.muxiaoguo import MuxiaoguoApi
from api.qingyunke import get_reply
from api.tianapi import TianApi
from api.wanplus import WanPlus
from base.base import BaseFunc as bf
from base.reply import Reply
from csgo.csgo import Csgo
import schedule

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


def schedules(wechat):
    schedule.every(5).minutes.do(send_broadcast_remind, wechat=wechat)
    # schedule.every().day.at('08:00').do(send_morning_msg, wechat=wechat)
    # schedule.every().day.at('11:20').do(send_noon_msg, wechat=wechat)
    # schedule.every().day.at('15:00').do(send_everyday_a_song, wechat=wechat)
    # schedule.every().monday.at('16:20').do(send_afternoon_msg, wechat=wechat)
    # schedule.every().tuesday.at('16:20').do(send_afternoon_msg, wechat=wechat)
    # schedule.every().wednesday.at('16:20').do(send_afternoon_msg, wechat=wechat)
    # schedule.every().thursday.at('16:20').do(send_afternoon_msg, wechat=wechat)
    # schedule.every().friday.at('16:20').do(send_afternoon_msg, wechat=wechat)
    # schedule.every().day.at('00:00').do(add_money_everyday, wechat=wechat)

    # schedule.every().day.at('19:00').do(send_lpl_tomorrow_game_list, wechat=wechat)

    # schedule.every().day.at('00:00').do(get_hupu_cookie)
    # schedule.every(5).minutes.do(send_hupu_msg, wechat=wechat)

    # schedule.every(5).seconds.do(send_everyday_a_song, wechat=wechat)
    try:
        while True:
            schedule.run_pending()
            time.sleep(0.5)
    except Exception as e:
        print(e)


def send_broadcast_remind(wechat):
    room_id = [25059330, 48901]
    for i in range(len(room_id)):
        msg = Bilibili().broadcast_remind(room_id[i])
        if msg:
            wechat.send_text(to_wxid=bf().pipi_room, content=msg)

def send_morning_msg(wechat):
    msg = '各位打工人们，早上好！\n'
    today = datetime.now().strftime('%Y-%m-%d')
    morning_msg = TianApi().holiday(today)
    weather_msg = HefengApi().weather_now('宁波')
    life_tip = TianApi().lifeTips()

    msg = msg + morning_msg + weather_msg + life_tip

    wechat.send_text(to_wxid='20802233439@chatroom', content=msg)


def send_everyday_a_song(wechat):
    songName, songPic, songArtists, mp3url, content = MuxiaoguoApi().wangyiyun()
    time.sleep(1)
    msg = f'菲菲每日一曲：\n今天给大家带来的是：《{songName}》'
    wechat.send_text(to_wxid=bf().dadaji_room, content=msg)
    wechat.send_link_card(to_wxid=bf().dadaji_room, title=songName, desc=songArtists, url=mp3url, image_url=songPic)
    wechat.send_text(to_wxid=bf().dadaji_room, content=content)
    time.sleep(1)
    wechat.send_text(to_wxid=bf().leibao_room, content=msg)
    wechat.send_link_card(to_wxid=bf().leibao_room, title=songName, desc=songArtists, url=mp3url, image_url=songPic)
    wechat.send_text(to_wxid=bf().leibao_room, content=content)
    # wechat.send_text(to_wxid=bf().debug_room, content=msg)
    # wechat.send_link_card(to_wxid=bf().debug_room, title=songName, desc=songArtists, url=mp3url, image_url=songPic)
    # wechat.send_text(to_wxid=bf().debug_room, content=content)s


def send_noon_msg(wechat):
    noon_msg = '还有10分钟就要吃午餐了！'
    wechat.send_text(to_wxid='20802233439@chatroom', content=noon_msg)


def send_afternoon_msg(wechat):
    afternoon_msg = '还有10分钟就要下班了！今天也辛苦啦~'
    wechat.send_text(to_wxid=bf().dadaji_room, content=afternoon_msg)


def add_money_everyday(wechat):
    Csgo().add_all_money()
    msg = '今日份免费余额奖励已送达。\n请发送“@菲菲 查询余额”查收'
    wechat.send_text(to_wxid=bf().cch_room, content=msg)
    wechat.send_text(to_wxid=bf().leibao_room, content=msg)


def send_lpl_tomorrow_game_list(wechat):
    res = WanPlus().send_tomorrow_lpl_game()
    wechat.send_text(to_wxid=bf().pipi_room, content=res)


def get_hupu_cookie():
    Hupu().autologin()


def send_hupu_msg(wechat):
    hupu = Hupu()
    title = hupu.get_report()
    res = hupu.contrast(title)
    if res:
        with open(r'data/hupu_title.txt', 'r', encoding='utf-8') as f:
            title = f.read()
        # send title
        wechat.send_text(to_wxid=bf().pipi_room, content=title)
        # wechat.send_text(to_wxid=bf().leibao_room, content=title)
        print(title)
    else:
        return
