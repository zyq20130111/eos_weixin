# -*- coding: utf-8 -*-# filename: receive.py

import xml.etree.ElementTree as ET 

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    
    msg_type = xmlData.find('MsgType').text
   
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'event':
        return EventMsg(xmlData)

class Msg(object):
    def __init__(self, xmlData):

        toUserName = xmlData.find('ToUserName')
        if not toUserName is None:
           self.ToUserName = toUserName.text
        
        FromUserName = xmlData.find('FromUserName')
        if not FromUserName is None:
           self.FromUserName = FromUserName.text

        CreateTime = xmlData.find('CreateTime')
        if not CreateTime is None:
           self.CreateTime = CreateTime.text
        
        MsgType = xmlData.find('MsgType')
        if not MsgType is None:
           self.MsgType = MsgType.text
        
        MsgId = xmlData.find('MsgId')
        if not MsgId is None:
           self.MsgId = MsgId.text
        
   

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class  EventMsg(Msg):
    def __init__(self,xmlData):
        Msg.__init__(self, xmlData)
        self.Event = xmlData.find("Event").text
        self.EventKey = xmlData.find("EventKey").text
