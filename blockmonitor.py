#/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import requests
import json

from config import Config  

class BlockInfo(object):
    def __init__(self):
         self.trxs = {}

    def addTrx(self,trx):
         self.trx.append(trx)

class Transaction(object):
    def __init__(self,trx_id):
         self.trx_id = trx_id
         self.actions= {}

    def addAction(self,action):
         self.actions.add(action)

class Action(object):
    def __init__(self,account,name,data):
         self.account = account 
         self.name    = name
         self.data    = data

class BlockMgr(object):

    __instance = None

    def __init__(self):
       pass
     
    def __new__(cls, *args, **kwargs):
       if not BlockMgr.__instance:
           BlockMgr.__instance = object.__new__(cls,*args, **kwargs)
       return BlockMgr.__instance

    def Instance(self):
        return BlockMgr.__instance

    def threadFun(self,arg):
       while(True):
           time.sleep(1)
           self.getBlockInfo(2000)

    def Start(self):

         self.block_num_id = 100     
         t =threading.Thread(target=self.threadFun,args=(1,))
         t.setDaemon(True)#设置线程为后台线程
         t.start()

    def pareBlock(self,blockJson):
       
        block = self.BlockInfo()        
        if("transactions" in js):
              for trx in js["transactions"):
                  trxObj =  self.parseTransaction(trx)
                  block.addTrx(trxObj)
        else:
            print 'not exsit transaction'

    def parseTransaction(self,trxJson):
        trx = Transaction()
        if("trx" in trxJson):
           if("transaction" in trxJson["trx"]):
              if("actions" in trxJson["trx"]["transaction"]):
                  for actionJson in trxJson["trx"]["transaction"]["actions"]
                         act =  self.parseAction(actionJson)
                         trx.addAction(act)

         return trx       
         
    
    
    def parseAction(self,actionJson):
        action = Action()
        return action;

    def getBlockInfo(self,blockid):

        headers = {'content-type': "application/json"}
        url = Config.HTTP_URL + "get_block"
        r = requests.post(url,data =json.dumps({"block_num_or_id":blockid}),headers = headers);
        if( r.status_code == 200):
           js = loads(r.text)
           return self.parseBlock(js)
        else:
           return None


    def getInfo(self):

        headers = {'content-type': "application/json"}
        url = Config.HTTP_URL + "get_info"
        r = requests.get(url)

	if(r.status_code == 200):

       	    js = json.loads(r.text)

            if("head_block_num" in js): 
               print js['head_block_num']
               return js['head_block_num'];
            else:
               print 'not exsit key'
               return -1
        else:
            print r.text

      
