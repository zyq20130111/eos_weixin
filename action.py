# -*- coding: utf-8 -*-
# filename: handle.py
import MySQLdb
import hashlib
import web

from  logger import Logger
from  accountmgr import AccountMgr
from text  import Text
from config import Config

class Action(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"

            db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )

            cursor = db.cursor()
            print data.openid
            print data.user

            #openid = data.openid
            #user = data.user
            
            #return openid
           
            #sql = "SELECT * FROM order_tbl where open_id ='%s' and username = '%s'" %(openid,account)
            #cursor.execute(sql)

            #cursor.fetchall()
            #if(cursor.rowcount > 0):
               #AccountMgr().Instance().AddAccount(openid,account,"demo")                    

            #cursor.close()
            #db.close()

            return "aaaa" 

        except Exception, Argument:
            return 'bbbb'
