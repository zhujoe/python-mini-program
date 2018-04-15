from aip import AipOcr
import time
import json


def initID(id, api_key, secret_key):
    """ 百度 APPID AK SK """
    APP_ID = id
    API_KEY = api_key
    SECRET_KEY = secret_key

    return AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    """ 读取图片 """
    with open(filePath, 'rb') as fp:
        return fp.read()


def getImgWord_id(img, client):
    """ 提交并识别后返回任务 """
    image = get_file_content(img)

    """ 调用表格文字识别 """
    a = client.tableRecognitionAsync(image)
    # print('返回：', a)

    """ 获取id """
    return a['result'][0]['request_id']


def getresult_excel(requestId, client):
    """ 获取识别结果（可添加选项：excel / json） """
    options= {}
    options["result_type"] = "excel"

    """ 轮询状态 """
    while 1:
        """ 带参数调用表格识别结果 """
        re = client.getTableRecognitionResult(requestId, options)
        # print(re)
        time.sleep(1)
        if re['result']['ret_msg'] == '已完成':
            print('已完成，成功返回excel下载地址')
            return re['result']['result_data']


def getresult_json(requestId, client):
    """ 获取识别结果（可添加选项：excel / json） """
    options= {}
    options["result_type"] = "json"

    """ 轮询状态 """
    while 1:
        """ 带参数调用表格识别结果 """
        re = client.getTableRecognitionResult(requestId, options)
        # print(re)
        time.sleep(1)
        if re['result']['ret_msg'] == '已完成':
            print('已完成,成功返回json数据')
            with open('re.json', 'w') as f:
                json.dump(re, f)
            return re['result']['result_data']


if __name__ == '__main__':
    my = initID('11077532', 'HCFcUeTHkRKlHCRxKL2Q1ve1', 'PDVS2VCOvs1Gmt3YIxhHMVQGHbY5lE9l')
    id = getImgWord_id('2018.jpg', my)
    re_excel = getresult_excel(id, my)
    re_json = getresult_json(id, my)
    print(re_excel)
    print(re_json)
