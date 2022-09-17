import requests

from base.base import BaseFunc


class MuxiaoguoApi(BaseFunc):
    # 彩虹屁
    def caihongpi(self):
        url = 'https://api.muxiaoguo.cn/api/caihongpi?api_key=dadd3a50136a2ee4'
        response = requests.get(url).json()
        code = response['code']
        if code == 200:
            comment = response['data']['comment']
            return comment
        else:
            return 'error'

    # 网易云热评
    def song_reping(self):
        url = 'https://api.muxiaoguo.cn/api/163reping?api_key=3ee5be5bf9a4bc42'
        response = requests.get(url).json()
        code = response['code']
        if code == 200:
            data = response['data']
            content = data['content']
            songId = data['songId']
            print(songId)
            print(content)
            return songId, content
            # return comment
        else:
            return 'error'

    # 网易云解析
    def song_jiexi(self, id):
        url = f'https://api.muxiaoguo.cn/api/163music?api_key=552745858bcc14d5&id={id}'
        response = requests.get(url).json()
        code = response['code']
        if code == 200:
            data = response['data']
            mp3url = data['mp3url']
            songName = data['songName']
            songPic = data['songPic']
            songArtists = data['songArtists']
            songurl = f'https://y.music.163.com/m/song?id={id}'
            # pic_filename = self.pic(songPic, songName)
            # print(mp3url)

            return songName, songPic, songArtists, songurl

        else:
            return 'error'

    def wangyiyun(self):
        songid, content = self.song_reping()
        songName, songPic, songArtists, mp3url = self.song_jiexi(songid)
        return songName, songPic, songArtists, mp3url, content
