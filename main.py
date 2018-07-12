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

urls = (
    '/wx', 'Handle',
)

def action(arg):

    while(True):
        time.sleep(1)
        print  'the thread name is:%s\r' % threading.currentThread().getName()


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
    accessToken = Basic().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)


if __name__ == '__main__':

    createMenu()

    t =threading.Thread(target=action,args=(1,))
    t.setDaemon(True)#设置线程为后台线程
    t.start()
    BlockMgr().Instance().Start()
    app = web.application(urls, globals())
    app.run()
