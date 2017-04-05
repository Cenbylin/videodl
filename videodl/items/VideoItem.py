#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日

@author: Cenbylin
'''
from bson.objectid import ObjectId
import copy
class VideoItem():
    """"
    :视频集合
    lessonNum 课时编号
    tableNum 平台编号
    url 视频地址
    memoryPath 视频在本地的存储地址
    codingFormat 编码格式
    length 视频长度
    resolution 分辨率
    datetime 录入时间
    """
    def __init__(self, _id=None, lesson_id=None, course_id=None, table_num=None, url=None, memory_path=None, audio_path=None, coding_format=None, length=None, resolution=None, datetime=None):
        self._id = _id
        self.course_id = course_id
        self.lesson_id = lesson_id
        self.table_num = table_num
        self.url = url
        self.course_id = course_id
        self.memory_path = memory_path
        self.audio_path = audio_path
        self.coding_format = coding_format
        self.length = length
        self.resolution = resolution
        self.datetime = datetime
        
    def load_dict(self, video_dict):
        '''
        :传入字典进行orm
        '''
        self._id = ObjectId(str(video_dict.get("_id", None)))
        self.lesson_id = ObjectId(str(video_dict.get("lesson_id", None)))
        self.course_id = ObjectId(str(video_dict.get("course_id", None)))
        self.table_num = video_dict.get("table_num", None)
        self.url = video_dict.get("url", None)
        self.coding_format = video_dict.get("coding_format", None)
        self.length = video_dict.get("length", None)
        self.resolution = video_dict.get("resolution", None)
        self.datetime = video_dict.get("datetime", None)
        self.memory_path = video_dict.get("memory_path", None)
        self.audio_path = video_dict.get("audio_path", None)

    def to_dict(self):
        return copy.copy(self.__dict__)
    def to_json_dict(self):
        src_dict = self.to_dict()
        src_dict["_id"] = str(src_dict["_id"])
        src_dict["lesson_id"] = str(src_dict["lesson_id"])
        src_dict["course_id"] = str(src_dict["course_id"])
        return src_dict

