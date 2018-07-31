# -*- coding: utf-8 -*-# filename: reply.py

import time
from logger import Logger
from blockmonitor import BlockMgr
from accountmgr import AccountMgr
from text  import Text
from config import Config

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
        
        if ((opts[0].lower() == "bind") and (len(opts) >=2 )):
           return self.bindEosAccount(opts[1])
        elif ((opts[0].lower()  == "unbind") and (len(opts) >=2) ):
           return self.unbindEosAccount(opts[1])
        elif((opts[0].lower() == "set") and (len(opts) > 2)):
           return self.setLimits(opts[1],opts[2])
        elif (opts[0].lower() == "help"):
            return self.helpCmd()
        else:
           return self.errorCmd()
    
    def setLimits(self,numstr1,numstr2):
       
       Logger().Log(Text.TEXT65)
       name = self.__dict['ToUserName']

       try:
          num1 = long(numstr1)
          num2 = long(numstr2)

          AccountMgr().Instance().AddRemind(name,num1,num2)
          self.__dict['Content'] = Text.TEXT66

       except:
          self.__dict['Content'] = Text.TEXT69 
      
       return self.sendMsg()       

    def helpCmd(self):
        self.__dict['Content'] =  Text.TEXT26
        return self.sendMsg()

    def errorCmd(self):
        self.__dict['Content'] = Text.TEXT22
        return self.sendMsg()
    
    def unbindEosAccount(self,account):
       
       Logger().Log(Text.TEXT52)

       af =  BlockMgr().Instance().getAccount(account)
       if (not af is  None):

          name = self.__dict['ToUserName']
          status = AccountMgr().Instance().getAccountStatus(name,account,"demo")
          
          if(status == -1):
              self.__dict['Content'] = Text.TEXT53.format(account)
              AccountMgr().Instance().delAccount(name,account)
          else:
              self.__dict['Content'] = Text.TEXT58            
 
          return self.sendMsg()

       else:
          self.__dict['Content'] = Text.TEXT23
          return self.sendMsg()                

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
  
    def __init__(self, toUserName, fromUserName, eventId,eventkey):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())

        self.__dict['Content'] = ""
        self.__dict['MedialID'] =""
        self.event = eventId
        self.eventkey = eventkey
    
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

    def sendPicMsg(self):

         XmlForm = """
         <xml>
         <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
         <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
         <CreateTime>{CreateTime}</CreateTime>
         <MsgType><![CDATA[image]]></MsgType>
         <Image>
         <MediaId><![CDATA[{MedialID}]]></MediaId>
         </Image>
         </xml>
         """
         return XmlForm.format(**self.__dict)
       
    def send(self):
        
        if(self.event == 'subscribe'): 
       	   
           Logger().Log(Text.TEXT35)

           self.__dict['Content'] = Text.TEXT26
           return self.sendMsg()

        elif(self.event == "unsubscribe"):

           Logger().Log(Text.TEXT56)

           weixin = self.__dict['ToUserName']
           AccountMgr().Instance().delWeiXin(weixin)
                      
           self.__dict['Content'] = Text.TEXT57
           return self.sendMsg()          

        elif((self.event == "CLICK") and (self.eventkey  == "bind")):
           self.__dict['Content'] = Text.TEXT48
           return self.sendMsg()
        elif((self.event == "CLICK") and (self.eventkey  == "unbind")):
           self.__dict['Content'] = Text.TEXT59
           return self.sendMsg()
        elif((self.event == "CLICK") and (self.eventkey == "join")):
           self.__dict['MedialID'] = Config.MEDIAID
           return self.sendPicMsg()
        elif((self.event == "CLICK") and (self.eventkey == "find")):
           name = self.__dict['ToUserName']
           accounts = AccountMgr().Instance().getAccounts(name)
         
           content = Text.TEXT50

           if(accounts is None):
              
              self.__dict['Content'] = Text.TEXT49
              return self.sendMsg()

           else:
              
              for eos in accounts :

                   title = Text.TEXT51.format(eos.eos_name)
                   eosdesc = self.getaccount(eos.eos_name)
                   content = "%s%s%s\n\r\n\r" %(content, title , eosdesc)  
             
              print content 
              self.__dict['Content'] = content
              return self.sendMsg()
        elif((self.event == "CLICK") and (self.eventkey == "set")):
              self.__dict['Content'] = Text.TEXT64
              return self.sendMsg()
    def getaccount(self,account):

       Logger().Log(Text.TEXT34)
       af =  BlockMgr().Instance().getAccount(account)
       if (not af is  None):

          balance = af.get("core_liquid_balance")
          if (balance  is None):
             balance = Text.TEXT25

          ram_usage = af.get("ram_usage")
          if(ram_usage is None):
             ram_usage =0
          ram_usage = format(float(ram_usage) / float(1024),'.2f')

          ram_quota = af.get("ram_quota")
          if(ram_quota is None):
             ram_quota = 0

          ram_quota = format(float(ram_quota) / float(1024),'.2f')

         #cpu_limit
          cpu_limit_used = 0
          cpu_limit_available = 0
          cpu_limit_max = 0

          cpu_limit = af.get("cpu_limit")
          if(not cpu_limit is None):

             if(not  cpu_limit.get("used") is None):
                 cpu_limit_used = cpu_limit.get("used")

             if(not  cpu_limit.get("available") is None):
                 cpu_limit_available = cpu_limit.get("available")

             if(not  cpu_limit.get("max") is None):
                 cpu_limit_max = cpu_limit.get("max")

          #net_limit
          net_limit_used = 0
          net_limit_available = 0
          net_limit_max = 0

          net_limit = af.get("cpu_limit")
          if(not net_limit is None):

             if(not  net_limit.get("used") is None):
                 net_limit_used = net_limit.get("used")
                 net_limit_used = format(float(net_limit_used) / float(1024),'.2f')

             if(not  net_limit.get("available") is None):
                 net_limit_available = cpu_limit.get("available")
                 net_limit_available = format(float(net_limit_available) / float(1024),'.2f')

             if(not  net_limit.get("max") is None):
                 net_limit_max = net_limit.get("max")
                 net_limit_max = format(float(net_limit_max) / float(1024),'.2f')



          content =  Text.TEXT46.format(balance,ram_usage,ram_quota,cpu_limit_used,cpu_limit_available,cpu_limit_max,net_limit_used,net_limit_available,net_limit_max)
          return content
       else:
          return  Text.TEXT23

