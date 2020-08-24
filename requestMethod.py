#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@Time : 2019/7/17 下午2:49
#@Author : guozhenhua
#@Site : 
#@File : requestMethod.py
#@Software: PyCharm

import requests
import json

class RunMethod:
    header = {
        'User-Agent': 'self-defind-user-agent',
        'Cookie': 'name=self-define-cookies-in header',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    def post_main(self,url,data,header=None):
        res=None
        if header == None:
            res=requests.post(url=url,data=data).json()
        else:
            res=requests.post(url=url,data=data,header=header).json()
        return res
    def get_main(self,url,data=None,header=None):
        res=None
        if header==None:
            res=requests.get(url=url,data=data).json()
        else:
            res=requests.get(url=url,data=data,header=header).json()

        return  res
    def run_main(self,method,url,data=None,header=None):
        if method=="get":
            res=self.get_main(url,data,header)
        else:
            res=self.post_main(url,data,header)
        return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)


if __name__ == '__main__':

    url = "http://qaaicms.knowbox.cn/api/oc/user/add?token=21c2e59531c8710156d34a3c30ac81d5"

    data = {
        "actor": 2,
        "userName": "郭郭老师",
        "mobile": 13810697234
    }
    run=RunMethod()


    res=run.run_main("post",url,data)
    print(res)


