#!/usr/local/bin/python
# encoding: utf-8
'''
任务分发，集群的从主机
@author: Cenbylin
'''
import dl_config as cfg
import socket
import json
import time
import thread
from threading import Timer
from items import VideoItem

"""
注册服务
"""
# 生成锁
_sock_lock = thread.allocate_lock()
# 连接socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((cfg.server_name, cfg.server_port))
def heart_beat():
    print "begin heart"
    _sock_lock.acquire()
    sock.sendall("h")
    _sock_lock.release()
    print "heart"
def get_config():
    """
    获得配置信息(七牛)
    :return: 
    """
    _sock_lock.acquire()
    sock.sendall("c")
    # 从远端拿到
    received = str(sock.recv(1024)).strip()
    _sock_lock.release()
    cfg_dict = json.loads(received)
    cfg.access_key = cfg_dict["access_key"]
    cfg.secret_key = cfg_dict["secret_key"]
    cfg.buckey = cfg_dict["buckey"]
    print cfg_dict["buckey"]

# 开启心跳
heart_timer = Timer(5, heart_beat)
# 获取信息
#get_config()



def get_job():
    """
    获得任务item
    :return: item
    """
    _sock_lock.acquire()
    sock.sendall("g")
    # 从远端拿到
    received = str(sock.recv(1024)).strip()
    _sock_lock.release()
    item_dict = json.loads(received)
    job_item = VideoItem()
    job_item.load_dict(item_dict)
    return job_item
def submit_result(item_list):
    """
    提交任务
    :param item_list: 
    :return: 
    """
    json_str = json.dumps(item_list)
    _sock_lock.acquire()
    sock.sendall("s%s" % json_str)
    received = str(sock.recv(1024)).strip()
    _sock_lock.release()
    if received=="success":
        return
    else:
        raise

if __name__ == '__main__':
    get_config()
    time.sleep(1)
    heart_beat()
    time.sleep(1)
    heart_beat()
    time.sleep(1)
    heart_beat()
