import requests


class Bilibili:
    def get_response(self, room_id):
        try:
            url = f'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id={room_id}' \
                  f'&protocol=0,1&format=0,1,2&codec=0,1&qn=0&platform=web&ptype=8&dolby=5&panorama=1 '
            response = requests.get(url).json()
            return response
        except Exception as e:
            print(e)
            # response = {'code': -1, 'message': e, 'data': None}
            # print(response)
            # return response

    def get_live_status(self, room_id):
        response = self.get_response(room_id)
        code = response['code']
        if code == 0:
            data = response['data']
            print(data)
            live_status = data['live_status']
            if live_status == 0:
                return 0
            else:
                return 1
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


if __name__ == '__main__':
    wb = Bilibili()
    roomid = 25059330
    roomids = 83171
    wb.broadcast_remind(roomid)
    wb.broadcast_remind(roomids)
