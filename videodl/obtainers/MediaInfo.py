#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''

'''
:媒体信息类
'''
class MediaInfo:
    def __init__(self, media_path=None, dir_path=None, media_name=None, media_format=None):
        self.media_path = media_path
        self.dir_path = dir_path
        self.media_name = media_name
        self.media_format = media_format