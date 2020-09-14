#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI

# import Exception

class CdataException(Exception):
    def __init__(self,err='cdata自定义异常'):
        Exception.__init__(self,err)


class IndexErrorException(CdataException):
    def __init__(self,err='获取索引错误'):
        Exception.__init__(self,err)




try:
    raise IndexErrorException
except IndexErrorException :
    print('error11')


class Networkerror(RuntimeError):
    def __init__(self, arg):
        self.args = arg

try:
    raise Networkerror("Bad hostname")
except Networkerror as e:
    print( e.args)

