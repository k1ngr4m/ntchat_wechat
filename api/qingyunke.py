import requests


def get_reply(msg):
    url = f'https://api.qingyunke.com/api.php?key=free&appid=0&msg={msg}'
    response = requests.get(url).json()['content']
    res = response.replace('{br}', '\n')
    return res
