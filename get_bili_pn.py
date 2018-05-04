import requests
from bs4 import BeautifulSoup as bs
import time
import json
import msvcrt
import matplotlib.pyplot as plt


def kbfunc():
    x = msvcrt.kbhit()
    if x:
        ret = ord(msvcrt.getch())
    else:
        ret = 0
    return ret


flg = 1
num = 0
all_count = []
web_online = []
times = []

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

print('## 此间按任意按键退出，并生成统计图和统计文件 ##')
while flg == 1:
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
    times.append(timenow)
    all_count.append(jsondata['data']['all_count'])
    web_online.append(jsondata['data']['web_online'])
    num += 1
    print('在线人数：' + str(web_online[-1]) +
          '\n一星期内总投稿数：' + str(all_count[-1]) +
          '\n------------------------------------------')

    # 取值间隔
    for i in range(step):
        r = kbfunc()
        if r != 0:
        # if flg ==1:
            print('## 停止收集数据，生成图和文件中。。。。。 ##')
            flg = 0
        time.sleep(1)

# print(times)
# print(all_count)
# print(web_online)
# print(num)

with open('loge.txt', 'w') as f:
    for i in range(num):
        f.write('num:'+str(i+1))
        f.write('\t'+ str(times[i]))
        f.write('\t一周内投稿数：'+str(all_count[i]))
        f.write('\t在线人数：' + str(web_online[i]) + '\n')
    f.write('总数据量：'+str(num))

print('数据文件在本路径生成完毕！名字是：loge.txt')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
ax = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax.plot(web_online)
ax2.plot(all_count)
ax.set_title('在线人数')
ax2.set_title('投稿数')
plt.show()
