# -*- coding: utf-8 -*-# filename: reply.py

import time
from logger import Logger

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
    def send(self):
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
           Logger().Print('unsubscribe')
