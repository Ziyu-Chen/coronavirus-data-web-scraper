import requests
import json
import pandas as pd

# Replace it with the path of the folder that contains this project.
path = '/Users/ZiyuChen/assignment/'

def index():
    
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    # Get data from https://www.zhihu.com/special/19681091/trends#map
    response = requests.get('https://www.zhihu.com/special/19681091/trends#map', headers=headers)
    response.encoding = 'utf-8'
    text = response.text

    # Get timestamp
    timestamp = get_string('"deadline":"', text)

    # Get oversea data
    foreign_countries = get_array('"overseasList":', text)
    foreign_countries_df = pd.DataFrame(foreign_countries)[['name', 'conNum', 'cureNum', 'deathNum', 'susNum']]
    foreign_countries_df.columns = ['国家', '累计确诊人数', '治愈人数', '死亡人数', '疑似病例']
    foreign_countries_df.to_csv(path + '疫情实时动态爬虫/外国数据（国别）/' + timestamp + '.csv')

    # Get domestic data
    provinces = get_array('"domesticList":', text)

    # Unravel domestic data
    cities = unravel(provinces)
    cities_df = pd.DataFrame(cities)[['province_name', 'name', 'conNum', 'cureNum', 'deathNum', 'susNum']]
    cities_df.columns = ['省', '市', '累计确诊人数', '治愈人数', '死亡人数', '疑似病例']
    cities_df.to_csv(path + '疫情实时动态爬虫/中国数据（市别）/' + timestamp + '.csv')


def get_string(signal, text):
    start = text.index(signal) + len(signal)
    end = text.index('"', start)
    return text[start:end]


def get_array(signal, text):
    start = text.index(signal) + len(signal)
    count = 1
    for i in range(start+1, len(text)):
        if text[i] == '[':
            count += 1
        elif text[i] == ']':
            count -= 1
        if count == 0:
            return json.loads(text[start:i+1])


def unravel(provinces):
    store = []
    for province in provinces:
        province_name = province['name']
        cities = province['cities']
        for city in cities:
            city['province_name'] = province_name
        store += cities
    return store


if __name__ == '__main__':
    index()
