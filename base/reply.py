# -*- coding: utf-8 -*-
import random
import re

import api
from api import op_gg
from api.free import FreeApi
from api.hupu import Hupu
from api.muxiaoguo import MuxiaoguoApi
from api.qingyunke import get_reply
from api.tianapi import TianApi
from api.wanplus import WanPlus
from api.yuanshen import Yuanshen
from csgo.csgo import Csgo

from base.base import BaseFunc
from game import mine
from game.ticket import Ticket


class Reply(BaseFunc):
    def get_reply(self, bf, wechat, msg, from_wxid, room_wxid, at_user_list):

        # ckd说的话
        if from_wxid == self.ckd_id:
            self.personal_statement(wechat, room_wxid, from_wxid, msg)

        self.others_statement(wechat, room_wxid, from_wxid, at_user_list, msg, bf)

    def personal_statement(self, wechat, room_wxid, from_wxid, msg):
        if msg == 'get_room_member_wxid':
            self.get_room_member_wxid(wechat, room_wxid)
        elif 'add_money' in msg:
            add_money = msg.split(' ')[1]
            Csgo().add_money(from_wxid, add_money)
            msg_1 = f'已为您添加{add_money}元。\n'
            print()
            msg_2 = Csgo().check_balance(from_wxid)
            msg = msg_1 + msg_2
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

    def others_statement(self, wechat, room_wxid, from_wxid, at_user_list, msg, bf):
        nickname = "@菲菲\u2005"
        # 大家说的话

        if '大乱斗' in msg:
            self.opgg(msg, wechat, room_wxid, from_wxid)

        elif '转账' in msg:
            self.transfer_accounts(msg, wechat, room_wxid, from_wxid, at_user_list)

        elif '开箱' in msg:
            self.open_case(msg, wechat, room_wxid, from_wxid)

        elif '查询比赛' in msg:
            self.search_game(msg, wechat, room_wxid, from_wxid)

        elif '原神' in msg:
            if msg == '今日原神材料':
                role_path, weapon_path = Yuanshen().get_item_path()
                wechat.send_image(to_wxid=room_wxid, file_path=role_path)
                wechat.send_image(to_wxid=room_wxid, file_path=weapon_path)
                path = Yuanshen().get_item()
                wechat.send_image(to_wxid=room_wxid, file_path=path)

        elif msg == 'print_user_money':
            msg = Csgo().print_user_money(wechat, room_wxid)
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

        elif msg == '模拟 龙狙':
            msg = Csgo().sim()
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)

        elif msg == '热搜' or msg == '热搜安卓':
            hot_search_url = 'https://weibo.com/hot/search'
            pic_url = 'https://www.somode.com/uploadimg/ico/2022/0810/1660120968235761.jpg'
            res = TianApi().hotSearch(msg)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '游戏资讯':
            res = TianApi().gameNews()
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '狗狗' or msg == '猫猫' or msg == '柴犬':
            if msg == '狗狗':
                filename = FreeApi().random_dog()
            elif msg == '柴犬':
                filename = FreeApi().random_Shiba()
            else:
                filename = FreeApi().random_cat()
            self.send_imagemsg(wechat, room_wxid, from_wxid, filename, filename)

        elif msg == '百科题库':
            res = '此功能还在开发中'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
            # TianApi().BaikeTiku(wechat, room_wxid, from_wxid)

        elif msg == '来首网易云':
            songName, songPic, songArtists, mp3url, content = MuxiaoguoApi().wangyiyun()
            # wechat.send_text(to_wxid=room_wxid, content=msg)
            wechat.send_link_card(to_wxid=room_wxid, title=songName, desc=songArtists, url=mp3url,
                                  image_url=songPic)
            wechat.send_text(to_wxid=room_wxid, content=content)

        elif msg == '查询余额':
            res = Csgo().check_balance(from_wxid)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '扫雷' and bf.into_mine_signal:
            bf.user = from_wxid
            bf.mine_signal = True
            bf.into_mine_signal = False
            mine.play(wechat, room_wxid, from_wxid)
            return

        elif msg == '扫雷' and bf.into_mine_signal == False:
            res = '已经有人在玩扫雷，请等待当前玩家结束。'
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif from_wxid == bf.user and bf.mine_signal:
            if msg == '退出':
                res = '欢迎下次来玩。'
                self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
                bf.into_mine_signal = True
                bf.mine_signal = False
            else:
                mine.plays(wechat, room_wxid, msg, bf)

        # elif msg == '购买彩票':
        #     res = Ticket().get_num_and_save(from_wxid)
        #     self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
        #
        # elif msg == '开奖':
        #     res = Ticket().run_a_lottery(from_wxid)
        #     self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

        elif msg == '测试':
            try:
                hupu = Hupu()
                title = hupu.get_report()
                res = hupu.contrast(title)
                if res:
                    with open(r'data/hupu_title.txt', 'r', encoding='utf-8') as f:
                        title = f.read()
                    # send title
                    wechat.send_text(to_wxid=room_wxid, content=title)
                    print(title)
                else:
                    return
            except Exception as e:
                print(e)


        # @菲菲说的话
        elif nickname in msg:
            temp_msg = self.delete_head(msg, nickname)
            res = api.qingyunke.get_reply(temp_msg)
            self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

    def open_case(self, msg, wechat, room_wxid, from_wxid):
        print(msg)
        max_count = 1000
        if msg == '开箱' or msg == '开箱帮助':
            msg = f'欢迎来到模拟开箱，请输入开箱数量（不得大于{max_count}）以及武器箱名！\n' \
                  '例如：开箱 100 命悬一线\n' \
                  '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' \
                  '目前支持的武器箱有：命悬一线、梦魇、古堡\n' \
                  '菲菲支持转账啦！\n输入"转账"并@你心爱的他 加上要转账的资金就可以啦！\n' \
                  '祝玩的开心！'
            self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
        else:
            try:
                temp = msg.split(' ')
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
                self.send_textmsg(wechat, room_wxid, from_wxid, msg, msg)
                # wechat.send_pat(room_wxid, from_wxid)
            except Exception as e:
                self.send_textmsg(wechat, room_wxid, from_wxid, e, e)

    def search_game(self, msg, wechat, room_wxid, from_wxid):
        if msg == '查询比赛 帮助':
            res = '发送【查询比赛】：查询明天所有比赛。\n' \
                  '发送【查询比赛 昨天/今天/明天（或指定日期）】：查询指定日期所有比赛。\n' \
                  '发送【查询比赛全部lpl】：查询全部lpl比赛。\n' \
                  '发送【查询比赛lpl】：查询明天lpl比赛\n' \
                  '~~~~~~~~~~~~~\n' \
                  '暂未支持查询指定战队比赛。'
        elif msg == '查询比赛全部lpl':
            res = WanPlus().lpl_game()
        elif msg == '查询比赛lpl':
            res = WanPlus().send_tomorrow_lpl_game()
        else:
            res = WanPlus().filter_msg(msg)
        self.send_textmsg(wechat, room_wxid, from_wxid, res, res)

    def transfer_accounts(self, msg, wechat, room_wxid, from_wxid, at_user_list):
        try:
            print(at_user_list)
            number = re.findall(r"\b\d+\b", msg)
            msgs = Csgo().transfer_accounts(from_wxid, at_user_list, number)
        except Exception as e:
            msgs = e
        self.send_textmsg(wechat, room_wxid, from_wxid, msgs, msgs)

    def opgg(self, msg, wechat, room_wxid, from_wxid):
        res = op_gg.get_opgg(wechat, msg, room_wxid, from_wxid)
        self.send_textmsg(wechat, room_wxid, from_wxid, res, res)
