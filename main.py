# -*- coding: utf-8 -*-
# filename: main.py
import web
import threading
import time

from config import Config
from menu import Menu
from handle import Handle
from basic import Basic
from blockmonitor import BlockMgr
from accessmgr import AccessMgr
from accountmgr import AccountMgr
from logger import Logger
import sys

urls = (
    '/wx', 'Handle',
)



def createMenu():

    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "开发指引",
                "key":  "mpGuide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            }
          ]
    }
    """
    accessToken = AccessMgr().Instance().getToken()
    print  "accesstoken", accessToken
   # myMenu.delete(accessToken)
   # myMenu.create(postJson, accessToken)


if __name__ == '__main__':

    #reload(sys)
    #sys.setdefaultencoding("ascii")
    createMenu()
    Logger().Init()
    AccountMgr().Instance().Init()
    BlockMgr().Instance().Start()
    app = web.application(urls, globals())
    app.run()
