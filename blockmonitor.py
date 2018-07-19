#/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import requests
import json

from accessmgr import AccessMgr
from config import Config  
from logger import Logger
from text  import Text

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

         self.block_num_id = 1000000     
         t =threading.Thread(target=self.threadFun,args=(1,))
         t.setDaemon(True)#设置线程为后台线程
         t.start()

    def parseBlock(self,blockJson):
        
        Logger().Log(Text.TEXT27)       
        block = BlockInfo()        
        if("transactions" in blockJson):
              for trx in blockJson["transactions"]:
                  trxObj =  self.parseTransaction(trx)
                  block.addTrx(trxObj)
        else:
            Logger().Log('not exsit transaction')
        return block

    def parseTransaction(self,trxJson):

        Logger().Log(Text.TEXT28)
        trx = Transaction()
        if("trx" in trxJson):
           if("transaction" in trxJson["trx"]):
              if("actions" in trxJson["trx"]["transaction"]):
                  for actionJson in trxJson["trx"]["transaction"]["actions"] :
                         act =  self.parseAction(actionJson)
                         trx.addAction(act)

        return trx       
         
    
    
    def parseAction(self,actionJson):
        
        Logger().Log(Text.TEXT29)
        action = Action(actionJson["account"],actionJson["name"],actionJson["data"])

        if(action.account == "eosio.token" and action.name == "transfer"):

            toaccount = action.data["to"]
            frmaccount = action.data["from"]
            quantity = action.data["quantity"]

            toac = AccountMgr().Instance().getWeiXinId(toaccount)
            frmac = AccountMgr().Instance().getWeiXinId(frmaccount)
            
            if(not toac  is None):
                 for eos in toac:
                     slef.sendTransertMsg("转帐提示",eos.name,frmaccount,toaccount,quantity)

            if(not frmac is None):
                 for eos in frmac:
                     self.sendTransertMsg("转帐提示",eos.name,frmaccount,toaccount,quantity)

        elif(action.account == "eosio" and action.name == "voteproducer"):
            
            voter = action.data["voter"]           
            for pb in action.data["producers"]:

                 pbwx = AccountMgr().Instance().getWeiXinId(pb) 
                 if(not pbwx is None):
                    for eos in pbwx:
                        self.sendVoteMsg(eos.name,voter,pb)
 
        return action;

    def getBlockInfo(self,blockid):
        
        Logger().Log(Text.TEXT10 % (blockid))
        headers = {'content-type': "application/json"}
        url = Config.HTTP_URL + "get_block"
        try:
             r = requests.post(url,data =json.dumps({"block_num_or_id":blockid}),headers = headers);
             if( r.status_code == 200):
                 js = json.loads(r.text)
                 return self.parseBlock(js)
             else:
                 Logger().Log(Text.Text11)
                 return None
        except:
             Logger().Log(Text.TEXT11)
             return None

    def getAccount(self,account):

        Logger().Log(Text.TEXT12)
        headers = {'content-type': "application/json"}
        url = Config.HTTP_URL + "get_account"
        try:
             r = requests.post(url,data =json.dumps({"account_name":account}),headers = headers);
             print r.status_code
             if( r.status_code == 200):
                 js = json.loads(r.text)
                 return js
             else:
                 return None
        except:
             Logger().Log(Text.TEXT13)
             return None
         

    
    def sendMsg(self,touser,content):
        
        Logger().Log(Text.TEXT14)
        token = AccessMgr().Instance().getToken()
        
        if not token is None:
            try:
                headers = {'content-type': "application/json"}
                postUrl = ("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %(token))
                r = requests.post(postUrl,data =json.dumps({"touser":touser,"msgtype":"text","text":{"content":content}}),headers = headers);
                if( r.status_code == 200):
                    js = json.loads(r.text)
            except:
                Logger().Log(Text.TEXT15)
    
    def sendTransertMsg(self,first,touser,auser,buser,balance):
       
       Logger().Log(Text.TEXT16)
       token = AccessMgr().Instance().getToken()
       if not token is None:
          try:
             headers = {'content-type': "application/json"}
             postUrl = ("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" %(token))

             r = requests.post(postUrl,data =json.dumps({"touser":touser,"template_id":"2yRo-UaxivRkKc3TzWQLRdb73lcmbpakquP9_QKZy8s",
             "data":{"first":{"value":first},"auser":{"value":auser},"buser":{"value":buser},"balance":{"value":balance}}}),headers = headers);
             
             if( r.status_code == 200):
                js = json.loads(r.text)
          except:
             Logger().Log(Text.TEXT17)
     

    def sendVoteMsg(self,pbwx,voter,pb):
       
       Logger().Log(Text.TEXT18) 
       token = AccessMgr().Instance().getToken()
       if not token is None:
          try:
              headers = {'content-type': "application/json"}
              postUrl = ("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" %(token))

              r = requests.post(postUrl,data =json.dumps({"touser":pbwx,"template_id":"qneLnkPx_W455wNdltxhAiNTqRUnEcufRQxZUKVftQM",
              "data":{"title":{"value":"投票提示"},"auser":{"value":voter},"buser":{"value":bp}}}),headers = headers);
              
              if( r.status_code == 200):
                   js = json.loads(r.text)  
          except:
              Logger().Log(Text.TEXT19)           

    def getInfo(self):

        Logger().Log(Text.TEXT20)
        try:

            headers = {'content-type': "application/json"}
            url = Config.HTTP_URL + "get_info"
            r = requests.get(url)

	    if(r.status_code == 200):

       	          js = json.loads(r.text)
                  
                  if("head_block_num" in js): 
                     Logger().Log(js['head_block_num'])
                     return js['head_block_num']
                  else:
                     Logger().Log('not exsit key')
                     return -1
            else:
                 Logger().Log(r.text)
        except:
            Logger().Log(Text.TEXT21)
          

      
