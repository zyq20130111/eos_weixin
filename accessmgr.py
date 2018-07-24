#/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import requests
import json
import MySQLdb
from config import Config
from logger import Logger
import sys
from text import Text

class AccessMgr(object):

    __instance = None

    def __init__(self):
       pass
     
    def __new__(cls, *args, **kwargs):
       if not AccessMgr.__instance:
           AccessMgr.__instance = object.__new__(cls,*args, **kwargs)
       return AccessMgr.__instance

    def Instance(self):
        return AccessMgr.__instance

    def sql_inj(self,name):

       inj_str = "'|and|exec|insert|select|delete|update|count|*|%|chr|mid|master|truncate|char|declare|;|or|-|+|,|drop"
       inj_stra = inj_str.split("|")

       for word in inj_stra:
          if(word == name.lower()):
             return True;

       return False;
 
    def getToken(self):

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" %(Config.APP_ID, Config.APP_SECRET)) 
        try:
             db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
             cursor = db.cursor()
             cursor.execute("SELECT * FROM access_tbl;")
             if(cursor.rowcount > 0):
        
                  Id = 0
                  token = ""
                  token_time = 0
                  token_expire =0
		  
                  for row in cursor.fetchall():
                       Id  =  row[0]
                       token = row[1]
                       token_time = row[2]
                       token_expire = row[3]
                  
                  if(time.time() < token_time + 0.9 * token_expire ):
                      return token
                  else:
          	     
                      try:
                         r = requests.get(postUrl)
         
                         if(r.status_code == 200):
                              
                              urlResp = json.loads(r.text)
                              if(self.sql_inj(urlResp['access_token']) or self.sql_inj(str(urlResp['expires_in']))):
                                  Logger().Error("update access_tbl 非法的sql注入")
                                  return 
          
                              sql = "update  access_tbl set token='%s' , token_time=%d ,token_expire=%d where Id =%d" %(urlResp['access_token'],time.time(),urlResp['expires_in'],Id)
                              cursor.execute(sql)
                              db.commit()   
                              Logger().Log("update access_tbl success")  
                              return urlResp['access_token'] 
                         else:
                              return None 
                     
                      except:
                         Logger().Error('update access_tbl error')
                         return None
             else:
                 try:
                     r = requests.get(postUrl)
                     urlResp = json.loads(r.text)
                     if(r.status_code == 200):


                         if(self.sql_inj(urlResp['access_token']) or self.sql_inj(str(urlResp['expires_in']))):
                              Logger().Error("update access_tbl 非法的sql注入")
                              return

                         sql = "INSERT INTO access_tbl(token,token_time,token_expire) VALUES('%s',%d,%d)" %(urlResp['access_token'],time.time(),urlResp['expires_in'])  
                         cursor.execute(sql)
                         db.commit()

                         Logger().Log(Text.TEXT31)
                         return urlResp['access_token']
                     else:
                         return None
                 except:
                     Logger().Error(Text.TEXT30)
                     return None

             cursor.close()
             db.close()
        except:
               return None 

