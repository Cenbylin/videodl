#!/usr/local/bin/python
# encoding: utf-8
'''
任务中心，集群数据中心
@author: Cenbylin
'''
from db_access import VideoDB
from items import VideoItem
from dl_exceptions import NoDataException
import dl_config as cfg
import logging
import SocketServer
import json
import time
import thread
from threading import Timer

# 任务中心锁
lock = thread.allocate_lock()
# 连接获得数据库实例
db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)
# 缓冲dict（32缓冲）
item_cache = {}

def get_job(binding_conn):
    """
    获得一个任务Item
    :param binding_conn: 绑定的链接
    :return: 
    """
    # 线程锁
    lock.acquire()
    '''
    尝试获得无锁的item
    '''
    item = None
    for k,v in item_cache.iteritems():
        if not v.cache_lock:
            item = v
    if not item:
        raise NoDataException
    logging.info("got an item without lock.")
    # 加锁
    item.cache_lock = binding_conn
    item_cache[str(item._id)] = item
    # 释放线程锁
    lock.release()
    # 判断刷新缓冲
    if len(item_cache)<8:
        logging.info("cache size is %d, now refresh it." % len(item_cache))
        __refresh_cache()
    return item

def unlocked_job(item):
    """
    解锁Item, 让其变成可被认领的任务
    :param item: 
    :return: 
    """
    if not item and not item_cache[str(item._id)]:
        item.__delattr__("cache_lock")

def __refresh_cache():
    """
    加载缓存
    一般是缓存中的item数目低于一定的值(8个)时进行刷新重载入
    """
    # 从数据库获得数据(32个)
    items = db.get_novideo_item_more(32)
    # 加入缓冲
    for item in items:
        # 判断有无，无则加入
        if not item_cache[str(item._id)]:
            item_cache[str(item._id)] = item

def submit_result(old_item, item_list):
    """
    提交结果
    :param old_item: 任务
    :param item_list: 结果集
    """
    '''
    结果入库
    '''
    for item in item_list:
        db.insert_video_item(item)
    logging.info("got results and insert into db.")
    '''
    删除原始记录
    '''
    # 从数据库删除
    logging.info("delete the template item of db.")
    db.delete_video_item(old_item._id)
    # 释放缓存
    logging.info("delete the template item of cache.")
    item_cache.pop(str(old_item._id))

'''
tcp连接
'''
class VsTcpHander(SocketServer.StreamRequestHandler):
    def check_alive(self):
        # 判断是否超时
        time_diff = time.localtime() - self.alive_time
        if time_diff>20000:
            self.timer.cancel()
            # 释放锁
            unlocked_job(self.job_item)
            # 结束
            self.conn_keep = False
            self.request.close()
    def handle(self):
        """
        tcp处理,长连接
        :return: 
        """
        self.conn_keep = True
        # 初始存活时间戳
        self.alive_time = time.localtime()
        # 20秒的定时检测器
        self.timer = Timer(20, self.check_alive)
        print "create"
        while self.conn_keep:
            self.data = str(self.request.recv(1024)).strip()
            print "got", self.data
            if not self.data:
                continue
            """
            消息类型判断
            """
            tag = self.data[0]
            if tag=="h":#心跳包
                # 更新存活时间戳
                self.alive_time = time.localtime()
            elif tag == "c":  # 获取配置
                cfg_dict = {"access_key":cfg.access_key,
                            "secret_key":cfg.secret_key,
                            "buckey":cfg.buckey}
                content = json.dumps(cfg_dict)
                self.request.sendall(content)
            elif tag=="g":#获取任务
                self.job_item = get_job(self)
                content = json.dumps(self.job_item.__dict__())
                self.request.sendall(content)
            elif tag=="s":#提交任务
                # 接收到的是一个list
                dict_list = json.loads(self.data)
                item_list = []
                for item_dict in dict_list:
                    submit_item = VideoItem()
                    submit_item.load_dict(item_dict)
                    item_list.append(submit_item)
                submit_result(self.job_item, item_list)
                #回馈
                self.request.sendall(u"success")
            else:
                pass
            logging.info("{} send message and proccess successfully".format(self.client_address[0]))

if __name__ == '__main__':
    """
    开启tcpserver
    """
    HOST, PORT = "localhost", 7037
    server = SocketServer.TCPServer((HOST, PORT), VsTcpHander)
    server.serve_forever()