# -*- coding: utf-8 -*-# filename: reply.py

import time
from logger import Logger
from blockmonitor import BlockMgr
from accountmgr import AccountMgr
from text  import Text

class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"
   

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def sendMsg(self):       
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>

        </xml>
        """
        return XmlForm.format(**self.__dict)
    
    def send(self):
        opts =  self.__dict['Content'].split() 
        if (opts[0] == "bind" or opts[0] == "c1"):
           return self.bindEosAccount(opts[1])
        elif (opts[0]  == "unbind"):
           return self.unbindEosAccount(opts[1])
        elif (opts[0] == "getaccount" or opts[0] == "c2"):
            return self.getaccount(opts[1])
        else:
           return self.errorCmd()
    
    def errorCmd(self):
        self.__dict['Content'] = Text.TEXT22
        return self.sendMsg()

    def getaccount(self,account):
       
       Logger().Log(Text.TEXT34)       
       af =  BlockMgr().Instance().getAccount(account) 
       if (not af is  None):
          
          balance = af.get("core_liquid_balance")
          if (balance  is None):
             balance = Text.TEXT25
          
          content =  "余额为{0:s}".format(balance)
          self.__dict['Content'] = content 
          return self.sendMsg()
       else:
          self.__dict['Content'] = Text.TEXT23
          return self.sendMsg()
    
    def unbindEosAccount(self,account):
        AccountMgr().Instance().delAccount(iname)       

    def bindEosAccount(self,account):
       
       Logger().Log(Text.TEXT36)       
       af =  BlockMgr().Instance().getAccount(account) 
       if (not af is  None):

          self.__dict['Content'] = Text.TEXT24
          name = self.__dict['ToUserName']
          account_name = af['account_name']
         
          status = AccountMgr().Instance().getAccountStatus(name,account_name,"demo")
          if(status == -1):
              self.__dict['Content'] = Text.TEXT39
          elif(status  == -2):
              self.__dict['Content'] = Text.TEXT37
          elif(status == -3):
              self.__dict['Content'] = Text.TEXT38
          elif(status == 0):
              self.__dict['Content'] = Text.TEXT24
              AccountMgr().Instance().AddAccount(name,account_name,"demo")       
          return self.sendMsg()
       
       else:
          self.__dict['Content'] = Text.TEXT23
          return self.sendMsg()
         
        
 
class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)



class EventMsg(Msg):
  
    def __init__(self, toUserName, fromUserName, eventId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Event'] = eventId
        self.__dict['Content'] = ""
    
    def send(self):
        
        if(self.__dict['Event'] == 'subscribe'): 
       	   
           Logger().Log(Text.TEXT35)

           self.__dict['Content'] = Text.TEXT26
           XmlForm = """
           <xml>
           <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
           <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
           <CreateTime>{CreateTime}</CreateTime>
           <MsgType><![CDATA[text]]></MsgType>
           <Content><![CDATA[{Content}]]></Content>
           </xml>
           """
           return XmlForm.format(**self.__dict)

        elif(self.__dict['Event'] == 'unsubscribe') :
            name = self.__dict['ToUserName'];
            AccountMgr().Instance().delAccount(name)
