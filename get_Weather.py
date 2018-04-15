# This Python file uses the following encoding: utf-8

from bs4 import BeautifulSoup
import random
import requests
import socket
import time
import http.client
import csv


def get_html(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/63.0.3239.108 Safari/537.36'
    }

    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = "utf-8"
            break
        except socket.timeout as e:
            print("失败:", e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print("失败:", e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print("失败:", e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print("失败:", e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text


def get_data(html_txt):
    final = []
    bs = BeautifulSoup(html_txt, "html.parser")
    body = bs.body
    data = body.find("div", {"id": "7d"})
    ul = data.find("ul")
    li = ul.find_all("li")

    for day in li:
        temp = []

        # 获取日期
        date = day.find("h1").string
        temp.append(date)
        inf = day.find_all("p")
        temp.append(inf[0].string)

        # 获取7日天气
        if inf[1].find("span") is None:
            temperature_high = None
        else:
            temperature_high = inf[1].find("span").string
            temperature_high = temperature_high.replace("℃", "")
        temperature_lower = inf[1].find("i").string
        temperature_lower = temperature_lower.replace("℃", "")
        temp.append(temperature_high)
        temp.append(temperature_lower)
        final.append(temp)

    return final


def write_data(data, name):
    file_name = name
    with open(file_name, 'w', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


def read_data(name):
    file_name = name
    data = []
    with open(file_name, 'r') as f:
        f_csv = csv.reader(f)
        for i in f_csv:
            data.append(i)
    return data


def get_url(city_name):
    city = {"成都": "101270101"}
    city_num = city[city_name]
    weather_url = "http://www.weather.com.cn/weather/%s.shtml" % city_num
    return weather_url


if __name__ == "__main__":
    # url="http://www.weather.com.cn/weather/城市代码.shtml"
    url = get_url('成都')
    html = get_html(url)
    result = get_data(html)
    write_data(result, "weather.csv")
    data = read_data('weather.csv')
    print('成都天气:')
    for i in data:
        if i[2]:
            print('|日期|', i[0],
                  '|天气|', i[1],
                  '|温度|', i[2], '℃-', i[3], '℃')
        else:
            print('|日期|', i[0],
                  '|天气|', i[1],
                  '|温度|', i[3], '℃')
