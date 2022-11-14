import json

import requests

from base.base import BaseFunc


class Bilibili:
    def __init__(self):
        self.filename = r'C:\py\git\PythonProject\ntchat_wechat\data\bilibili_status.json'

    def get_room_response(self, room_id):
        try:
            url = f'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id={room_id}' \
                  f'&protocol=0,1&format=0,1,2&codec=0,1&qn=0&platform=web&ptype=8&dolby=5&panorama=1 '
            response = requests.get(url).json()
            return response
        except Exception as e:
            print(e)

    def get_room_info(self, room_id):
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/index/getOffLiveList?room_id={room_id}&count=8&rnd=1668134243'
        resonse = requests.get(url).json()
        print(resonse)
        data = resonse['data']
        record_list = data['record_list']
        print(record_list)

    def get_live_status(self, _room_id):

        with open(self.filename, 'r', encoding='utf-8') as f:
            status_list = json.load(f)
            print(status_list)

        for i in range(len(status_list)):
            dict_room_id = status_list[i]['room_id']
            response = self.get_room_response(_room_id)
            code = response['code']
            if code == 0:

                if _room_id == dict_room_id:
                    dict_live_status = status_list[i]['live_status']
                    dict_name = status_list[i]['name']
                    dict_room_title = status_list[i]['room_title']

                    data = response['data']
                    print(data)
                    live_status = data['live_status']
                    if dict_live_status == 0 and live_status == 1:    # 开播了
                        print('开播啦')
                        status_list[i]['live_status'] = 1

                        with open(self.filename, 'w', encoding='utf-8') as fs:
                            result = json.dumps(status_list, ensure_ascii=False)
                            fs.write(result)

                        return 1

                    elif dict_live_status == 1 and live_status == 0:  # 未开播
                        print('关播啦')
                        status_list[i]['live_status'] = 0

                        with open(self.filename, 'w', encoding='utf-8') as fs:
                            result = json.dumps(status_list, ensure_ascii=False)
                            fs.write(result)

                        return 0
            else:
                message = response['message']
                print(f'code:{code},message:{message}')
                return 0

    def broadcast_remind(self, room_id):
        res = self.get_live_status(room_id)
        if res:
            msg = f'{room_id}开播啦!\n' \
                  f'https://live.bilibili.com/{room_id}'
            print(msg)
            return msg
        else:
            return 0

    def write_status_init(self):
        # file_name = r'C:\py\git\PythonProject\ntchat_wechat\data\bilibili_status.json'

        status_list = [{
            'name': 'uzi',
            'room_id': 25059330,
            'room_title': '',
            'live_status': 1
        }]

        with open(self.filename, 'w', encoding='utf-8') as f:
            fs = json.dumps(status_list)
            f.write(fs)


if __name__ == '__main__':
    wb = Bilibili()
    wb.write_status_init()
    roomid = 25059330
    roomids = 83171
    wb.broadcast_remind(roomid)
    # wb.broadcast_remind(roomids)
    # wb.get_room_info(roomid)
