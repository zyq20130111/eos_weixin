# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import web
from  logger import Logger
from text import Text

class Action(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"

            openid  = data.openid
            return openid

        except Exception, Argument:
            return '{"code":-1}'