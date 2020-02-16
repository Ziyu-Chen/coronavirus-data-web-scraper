import requests
import json
from bs4 import BeautifulSoup

def index():
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }
    response = requests.get('https://www.zhihu.com/special/19681091/trends#map', headers=headers)
    response.encoding = 'utf-8'
    text = response.text
    # Get timestamp
    timestamp = get_string('"deadline":"', text)
    print(timestamp)

    # Get oversea data
    oversea = get_array('"overseasList":', text)
    print(oversea)

    # Get domestic data
    domestic = get_array('"domesticList":', text)
    print(domestic)
    
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



if __name__ == '__main__':
    index()