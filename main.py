# -*- coding: utf-8 -*-
import sys
import time
import xml
from xml import dom
from xml.dom import minidom

import ntchat

from base import schedule_list
from base.base import BaseFunc
from base.reply import Reply

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
    else:
        Reply().get_reply(wechat, msg, from_wxid, room_wxid, at_user_list)


@wechat.msg_register(ntchat.MT_RECV_FRIEND_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    xml_content = message["data"]["raw_msg"]
    dom = xml.dom.minidom.parseString(xml_content)

    # 从xml取相关参数
    encryptusername = dom.documentElement.getAttribute("encryptusername")
    ticket = dom.documentElement.getAttribute("ticket")
    scene = dom.documentElement.getAttribute("scene")

    # 自动同意好友申请
    ret = wechat_instance.accept_friend_request(encryptusername, ticket, int(scene))

    # if ret:
    # 通过后向他发条消息
    # wechat_instance.send_text(to_wxid=ret["userName"], content="你好!!!!!")


try:
    while True:
        time.sleep(0.5)
        schedule_list.schedules(wechat)
except Exception as e:
    if e == KeyboardInterrupt:
        ntchat.exit_()
        sys.exit()
    else:
        print(e)
