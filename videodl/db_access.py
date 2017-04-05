#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日

@author: Cenbylin
'''
from bson.objectid import ObjectId
from pymongo import MongoClient

from items.VideoItem import VideoItem
import dl_config as cfg


class VideoDB:
    def __init__(self, host, port, dbname, authdb=None, username=None, password=None):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.authdb = authdb
        self.username = username
        self.password = password
        #建立链接
        self.client = MongoClient(host, port)
        if authdb:
            self.client[authdb].authenticate(username, password)
        
    def __get_client(self):
        '''
        :拿到数据库连接
        '''
        if self.client and self.client.is_primary:
            pass
        else:
            #重新建立链接
            self.client.close()
            self.client = MongoClient(self.host, self.port)
            if self.authdb:
                self.client[self.authdb].authenticate(self.username, self.password)
        return self.client
    
    def get_novideo_item(self):
        '''
        :拿到一个尚未有视频的VideoItem
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['video']
        #查询
        obj = coll.find_one(
            {'$or':[{"memory_path":{'$exists':False}}, {"memory_path":None}, {"memory_path":""}]}
        )
        #orm操作
        if not obj:
            return None
        video_item = VideoItem()
        video_item.load_dict(obj)
        return video_item
    def get_item_byurl(self, url):
        '''
        :拿到指定url的Item
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['video']
        #查询
        obj = coll.find_one(
            {"url":url}
        )
        #orm操作
        if not obj:
            return None
        video_item = VideoItem()
        video_item.load_dict(obj)
        return video_item
    def get_novideo_item_more(self, num):
        '''
        :拿到多个尚未有视频的VideoItem，不足则全返回
        '''
        res = []
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['video']
        #查询多个
        objs = coll.find(
            {'$or':[{"memory_path":{'$exists':False}}, {"memory_path":None}, {"memory_path":""}]}
        )
        for obj in objs:
            # orm操作
            if not obj:
                return None
            video_item = VideoItem()
            video_item.load_dict(obj)
            res.append(video_item)

            # 取指定个数
            num = num - 1
            if num == 0:
                break
        return res
        
    def update_video_item(self, video_item):
        '''
        :更新coll
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['video']
        #更新
        coll.update({"_id":ObjectId(str(video_item._id))}, video_item.to_dict())
    
    def insert_video_item(self, video_item):
        '''
        :插入item文档（不指定_id）
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['video']
        video_dict = video_item.to_dict()
        #一定要去除id
        video_dict.pop("_id")
        coll.insert(video_dict)
    
    def delete_video_item(self, _id):
        '''
        :删除（根据_id）
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['video']
        coll.remove({"_id":ObjectId(ObjectId(_id))})
        
if __name__ == '__main__':

    db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)
    import json
    from utils import ItemEncoder
    #db.insert_video_item(video_item)
    print json.dumps(db.get_item_byurl("3225"), cls=ItemEncoder)
    print json.dumps({"123":1})
    