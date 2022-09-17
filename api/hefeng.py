import requests

from base.base import BaseFunc


class HefengApi(BaseFunc):
    def __init__(self):
        super().__init__()
        self.key = '5d1c676fb7e249b3b6cb76e1188d7f08'

    # 获取Location ID
    def geo_citylookup(self, location):
        url = f'https://geoapi.qweather.com/v2/city/lookup?location={location}&key={self.key}'
        response = requests.get(url).json()
        code = response['code']
        if code == '200':
            locations = response['location']
            location_id = locations[0]['id']
            return location_id
        else:
            error = 'geoid出错了,找崔崔'
            print(f'code:{code},{error}')
            return error

    # 获取天气
    def weather_now(self, location):
        location_id = self.geo_citylookup(location)
        url = f'https://devapi.qweather.com/v7/weather/now?key={self.key}&location={location_id}'
        response = requests.get(url).json()
        code = response['code']
        if code == '200':
            now = response['now']
            temperature = now['temp']
            text = now['text']
            windDir = now['windDir']
            windScale = now['windScale']
            weather_msg = f'当前气温{temperature}℃，{text}，{windDir}{windScale}级\n'
            return weather_msg
        else:
            error = '出错了,找崔崔'
            print(error)
            return error

    # 获取台风