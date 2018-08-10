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
                "name": "关于我们",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "官网",
                        "url": "http://www.eosgalaxy.io"
                    },
                    {
                       "type": "click",
                       "name": "加入社区",
                       "key":  "join"
                    }
                ]
            },
            {
                "type": "view",
                "name": "EOS投票",
                "url":  "http://www.huoxing24.com/newsdetail/20180712195305691775.html"
            },
            {
                "name": "账号查询",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "绑定EOS账号",
                        "key": "bind"
                    },
                    {
                        "type": "click",
                        "name": "解绑EOS账号",
                        "key": "unbind"
                    },                    
                    {
                        "type": "click",
                        "name": "查询EOS账号",
                        "key": "find"
                    },
                    {
                        "type": "click",
                        "name": "EOS提醒设置",
                        "key": "set"
                    }
                ]
            }
          ]
    }
    """
    accessToken = AccessMgr().Instance().getToken()
    print  "accesstoken", accessToken
    myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)


if __name__ == '__main__':

    Logger().Init()
    createMenu()
    AccountMgr().Instance().Init()
    BlockMgr().Instance().Start()
    app = web.application(urls, globals())
    app.run()
