#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2019/7/17 下午2:50
#@Author : guozhenhua
#@Site : 
#@File : stress_student.py
#@Software: PyCharm

import websocket
import time, os, sys
from requestMethod import RunMethod
import urllib.parse
import threading, json
import requests

domain = 'qaaiclass1.knowbox.cn/api'
version = '2.2.0'

request_send = RunMethod()

answerCount = {}

messageLock = True


def on_message(ws, message):
    global answerCount
    print(message)
    data = json.loads(message)
    push_1100 = '{"uuid":null,"action":1111}'

    ws.send(push_1100)

    if 5071 == data['action']:
        push_1101='{"uuid":null,"action":1101,"params":{"courseId":"9171690484870656","nodeId":"3947","aiCourseId":"377"}}'

        #push_anwser = ' {"uuid":null,"action":1110,"data":{"questionId":3264,"difficulty":2,"answer":"A","isRight":1,"timeUsed":2147483647,"isTimeout":1,"showType":21,"blankTotal":-1,"blankRight":-1}}'
        for i in range(1,100):
            #t = threading.Thread(target=ws.send, args=(push_1101,))
            #t.start()
            ws.send(push_1101)

            print(message)
            #ws.send(push_1100)

            # if 5116 == data['action'] :
        #
        #    push_anwser='{"action":1116,"data":{"choice":"A","isRight":1}}'
        #    ws.send(push_anwser)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    # 进入班级上课
    def run():
        time.sleep(1)
        #print("socket is ok !")
        # 点击上课
        #start_class = '{"action":1012,"params":{"courseId":8611836801318400},"data":{}}'
        # 请求初始白板数据
        #in_classroom = '{"action":1015,"param":{},"data":{}}'

        #ws.send(start_class)
        # print(start_class)

        # print("学生" + mobile + "收到的消息是 %s" % ws.recv())

        #time.sleep(1)

        #ws.send(in_classroom)

    t = threading.Thread(target=run)
    t.start()


def start_test(mobile, classId):
    # 学生端登陆
    return_data = login_user_student(mobile)
    print(return_data)

    if return_data['code'] == 0:

        student_token = return_data['data']['token']
        # print(student_token)
        encode_studnet_token = urllib.parse.quote(student_token)


        SERVER_URL = "wss://" + domain + "/ws/student?token=" + encode_studnet_token + "&sid=9171752533831168&version=" + version + "&from=client&miniClassNumber=" + classId
        print(SERVER_URL)

        ws = websocket.WebSocketApp(SERVER_URL,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever(ping_interval=30, ping_timeout=5)

        time.sleep(0.5)
    else:
        print("该手机号登陆失败 返回错误信息：%s" % mobile + str(return_data))


# 登陆接口
def login_user_student(mobile):
    url = 'https://' + domain + '/student/login?version=2.2.0'
    print(url)
    data = 'mobile=' + mobile + '&password=123456&system=mac&platform=web'

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return_data = requests.post(url=url, headers=headers, data=data).json()

    return return_data


if __name__ == "__main__":
    # 线程数，相当于多少个学生在线上课
    os.system('rm -fr msg_recv.txt')

    # classId = sys.argv[1]
    # mobilePrefix = sys.argv[2]
    # start = int(sys.argv[3])
    # end = int(sys.argv[4])

    classId = "9171768247528960"
    mobile = "13099988801"
    t = threading.Thread(target=start_test, args=(mobile, classId,))
    t.start()

    #
    # for ir in range(start,end):
    #
    #    	time.sleep(0.1)
    #
    #     #print("开始学生个数%d" % ir)
    #     if ir < 10:
    #             mobile = mobilePrefix+"000000" + str(ir)
    #             t = threading.Thread(target=start_test, args=(mobile,classId,))
    #             t.start()
    #
    #     elif ir < 100:
    #         mobile = mobilePrefix + "00000" + str(ir)
    #         t = threading.Thread(target=start_test, args=(mobile,classId,))
    #         t.start()
    #
    #     elif ir < 1000:
    #         mobile = mobilePrefix + "0000" + str(ir)
    #         t = threading.Thread(target=start_test, args=(mobile,classId,))
    #         t.start()
    #
    #     else:
    #         mobile = mobilePrefix + "000" + str(ir)
    #         t = threading.Thread(target=start_test, args=(mobile, classId,))
    #         t.start()
    #
