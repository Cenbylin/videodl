#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月12日

@author: Cenbylin
'''
import string, sys

def istextfile(filename, blocksize = 512):
    return isText(open(filename).read(blocksize))

def isText(s):
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")
    '''
        判断文件是文本还是二进制
    '''
    if "\0" in s:
        return False
   
    if not s:
        return 1
    t = s.translate(_null_trans, text_characters)
    if float(len(t))/float(len(s)) > 0.30:
        return False
    return True

if __name__ == '__main__':
    print istextfile(ur'D:\videos\1\2\2f9cdb00-ef80-11e6-978a-14dda90a667e.mp4')
    print istextfile(ur'D:\videos\1\2\1.txt')
    
    