# -*- coding: utf-8 -*-# filename: reply.py

import time
from logger import Logger
from blockmonitor import BlockMgr
from accountmgr import AccountMgr

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
        if (opts[0] == "bind"):
           return self.bindEosAccount(opts[1])
        elif (opts[0]  == "unbind"):
           return self.unbindEosAccount(opts[1])
        elif (opts[0] == "getaccount"):
            return self.getaccount(opts[1])
        else:
           return self.errorCmd()
    
    def errorCmd(self):
        self.__dict['Content'] = "没有相应的命令"
        return self.sendMsg()

    def getaccount(self,account):
       
       af =  BlockMgr().Instance().getAccount(account) 
       if (not af is  None):
          print "bbbb" 
          balance = af["core_liquid_balance"]
          print balance
          if (balance  is None):
             balance = "0.0000 EOS"
          print "cccc"
          content =  "余额为{0}".format(balance)  
          print content     
          self.__dict['Content'] = content 
          return self.sendMsg()
       else:
          self.__dict['Content'] = "EOS账号不存在"
          return self.sendMsg()
    
    def unbindEosAccount(self,account):
        AccountMgr().Instance().delAccount(iname)       

    def bindEosAccount(self,account):
       
       af =  BlockMgr().Instance().getAccount(account) 
       if (not af is  None):

          self.__dict['Content'] = "EOS账户绑定成功!"
          name = self.__dict['ToUserName']
          account_name = af['account_name']
          AccountMgr().Instance().AddAccount(name,account_name,"demo")       
          return self.sendMsg()
       else:
          self.__dict['Content'] = "EOS账号不存在"
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
       	   
           Logger().Print('subscribe')

           self.__dict['Content'] = '欢迎使用EOS监控系统！注册EOS账户请使用bind accountname'
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
            print name
            AccountMgr().Instance().delAccount(name)
