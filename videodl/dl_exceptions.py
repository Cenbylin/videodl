#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月13日

@author: Cenbylin
'''

class NoDataException(Exception):
    def __init__(self, msg=None):
        self.msg = msg
    

