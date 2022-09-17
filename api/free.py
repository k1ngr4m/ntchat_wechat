

import requests

from base.base import BaseFunc


class FreeApi(BaseFunc):
    # 随机狗狗照片
    def random_dog(self):
        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url).json()
        pic_url = response['message']
        return self.pic(pic_url, 'temp')

    # 随机猫猫照片
    def random_cat(self):
        url = 'https://api.thecatapi.com/v1/images/search?api_key=live_KcFizldcZepQ5GCYohanKDemRK9AVqQGcst4RDF9xrzXIUMtr3Oj7HjXt82i9yT2&breed_id=amis'
        response = requests.get(url).json()
        pic_url = response[0]['url']
        print(pic_url)
        return self.pic(pic_url, 'temp')

