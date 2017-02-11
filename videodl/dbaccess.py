#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日

@author: Cenbylin
'''
from pymongo import MongoClient
class VideoDB:
    
    def __init__(self, host, port, dbname, authdb, username, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.authdb = authdb
        self.username = username
        self.password = password
        #建立链接
        self.client = MongoClient(host, port)
        self.client[authdb].authenticate(username, password)
        
    def __get_client(self):
        '''
        :拿到数据库连接
        '''
        if self.client and self.client.is_primary():
            pass
        else:
            #重新建立链接
            self.client.close()
            self.client = MongoClient(self.host, self.port)
            self.client[self.authdb].authenticate(self.username, self.password)
        return self.client
    
    def get_novideo_item(self):
        '''
        :拿到尚未有视频的VideoItem
        '''
        client = self.__get_client()
        #数据库
        db = client[self.dbname]
        #视频集合
        coll = db['vs_video']
        #查询
        obj = coll.find_one(
            {"local_uri":{'$exists':True}}
        )
        #orm操作
        

    def update_video_item(self, video_item):
        pass
    
    
if __name__ == '__main__':
    db = VideoDB("localhost", 27017, "root", "037037037")