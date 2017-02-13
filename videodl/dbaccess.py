#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日

@author: Cenbylin
'''
from pymongo import MongoClient
from items.VideoItem import VideoItem
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
        coll = db['vs_video']
        #查询
        obj = coll.find_one(
            {'$or':[{"memory_path":{'$exists':False}}, {"memory_path":None}, {"memory_path":""}]}
        )
        #orm操作
        if not obj:
            return None
        video_item = VideoItem()
        video_item.load_dict(obj)
        print obj
        return video_item
        
    def update_video_item(self, video_item):
        '''
        :更新coll
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['vs_video']
        #更新
        coll.update({"_id":video_item._id}, video_item.to_dict())
    
    def insert_video_item(self, video_item):
        '''
        :插入item文档（不指定_id）
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['vs_video']
        video_dict = video_item.to_dict()
        #一定要去除id
        video_dict.pop("_id")
        coll.insert(video_dict)
    
    def delete_video_item(self, video_item):
        '''
        :删除（根据_id）
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['vs_video']
        coll.delete_one({"_id":video_item._id})
        
if __name__ == '__main__':
    db = VideoDB("localhost", 27017, "video_search")
    video_item = VideoItem()
    video_item.lessonNum = "1"
    video_item.tableNum = "imooc"
    video_item.url = "3240"
    db.insert_video_item(video_item)
    #print db.get_novideo_item().to_dict()
    