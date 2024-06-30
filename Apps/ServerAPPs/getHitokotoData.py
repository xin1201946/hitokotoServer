import requests

version = '1.0.393'
F_url = f'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@{version}/sentences/'

try:
    for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
        D_URL = F_url + i + '.json'
        data = requests.get(D_URL)
        path = f'./DATA/{i}.json'
        with open(path, 'w',encoding='utf-8') as file:
            file.write(data.text)
    print('DONE!')
except Exception as e:
    print('A Error in \n', e)
