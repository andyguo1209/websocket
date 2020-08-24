#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@Time : 2019/3/26 下午4:17
#@Author : guozhenhua
#@Site : 
#@File : 有心跳学生端.py
#@Software: PyCharm
import websocket
import time,os,sys
from requestMethod import RunMethod
import urllib.parse
import threading,json

domain = 'aiclass.knowbox.cn/api'
version = '2.2.0'

request_send=RunMethod()

answerCount = {}

messageLock = True

def on_message(ws, message):

    global answerCount
    print(message)
    data = json.loads(message)
    
    if 5110 == data['action'] :
        
        #threadId = threading.currentThread().ident
        #if threadId not in answerCount:
        #    answerCount[threadId] = 0

        #totalCount = data['data']['total']
        #if answerCount[threadId] < totalCount :    
        time.sleep(2)
        questionid=data['data']['questionInfo']['questionId']
        push_anwser = '{"action":1110,"params":{},"data":{"questionId":'+(questionid)+',"difficulty":2,"answer":"http://download.cloud.chivox.com/5d070944ecca2bf11a07b5be.mp3","isRight":1,"timeUsed":7,"isTimeout":0,"showType":523,"blankTotal":-1,"blankRight":-1,"reciteWordAnswer":{"word":"kite","wordScore":100,"phoneList":[{"phone ":"k","phoneScore ":100},{"phone ":"ay","phoneScore ":100},{"phone ":"t","phoneScore ":100}]}}}'
        ws.send(push_anwser)
        # answerCount[threadId] += 1
        # print("push anwser. answer count " + answerCount[threadId])


    if 5111 == data['action'] :
        answerCount = {}

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    #进入班级上课
    def run():
	
        time.sleep(1)
	    #点击上课
        start_class = '{"action":1012,"params":{"courseId":8364585209115136},"data":{}}'
	    #请求初始白板数据
        in_classroom = '{"action":1015,"param":{},"data":{}}'

        ws.send(start_class)
        #print(start_class)

        #print("学生" + mobile + "收到的消息是 %s" % ws.recv())

        time.sleep(1)

        ws.send(in_classroom)

        #print("学生" + mobile + "收到的消息是 %s" % ws.recv())

        time.sleep(5)

        global messageLock
        push_msg = '{"action":1000,"params":{},"data":{"text": "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"}}'
        print(messageLock)
        if messageLock :
            messageLock = False
            while(1) :
                ws.send(push_msg)
                time.sleep(0.2)

                ws.send(push_msg)
                time.sleep(0.2)

                ws.send(push_msg)
                time.sleep(0.3)

                ws.send(push_msg)
                time.sleep(0.1)

                ws.send(push_msg)
                time.sleep(0.3)

    t = threading.Thread(target=run)
    t.start()


def start_test(mobile, classId):
    #学生端登陆
    return_data=login_user_student(mobile)
    #print(return_data)

    if return_data['code']==0:

        student_token =return_data['data']['token']
        #print(student_token)
        encode_studnet_token = urllib.parse.quote(student_token)
        SERVER_URL = "ws://"+domain+"/ws/student?token=" + encode_studnet_token + "&sid=8378473311884800&version="+version+"&from=client&miniClassNumber="+classId

        ws = websocket.WebSocketApp(SERVER_URL,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever(ping_interval=30, ping_timeout=5)

        time.sleep(0.5)
    else:
        print("该手机号登陆失败 返回错误信息：%s"  % mobile+str(return_data))

#登陆接口
def login_user_student(mobile):
    url = 'http://'+domain+'/student/login?version='+version
    data = {
        "mobile":mobile,
        "password":"123456",
        "system":"mac",
        "platform":"web",
        "version":version
        }
    #print(data)
    return_data = request_send.run_main('post', url, data)
    return json.loads(return_data)


if __name__ == "__main__":

    #线程数，相当于多少个学生在线上课
    os.system('rm -fr msg_recv.txt')

    classId = sys.argv[1]
    mobilePrefix = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    #classId = '8378799005844480'
    #mobilePrefix = '1770'
    #start = 1
    #end = 2

    for ir in range(start,end):

       	time.sleep(5)

        #print("开始学生个数%d" % ir)

        if ir > 9 and ir < 100:

            mobile = mobilePrefix+"00000" + str(ir)
            t = threading.Thread(target=start_test, args=(mobile,classId,))
            t.start()

        elif ir > 99 and ir < 1000:

            mobile = mobilePrefix + "0000" + str(ir)
            t = threading.Thread(target=start_test, args=(mobile,classId,))
            t.start()

        elif ir > 999:

            mobile = mobilePrefix + "000" + str(ir)
            t = threading.Thread(target=start_test, args=(mobile,classId,))
            t.start()

        else:

            mobile = mobilePrefix + "000000" + str(ir)
            t = threading.Thread(target=start_test, args=(mobile, classId,))
            t.start()

