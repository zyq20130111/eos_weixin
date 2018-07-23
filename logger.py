#!/usr/bin/python
# -*- coding:UTF-8 -*-

import logging
class Logger(object):

    __instance = None

    def __init__(self):
       pass

    def __new__(cls, *args, **kwargs):
       if not Logger.__instance:
           Logger.__instance = object.__new__(cls,*args, **kwargs)
       return Logger.__instance

    def Instance(self):
        return Logger.__instance

    def Init(self):

        self.logger = logging.getLogger("simple_example")
	self.logger.setLevel(logging.DEBUG)
	# 建立一个filehandler来把日志记录在文件里，级别为debug以上
	fh = logging.FileHandler("spam.log")
	fh.setLevel(logging.DEBUG)
	# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)
	# 设置日志格式
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)
	#将相应的handler添加在logger对象中
	self.logger.addHandler(ch)
	self.logger.addHandler(fh)
     
    def Log(self,msg):
        self.logger.debug(msg)
     
    def Error(self,msg):
        self.logger.error(msg)

    def Print(self,msg):
        self.logger.debug(msg)
