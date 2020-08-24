#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2019/7/17 下午2:50
#@Author : guozhenhua
#@Site : 
#@File : stress_teacher.py
#@Software: PyCharm

import datetime
import  json
import urllib.parse
import websocket
import urllib
import time
from requestMethod import RunMethod
import requests


run=RunMethod()

domain = 'aiclass.knowbox.cn/api'
classId = '8611876113954816'
courseId = '8611836800269824'
version = '1.14.0.0-alpha'

def login_user():
    #登陆相关

    url = 'https://teacherlive.knowbox.cn/login.do'

    data = {
	"email": "jisy@knowbox.cn",
	"password": "123456",
	"rememberMe":"true"
    }
    headers = {'Content-Type': 'application/json'}

    return_data = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
    #print(return_data)
    return return_data

def start_class(token):

    url = 'https://'+domain+'/teacher/course/start?version=2.2.0&classNumber='+classId+'&courseLessonNumber='+courseId+'&sid='+classId

    print(url)
    headers = {'Content-Type': 'application/json', 'authorization':token}
    print(headers)
    return_data = requests.get(url=url, headers=headers).json()

    msg=return_data['msg']
    if msg=='success':
        return "success"
    else:
        return "fail"

try:
    import thread
except ImportError:
    import _thread as thread



def on_message(ws, message):
    #老师收到的消息
    #pass
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


def on_open(ws):


    def run(*args):

        n = 0

	#老师改变样式
        shangke = '{"action": 2071, "params": {"courseStyle": 0}, "data": {}}'
	#请求初始白板数据
        start_calss = '{"action": 2015, "param": {}, "data": {}}'
	#老师打开课堂
        dakaijiaoshi = '{"action": 2012, "params": {}, "data": {}}'
	#老师改变样式
        dakaijiaos2 = '{"action": 2071, "params": {"courseStyle": 0}, "data": {}}'

        ws.send(shangke)
        time.sleep(1)

        ws.send(start_calss)
        time.sleep(1)

        ws.send(dakaijiaoshi)
        time.sleep(1)

        ws.send(dakaijiaos2)

        time.sleep(15*60)

        board_msg = '{"action":2014,"data":{"text":"111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"}}'
        while(1):

            time.sleep(60)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            ws.send(board_msg)
            time.sleep(0.1)

            n = n + 1

            print("发送的消息条数 %d" % n)

            #ws.close()

    thread.start_new_thread(run,())

if __name__ == "__main__":

    # 生成token
    token = login_user()['data']
    #print(token)

    # 需要对返回的token进行urlencode
    encode_token = urllib.parse.quote(token)

    print('生成的token：%s' % encode_token)

    start_class_status = start_class(encode_token)


    print('开始上课: %s' % start_class_status)

    SERVER_URL = "wss://"+domain+"/ws/teacher?sid="+classId+"&classNumber="+classId

    #websocket.enableTrace(True)

    header = {'authorization':token}
    ws = websocket.WebSocketApp(SERVER_URL,header=header,
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)


    ws.on_open = on_open

    ws.run_forever(ping_interval=60,ping_timeout=10)