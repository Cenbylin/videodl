#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日

@author: Cenbylin
'''
class VideoItem():
    '''
    :视频集合
    lessonNum 课时编号
    url 视频地址
    codingFormat 编码格式
    length 视频长度
    resolution 分辨率
    playCount 播放次数
    time 录入时间
    '''
    def __init__(self, objectId=None, lessonNum, url, codingFormat, length, resolution, playCount, time):
        self.objectId = objectId
        self.lessonNum = lessonNum
        self.url = url
        self.codingFormat = codingFormat
        self.length = length
        self.resolution = resolution
        self.playCount = playCount
        self.time = time
