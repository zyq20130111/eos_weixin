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

class EosRemind(object):
    def __init__(self,name,transfer,vote):
        self.name = name
        self.transfer = transfer
        self.vote = vote
  
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
        self.reminds = {}

        try:
             db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
	     cursor = db.cursor()
	     cursor.execute("SELECT * FROM weixin_tbl")
            
             #初始化weixin_tbl
             for row in cursor.fetchall():

                  account = EosAccount(row[1],row[2],row[3])
                  
                  if(not self.accounts.has_key(row[1])):
                     self.accounts[row[1]] = []
                 
                  self.accounts[row[1]].append(account)
                                    
                  if(not self.eosaccounts.has_key(row[2])):
                     self.eosaccounts[row[2]] = []

                  self.eosaccounts[row[2]].append(account)

             #初始化remind表
             
             cursor.execute("SELECT * FROM remind_tbl")
             for row in cursor.fetchall():

                  print row[1],row[2],row[3]
                  remind = EosRemind(row[1],row[2],row[3])
                  self.reminds[row[1]] = remind
 
             cursor.close()
             db.close()
            
        except:
            Logger().Error(Text.TEXT3)

    def getWeiXinId(self,eosname):
        if(self.eosaccounts.has_key(eosname)):
           return self.eosaccounts[eosname]
        else:
           return None

    def getAccounts(self,name):
        
        if(self.accounts.has_key(name)):
           return self.accounts[name]
        else:
           return None

    def getRemind(self,name):

        if(self.reminds.has_key(name)):
           return self.reminds[name]
        else:
           return None         

    def getAccountStatus(self,name,eos_name,demo):
         
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
    
    
    def sql_inj(self,name):
      
       inj_str = "'|and|exec|insert|select|delete|update|count|*|%|chr|mid|master|truncate|char|declare|;|or|-|+|,|drop"
       inj_stra = inj_str.split("|")
      
       for word in inj_stra:
          if(word == name.lower()):
             return True;

       return False;

    
    def AddAccount(self,name,eos_name,demo):
         
         Logger().Log(Text.TEXT8)
         if(self.sql_inj(name) or self.sql_inj(eos_name) or self.sql_inj(demo)):
            Logger().Log("addaccount 非法的sql语句注入")
            return

         try:
              account = EosAccount(name,eos_name,demo)

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
       
 
    def delAccount(self,name,account):
       
        try:
            Logger().Log(Text.TEXT6)

	    if(self.sql_inj(name) or self.sql_inj(account)):
               Logger().Error("delAccount 非法的SQL语句注入")
               return 

            db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
            cursor = db.cursor()
            sql = "DELETE FROM  weixin_tbl where name ='%s' and eos_name = '%s'" %(name,account)

	    cursor.execute(sql)
            db.commit()

            #删除微信号队应的账号
            i = 0
            for eos in self.accounts[name]:
                            
               if(eos.eos_name == account):
                  self.accounts[name].pop(i)

               i = i + 1

            #删除账号所对应的微信号
            i = 0
            for eos1  in self.eosaccounts[account]:
                     
                 if(eos1.name == name):
                     self.eosaccounts[account].pop(i)   
                 i = i + 1

            cursor.close()
            db.close()

        except:
            Logger().Error(Text.TEXT7)
      
       
    def delWeiXin(self,name):

        try:
            Logger().Log(Text.TEXT54)

            if(self.sql_inj(name)):
               Logger().Error("delAccount 非法的SQL语句注入")
               return

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

            #删除微信号所对应的设置            
            sql = "DELETE FROM  remind_tbl where name ='%s'" %(name)
            cursor.execute(sql)
            db.commit()
            del self.reminds[name]

            cursor.close()
            db.close()

        except:
            Logger().Error(Text.TEXT55)

    def AddRemind(self,name,transfer,vote):

         
         print(Text.TEXT61)
         if(self.sql_inj(name) or self.sql_inj(str(transfer)) or self.sql_inj(str(vote))):
            Logger().Log("addremind 非法的sql语句注入")
            return

         try:
              
              remind = EosRemind(name,transfer,vote)
              db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
              cursor = db.cursor()
              
              sql = "SELECT * FROM remind_tbl where name ='%s'" %(name)
              cursor.execute(sql)
               
              
              cursor.fetchall() 
              if(cursor.rowcount <= 0):
                  sql = "INSERT INTO remind_tbl(name,tranfer, vote)VALUES ('%s',%d,%d)" %(name,transfer,vote)
              else:
                  sql = "update remind_tbl SET tranfer=%d,vote=%d where name = '%s'" %(transfer,vote,name)
              
              
              cursor.execute(sql)
              db.commit()

              self.reminds[name] = remind

              cursor.close()
              db.close()

              Logger().Log(Text.TEXT62)
         except:
              Logger().Error(Text.TEXT63)
