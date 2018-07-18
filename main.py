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
    print accessToken
   # myMenu.delete(accessToken)
   # myMenu.create(postJson, accessToken)


if __name__ == '__main__':

    createMenu()


    BlockMgr().Instance().Start()
    BlockMgr().Instance().sendTransertMsg("test","oMywO0033f8U-P7kvBvfxbEOE7g8","oMywO0033f8U-P7kvBvfxbEOE7g8","200")
    app = web.application(urls, globals())
    app.run()
