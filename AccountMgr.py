#/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
from config import Config

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

        self.accounts = {}

        db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
        try:
	     cursor = db.cursor()
	     cursor.execute("SELECT * FROM weixin_tbl")

             for row in cursor.fetchall():

                  account = EosAccount(row[1],row[2],row[3])
                  self.accounts[row[1]] =  account

        except:
             db.rolllback() 

    def AddAccount(self,name,eos_name,demo):

       if(self.accounts.has_key(name) == False):       
           
           db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
           cursor = db.cursor()
           sql = "INSERT INTO weixin_tbl(name,eos_name, demo)VALUES ('%s','%s','%s')" %(name,eos_name,demo)

           try:
              cursor.execute(sql)
              db.commit()
              account = EosAccount(name,eos_name,demo)
              self.accounts[name] = account
           except:
              db.rollback()
       
           cursor.close()
           db.close()

       else:
           print 'addaccount name is exsit'
   
    def delAccount(self,name):
       
        if(self.accounts.has_key(name)):

            db = MySQLdb.connect(Config.DB_SERVER, Config.DB_USER, Config.DB_PWD, Config.DB_NAME, charset='utf8' )
            cursor = self.db.cursor()
            sql = "DELETE FROM  weixin_tbl where name ='%s'" %(name)
            try:
	        cursor.execute(sql)
                db.commit()
                del self.accounts[name]
            except:
                db.rollback()
      
            cursor.close()
            db.close()
       
        else:
             print 'delAccount account isnot exsit'

if __name__ == '__main__':
     AccountMgr().Instance().Init()
     AccountMgr().Instance().AddAccount("111","eosgalaxybp1","13")
     AccountMgr().Instance().AddAccount("222","eosgalaxybp2","23")
     AccountMgr().Instance().AddAccount("222","eosgalaxybp2","23")
