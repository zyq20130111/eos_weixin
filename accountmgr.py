#/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
from config import Config
from text import Text
from logger import Logger

class EosAccount(object):
    def __init__(self,name,eos_name,demo):
        self.name = name
        self.eos_name = eos_name;
	self.demo = demo

  
class AccountMgr(object):

    __instance = None

    def __init__(self):
       pass
    
    def __new__(cls, *args, **kwargs):
       if not AccountMgr.__instance:
           AccountMgr.__instance = object.__new__(cls,*args, **kwargs)
       return AccountMgr.__instance

    def Instance(self):
        return AccountMgr.__instance 
   
    def Init(self):
        self.initAccounts(); 
     
    def initAccounts(self):

        Logger().Log("initAccounts")
        self.accounts = {}
        self.eosaccounts = {}

        try:
             db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
	     cursor = db.cursor()
	     cursor.execute("SELECT * FROM weixin_tbl")

             for row in cursor.fetchall():

                  account = EosAccount(row[1],row[2],row[3])
                  
                  if(not self.accounts.has_key(row[1])):
                     self.accounts[row[1]] = []
                  
                  self.accounts[row[1]].append(account)
                                    
                  if(not self.eosaccounts.has_key(row[2])):
                     self.eosaccounts[row[2]] = []

                  self.eosaccounts[row[2]].append(account)

        except:
            Logger().Error(Text.TEXT3)

    def getWeiXinId(self,eosname):

        if(self.eosaccounts.has_key(eosname)):
           return self.eosaccounts[eosname]
        else:
           return None 

    def getAccountStatus(self,name,eos_name,demo):
         
         account = EosAccount(name,eos_name,demo)
         if(not self.accounts.has_key(name)):
              self.accounts[name] = []

         for eos in self.accounts[name]:
               if eos.eos_name == eos_name:
                  Logger().Log(Text.TEXT39)
                  return -1

         if(len(self.accounts[name]) == Config.EOSCOUNTINWEIXIN):
              Logger().Log(Text.TEXT1)
              return -2

         if(not self.eosaccounts.has_key(eos_name)):
              self.eosaccounts[eos_name] = []

         if(len(self.eosaccounts[eos_name]) == Config.WEIXINCOUNTINEOS):
              Logger().Log(Text.TEXT2)
              return -3


         return 0
        
    def AddAccount(self,name,eos_name,demo):
         
         Logger().Log(Text.TEXT8)
         try:

              db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
              cursor = db.cursor()
              sql = "INSERT INTO weixin_tbl(name,eos_name, demo)VALUES ('%s','%s','%s')" %(name,eos_name,demo)
              
              cursor.execute(sql)
              db.commit()
               
              self.accounts[name].append(account) 
              self.eosaccounts[eos_name].append(account)
              
              cursor.close()
              db.close()
              
              Logger().Log(Text.TEXT5)
         except:
              Logger().Error(Text.TEXT4)
       
   
    def delAccount(self,name):
       
        try:
            Logger().Log(Text.TEXT6)

            db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
            cursor = db.cursor()
            sql = "DELETE FROM  weixin_tbl where name ='%s'" %(name)

	    cursor.execute(sql)
            db.commit()

            #删除账户所对应的weixin号
            for eos in self.accounts[name]:
               
               i = - 1
               eos_name = eos.eos_name              
               
               for eos1  in self.eosaccounts[eos_name]:
                     
                     i = i + 1 
                     if(eos1.name == name):
                          self.eosaccounts[eos_name].pop(i)   
            
            #删除微信号所对应的Eos账号
            del self.accounts[name]

            cursor.close()
            db.close()

        except:
            Logger().Error(Text.TEXT7)
      
       

