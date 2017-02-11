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
    localUri 视频本地路径
    codingFormat 编码格式
    length 视频长度
    resolution 分辨率
    playCount 播放次数
    time 录入时间
    '''
    def __init__(self, _id=None, lessonNum=None, url=None, localUri=None, codingFormat=None, length=None, resolution=None, playCount=None, time=None):
        self._id = _id
        self.lessonNum = lessonNum
        self.url = url
        self.localUri = localUri
        self.codingFormat = codingFormat
        self.length = length
        self.resolution = resolution
        self.playCount = playCount
        self.time = time
        
    def load_dict(self, video_dict):
        '''
        :传入字典进行orm
        '''
        self._id = video_dict.get("_id", None)
        self.lessonNum = video_dict.get("lesson_num", None)
        self.url = video_dict.get("url", None)
        self.codingFormat = video_dict.get("coding_format", None)
        self.length = video_dict.get("length", None)
        self.resolution = video_dict.get("resolution", None)
        self.playCount = video_dict.get("playCount", None)
        self.time = video_dict.get("time", None)
        self.localUri = video_dict.get("local_uri", None)
        
    def to_dict(self):
        '''
        :实体变成dict
        '''
        video_dict = {}
        video_dict['_id'] = self._id
        video_dict['lesson_num'] = self.lessonNum
        video_dict['url'] = self.url
        video_dict['local_uri'] = self.localUri
        video_dict['coding_format'] = self.codingFormat
        video_dict['length'] = self.length
        video_dict['resolution'] = self.resolution
        video_dict['playCount'] = self.playCount
        video_dict['time'] = self.time
        return video_dict
        
        