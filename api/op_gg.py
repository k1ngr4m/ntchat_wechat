import json

from base.base import BaseFunc as bf


def get_opgg(wechat, msg, room_wxid, from_wxid):
    tf = open(r"C:\Webot\Scripts\Json\lol.json", "r")
    dict1 = json.load(tf)
    name = bf().delete_head(msg, ele='大乱斗')
    for key, value in dict1.items():
        if name in key:
            champion = dict1[name]
            res = f"https://www.op.gg/modes/aram/{champion}/build"
            bf().send_textmsg(wechat, room_wxid, from_wxid, res, res)
            path = r"C:\py\screenshot"
            png_path = path + '/{}.png'.format(f'{champion}_opgg_screenshot')
            # print(png_path)
            bf().send_imagemsg(wechat, room_wxid, from_wxid, png_path, png_path)
            return