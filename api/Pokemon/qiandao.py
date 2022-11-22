import requests


class QiandaoApi:
    def __init__(self):
        self.url = 'https://api.qiandao.cn'

    def search_info_classify(self, msg):
        pass

    def search_pokemon_by_name(self, name):
        api_request = f'/plast/search/spu?q={name}'
        url = self.url + api_request
        response = requests.get(url).json()
        print(response)

    def get_pokemon_simpleInfo(self):
        api_request = '/treasure/spus/search/simple-info'
        url = self.url + api_request

        para = {
            'andTagIds': ["1416052"],
            'limit': 100,
            'offset': 0,
            'orderBy': 'latest',
            'propertyIds': ["55407"]
        }

        response = requests.post(url, params=para).json()
        print(response)


if __name__ == '__main__':
    qd = QiandaoApi()
    qd.search_pokemon_by_name('海豚侠')
    spuid = "523498484079480168"
    qd.get_pokemon_simpleInfo()
