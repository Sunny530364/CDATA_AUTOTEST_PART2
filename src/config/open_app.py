#!/usr/bin/python
# -*- coding UTF-8 -*-

#author: ZHONGQI
import win32api
import sys
import os

tftp = (os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))),"data/tftpd32.exe"))
win32api.ShellExecute(0, 'open', tftp, '', '', 1)