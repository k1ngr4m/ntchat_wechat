# -*- coding: utf-8 -*-
from datetime import datetime
import sys
import ntchat
import urllib.request
import os, stat

import urllib.request


class BaseFunc:
    def __init__(self):
        self.robot_id = 'wxid_2ugano9m3lwl22'
        self.movie_signal = True
        self.cdkey = 'DSAJK-DHO34-A341G-F45VB'
        self.cdkey_signal = True
        self.cdkey_signal_2 = False
        self.debug_room = '17418658670@chatroom'
        self.dadaji_room = '20802233439@chatroom'
        self.cch_room = '24928809083@chatroom'
        self.hrj_id = 'wxid_2xe76q5yl34k22'
        self.ckd_id = 'wxid_rbq4p73yvv0312'
        self.cst_id = 'wxid_lo73nhg1rw0322'
        self.leibao_room = '4654915424@chatroom'
        self.xf_id = 'wxid_lzedtxou05t122'
        self.user = ''
        self.pipi_room = '22817919155@chatroom'
        self.mine_signal = False
        self.into_mine_signal = True

    def get_contacts_and_rooms(self, wechat):
        # 等待登录
        wechat.wait_login()

        # 获取联系人列表并输出
        contacts = wechat.get_contacts()

        print("联系人列表: ")
        print(contacts)

        rooms = wechat.get_rooms()
        print("群列表: ")
        print(rooms)

    def get_room_member_wxid(self, wechat, room_wxid):
        data = wechat.get_room_members(room_wxid)
        member_list = data['member_list']
        # print(member_list)
        msg = ''
        for i in range(len(member_list)):
            nick_name = member_list[i]['nickname']
            wxid = member_list[i]['wxid']
            msg = msg + f'{nick_name}：{wxid}\n'
        wechat.send_text(to_wxid=room_wxid, content=msg)

    def delete_head(self, msg, ele):
        return msg.replace(ele, '')

    # 发送文本消息
    def send_textmsg(self, wechat, room_wxid, from_wxid, room_res, from_res):
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content=room_res)
        else:
            wechat.send_text(to_wxid=from_wxid, content=from_res)

    # 发送图片消息
    def send_imagemsg(self, wechat, room_wxid, from_wxid, room_file_path, from_file_path):
        if room_wxid != "":
            wechat.send_image(to_wxid=room_wxid, file_path=room_file_path)
        else:
            wechat.send_image(to_wxid=from_wxid, file_path=from_file_path)

    # 发送url图片游戏
    def send_url_image_msg(self, wechat, room_wxid, from_wxid, url, pic_name):
        filename = self.pic(url, pic_name)
        if room_wxid != "":
            wechat.send_image(to_wxid=room_wxid, file_path=filename)
        else:
            wechat.send_image(to_wxid=from_wxid, file_path=filename)

    # 发送群@消息
    def send_roomat_msg(self, wechat, room_wxid, from_wxid, room_res, from_res, at_list):
        if room_wxid != "":
            wechat.send_room_at_msg(to_wxid=room_wxid, content=room_res, at_list=at_list)
        else:
            wechat.send_room_at_msg(to_wxid=from_wxid, content=from_res, at_list=at_list)

    # 图片转换成文件
    def pic(self, url, pic_name):
        img_url = url
        file_path = 'C:/img'
        file_name = pic_name
        try:
            # 是否有这个路径
            if not os.path.exists(file_path):
                # 创建路径
                os.makedirs(file_path)
            # 获得图片后缀
            file_suffix = os.path.splitext(img_url)[1]
            print(file_suffix)
            # 拼接图片名（包含路径）
            filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
            print(filename)
            opener = urllib.request.build_opener()
            opener.addheaders = [(
                'User-Agent',
                'Mozilla / 5.0 (Windows NT 6.1; WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                '36.0.1941.0Safari / 537.36 '
            )]
            urllib.request.install_opener(opener)
            # 下载图片，并保存到文件夹中
            urllib.request.urlretrieve(img_url, filename=filename)
            return filename
        except IOError as e:
            print(f"IOError:{e}")
        except Exception as e:
            print("Exception")
