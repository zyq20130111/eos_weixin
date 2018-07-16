#/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import requests
import json

from config import Config  

class BlockInfo(object):
    def __init__(self):
         self.trxs = []

    def addTrx(self,trx):
         self.trxs.append(trx)

class Transaction(object):
    def __init__(self):
         self.trx_id = 0
         self.actions= []

    def addAction(self,action):
         self.actions.append(action)

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
           self.block_num_id = self.block_num_id + 1
           time.sleep(0.01)
           self.getBlockInfo(self.block_num_id)

    def Start(self):

         self.block_num_id = 4000000     
         t =threading.Thread(target=self.threadFun,args=(1,))
         t.setDaemon(True)#设置线程为后台线程
         t.start()

    def parseBlock(self,blockJson):
       
        block = BlockInfo()        
        if("transactions" in blockJson):
              print '-----------------'
              print 'in transations'
              for trx in blockJson["transactions"]:
                  trxObj =  self.parseTransaction(trx)
                  block.addTrx(trxObj)
        else:
            print 'not exsit transaction'
        return block

    def parseTransaction(self,trxJson):
        trx = Transaction()
        if("trx" in trxJson):
           print '------------------'
           print 'trx'
           if("transaction" in trxJson["trx"]):
              print '----------------'
              print 'in transaction'
              if("actions" in trxJson["trx"]["transaction"]):
                  print '-------------'
                  print 'actions'
                  for actionJson in trxJson["trx"]["transaction"]["actions"] :
                         act =  self.parseAction(actionJson)
                         trx.addAction(act)

        return trx       
         
    
    
    def parseAction(self,actionJson):
        print actionJson["account"]
        print actionJson["name"]
        print actionJson["data"]
        action = Action(actionJson["account"],actionJson["name"],actionJson["data"])
        return action;

    def getBlockInfo(self,blockid):

        headers = {'content-type': "application/json"}
        url = Config.HTTP_URL + "get_block"
        
        try:
             r = requests.post(url,data =json.dumps({"block_num_or_id":blockid}),headers = headers);
             if( r.status_code == 200):
                 js = json.loads(r.text)
                 print '-------------------------'
                 #print r.text
                 return self.parseBlock(js)
             else:
                 return None
        except:
             print 'request error'

    
    def sendMsg(self):
        
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

      
