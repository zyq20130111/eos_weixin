#/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import threading
import time
import requests
import json
import pytz

from accessmgr import AccessMgr
from config import Config  
from logger import Logger
from text  import Text
from accountmgr import AccountMgr

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

class Voter(object):
    def __init__(self,owner,proxy,producers,stake,is_proxy):
       self.owner = owner
       self.proxy = proxy
       self.producers = producers
       self.stake = stake
       self.is_proxy = is_proxy

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

           curId = self.getInfo()

           if(self.block_num_id < curId):
               
               self.block_num_id = self.block_num_id + 1
               time.sleep(0.001)
               self.getBlockInfo(self.block_num_id)

               f = open('block.txt', 'w')
               f.write(str(self.block_num_id) + " curnumid=" + str(curId))
               f.flush()

           else:
              Logger().Log("start_block_id access curnumid:{0}".format(curId))

    def Start(self):

         self.block_num_id = Config.START_BLOCK_NUM_ID
              
         t =threading.Thread(target=self.threadFun,args=(1,))
         t.setDaemon(True)#设置线程为后台线程
         t.start()

   
    def parseBlock(self,blockJson):
        
        print(Text.TEXT27)       
        block = BlockInfo()        
        if("transactions" in blockJson):
              for trx in blockJson["transactions"]:
                  trxObj =  self.parseTransaction(trx)
                  block.addTrx(trxObj)
        else:
            Logger().Log('not exsit transaction')
        return block

    def parseTransaction(self,trxJson):

        print(Text.TEXT28)
        trx = Transaction()
        if("trx" in trxJson):

           trxid = "00000000"
           if("id" in trxJson["trx"]):
             trxid = trxJson["trx"]["id"]
            

           if("transaction" in trxJson["trx"]):
              if("actions" in trxJson["trx"]["transaction"]):
                  for actionJson in trxJson["trx"]["transaction"]["actions"] :
                         act =  self.parseAction(actionJson,trxid)
                         if(not act is None):
                            trx.addAction(act)

        return trx       
         
    
    
    def parseAction(self,actionJson,trxid):
        
        print(Text.TEXT29)
        action = Action(actionJson.get("account"),actionJson.get("name"),actionJson.get("data"))
        
        if(action.data is None):
            return None

        if(action.account == "eosio.token" and action.name == "transfer"):
            
            toaccount = action.data.get("to")
            frmaccount = action.data.get("from")
            quantity = action.data.get("quantity")
            
            toac = AccountMgr().Instance().getWeiXinId(toaccount)
            frmac = AccountMgr().Instance().getWeiXinId(frmaccount)

            
            if(not toac  is None):
                 for eos in toac:
                     self.sendTransertMsg(trxid,eos.name,time.time(),frmaccount,toaccount,quantity,toaccount)

            if(not frmac is None):
                 for eos in frmac:
                     self.sendTransertMsg(trxid,eos.name,time.time(),frmaccount,toaccount,quantity,frmaccount)

            
            try:
                 nowTime = self.getDateTime()
                 AccountMgr().Instance().addTransfer(frmaccount,toaccount,nowTime,quantity)
            except:
                 Logger().Log(Text.TEXT17)
                 return


        elif(action.account == "eosio" and action.name == "voteproducer"):
            
            voter = action.data.get("voter")
            accountNum = self.getAccountDelegate(voter)
           
            for pb in action.data.get("producers"):

                 pbwx = AccountMgr().Instance().getWeiXinId(pb) 
                 if(not pbwx is None):
                    for eos in pbwx:
                        self.sendVoteMsg(trxid,eos.name,voter,pb,action,accountNum)
 
        return action;

    def getBlockInfo(self,blockid):
     
        print(Text.TEXT10 % (blockid))
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
    

    def getDateTime(self):

        tz = pytz.timezone('Asia/Shanghai') #东八区
        t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        return t

    def sendTransertMsg(self,trxid,pbwx,actionID,auser,buser,quantity,account):
        
       Logger().Log(Text.TEXT16)

       transfer = 0
       re = AccountMgr().Instance().getRemind(pbwx)
       if not re is None:
          transfer = re.transfer

       
       balanceSplt = quantity.split("EOS")
       if(len(balanceSplt) <= 0 ):
          Logger().Log(Text.TEXT67)
          return
            
             
       if(float(balanceSplt[0]) < transfer):
          Logger().Log(Text.TEXT68)
          return
       
       token = AccessMgr().Instance().getToken()
       if not token is None:
          try:

             headers = {'content-type': "application/json"}
             postUrl = ("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" %(token))

             balance = Text.TEXT25
             af =  BlockMgr().Instance().getAccount(account)

             if (not af is  None):
                 balance = af.get("core_liquid_balance")

             url = Text.TEXT72.format(auser,buser,quantity,balance,account) 
             reMarket = Text.TEXT45.format(auser,buser)

             nowTime = self.getDateTime()
             
             r = requests.post(postUrl,data =json.dumps({"touser":pbwx,"template_id":Config.TRANSFERTEMPLATEID,"url":url,
             "data":{"first":{"value":Text.TEXT43},"keyword1":{"value":actionID},"keyword2":{"value":nowTime},
             "keyword3":{"value":actionID},"keyword4":{"value":Text.TEXT44},"keyword5":{"value":quantity},"remark":{"value":reMarket}}}),headers = headers);

             if( r.status_code == 200):
                js = json.loads(r.text)
          except:
             Logger().Log(Text.TEXT17)
     

    def getAccountDelegate(self,vote):
         
          weight = 0
          
          acc = self.getAccount(vote)
          if(acc is None):
              return 0

          if("voter_info" in acc):
              if("staked" in acc["voter_info"]):
                 weight = acc["voter_info"]["staked"]
 

          return  long(weight) / 10000                 


    def sendVoteMsg(self,trxid,pbwx,voter,pb,action,accountNum):
        
       Logger().Log(Text.TEXT18)
       token = AccessMgr().Instance().getToken()
       if not token is None:
          try:
              headers = {'content-type': "application/json"}
              postUrl = ("https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" %(token))
              
              nowTime = self.getDateTime()
              remark = Text.TEXT42.format(voter,pb,accountNum)
             
              voteNum = 0
              re = AccountMgr().Instance().getRemind(pbwx)
              if not re is None:
                    voteNum = re.vote
        
              
              AccountMgr().Instance().addVote(voter,pb,accountNum,nowTime)
              
              if(accountNum < voteNum): 
                    Logger().Log(Text.TEXT68)
                    return 
 
              producers = ""
              if(not action is None):
                  producers =  action.data.get("producers")
                  producers = ','.join(producers)

              url = Text.TEXT60.format(voter,producers,accountNum,pb)
              r = requests.post(postUrl,data =json.dumps({"touser":pbwx,"template_id":Config.VOTETEMPLATEID,"url":url,
              "data":{"first":{"value":Text.TEXT40},"keyword1":{"value":Text.TEXT41},"keyword2":{"value":nowTime},"remark":{"value":remark}}}),headers = headers);
              
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
                     
                     if "head_block_num" in js:
                          return js['head_block_num']
                     else:
                          return -1
                  else:
                     Logger().Log('not exsit key')
                     return -1
            else:
                 Logger().Log(r.text)
                 return -1
        except:
            Logger().Log(Text.TEXT21)
            return -1
          

      
