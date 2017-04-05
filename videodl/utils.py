#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月12日

@author: Cenbylin
'''
import json
from items.VideoItem import VideoItem
from bson.objectid import ObjectId
class ItemEncoder(json.JSONEncoder):
    """
    编码器
    """
    def default(self, obj):
        if isinstance(obj, VideoItem):
            return obj.to_json_dict()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)