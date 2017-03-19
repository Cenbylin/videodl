#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月12日

@author: Cenbylin
'''
import string, sys,os
import subprocess

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
def extract_proccess(dir_path, media_path):
    #os.system("ffmpeg")
    #subprocess.call([u"ffmpeg"], shell=True)
    print subprocess.call(["ffmpeg", "-i", media_path, "-vn", "-ar", "18000", "-ac", "2", "-ab", "100k", "-f", "wav", dir_path + "\\audio.wav"])
if __name__ == '__main__':
    extract_proccess(ur'D:\\videos\\imooc\\1\\ed3c6d91-f509-11e6-a4bf-14dda90a667e\\', ur"D:\\videos\\imooc\\1\\ed3c6d91-f509-11e6-a4bf-14dda90a667e\\2f43f640-f50a-11e6-bff8-14dda90a667e.mp4")
    
    