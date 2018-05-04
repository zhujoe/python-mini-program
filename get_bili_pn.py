import requests
from bs4 import BeautifulSoup as bs
import time
import json

step = input('输入我检测数据的时间间隔（单位：秒）:')
step = int(step)

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'sid=8mnjcgif; buvid3=1FA572EB-D969-4049-8B34-27E9549B2676188737infoc; UM_distinctid=1618db679ee94-06d2071ac5f218-3c60460e-144000-1618db679ef118; fts=1518501002; rpdid=oqmmwqimkodosoqswowww; finger=edc6ecda; CURRENT_QUALITY=0; LIVE_BUVID=f73dc4d76759a82060d9b7b773020cec; LIVE_BUVID__ckMd5=0965e40f8f9553f5',
    'DNT': '1',
    'Host': 'api.bilibili.com',
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

while True:
    ticks = time.time()
    timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ticks))
    ticks = ticks*1000
    print(timenow)
    print('时间戳：', str(int(ticks)))
    url = 'http://api.bilibili.com/x/web-interface/online?callback=jqueryCallback_bili_2&jsonp=jsonp&_='+ str(int(ticks)) + ' HTTP/1.1'
    try:
        html = requests.get(url, timeout=120, headers=headers).content
    except:
        print('这次访问，bilibili没有搭理我，我2秒后再试 =_=|')
        time.sleep(2)
        continue
    data = bs(html, 'html5lib')
    jsondata = json.loads(data.body.text[22:-1])
    # print(jsondata)
    all_count = jsondata['data']['all_count']
    web_online = jsondata['data']['web_online']
    print('在线人数：' + str(web_online) +
          '\n一星期内总投稿数：' + str(all_count) +
          '\n------------------------------------------')

    # 取值间隔
    time.sleep(step)
