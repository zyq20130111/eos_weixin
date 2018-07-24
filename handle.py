# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import receive
import web
from  logger import Logger
from text import Text
import reply

class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "galaxy" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()

            Logger().Log(webData)  #后台打日志
            recMsg = receive.parse_xml(webData)

            if isinstance(recMsg, receive.Msg):

                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName

                if recMsg.MsgType == 'text':
                    Logger().Log(Text.TEXT32.format(recMsg.Content))
                    content = recMsg.Content
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()

                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()

                if recMsg.MsgType == 'event':
                    Logger().Log(Text.TEXT33.format(recMsg.Event)) 
                    event = recMsg.Event
                    eventkey = recMsg.EventKey
                    replyMsg = reply.EventMsg(toUser,fromUser,event,eventkey)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print "暂且不处理"
                return reply.Msg().send()
        except Exception, Argment:
            return Argment
