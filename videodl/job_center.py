#!/usr/local/bin/python
# encoding: utf-8
'''
任务中心，集群数据中心
@author: Cenbylin
'''
from db_access import VideoDB
from items import VideoItem
import dl_config as cfg
import logging
import json
import pika
from multiprocessing import Process
import os
import time

# 连接获得数据库实例
db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)
'''
日志初始化
'''
def init_log():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='../log/job_center.log',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-8s: %(levelname)-5s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
def get_config():
    """
    获得配置
    :return: 七牛配置的json 
    """
    cfg_dict = {"access_key": cfg.access_key,
                "secret_key": cfg.secret_key,
                "buckey": cfg.buckey}
    content = json.dumps(cfg_dict)
    return content

def submit_result(old_item_id, dict_list):
    """
    提交结果
    """
    item_list = []
    for item_dict in dict_list:
        submit_item = VideoItem()
        submit_item.load_dict(item_dict)
        item_list.append(submit_item)
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
    db.delete_video_item(old_item_id)

"""
rpc部署
"""
def on_request_getconfig(ch, method, props, body):
    logging.info("[R]to get config.")
    # 调用函数获得计算结果
    response = get_config()

    # exchage为空字符串则将message发送个到routing_key指定的queue
    # 这里queue为回调函数参数props中reply_ro指定的queue
    # 要发送的message为计算所得的斐波那契数
    # properties中correlation_id指定为回调函数参数props中co的rrelation_id
    # 最后对消息进行确认
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))

def on_request_submitresult(ch, method, props, body):
    logging.info("[R]to submit 1 result.")
    param_dict = json.loads(body)
    # 调用函数获得计算结果
    response = submit_result(param_dict["old_item_id"], param_dict["item_list"])

    # exchage为空字符串则将message发送个到routing_key指定的queue
    # 这里queue为回调函数参数props中reply_ro指定的queue
    # 要发送的message为计算所得的斐波那契数
    # properties中correlation_id指定为回调函数参数props中co的rrelation_id
    # 最后对消息进行确认
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=str(response))

def __get_queue_count(queue_name):
    """
    获得队列任务数量
    :param queue_name: 
    :return: 
    """
    r = os.popen("rabbitmqctl list_queues")  # 执行该命令
    info = r.readlines()
    for line in info:
        if line.startswith(queue_name):
            line = line.strip().encode("utf-8")
            start = line.find(u"\t")
            return int(line[start+1:])

#子进程
def sub_proc():
    logging.info("[0]rpc-engine start.")
    # 建立到达RabbitMQ Server的connection
    credentials = pika.PlainCredentials('admin','12345')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '127.0.0.1', 5672, '/', credentials))
    channel = connection.channel()
    # 获得配置的queue
    channel.queue_declare(queue='rpc_getconfig')
    # 提交结果的queue
    channel.queue_declare(queue='rpc_submitresult', durable=True)
    # 只有consumer已经处理并确认了上一条message时queue才分派新的message给它
    #channel.basic_qos(prefetch_count=5)
    # 设置consumeer参数，即从哪个queue获取消息使用哪个函数进行处理，是否对消息进行确认
    channel.basic_consume(on_request_getconfig, queue='rpc_getconfig', no_ack=True)
    channel.basic_consume(on_request_submitresult, queue='rpc_submitresult', no_ack=True)
    logging.info("[R]waitting for calling.")
    # 开始接收并处理消息
    channel.start_consuming()
def super_proc():
    logging.info("[0]job-engine start.")
    # 建立到达RabbitMQ Server的connection
    credentials = pika.PlainCredentials('admin', '12345')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        '127.0.0.1', 5672, '/', credentials))
    channel = connection.channel()
    def close_callback():
        """断开重连"""
        logging.info("[J]connection blocked.now reconnect")
        global channel
        channel = connection.channel()
    channel.add_on_cancel_callback(close_callback)
    # 任务队列的queue
    channel.queue_declare(queue='dl_task', auto_delete=True)
    #监控任务队列
    while True:
        if __get_queue_count("dl_task")<8:
            logging.info("[J]queue has no enough jobs(<8), now loading...")
            item_list = db.get_novideo_item_more(32)
            for item in item_list:
                content = json.dumps(item.__dict__())
                channel.basic_publish(exchange='',
                                      routing_key='dl_task',
                                      body=content)
            logging.info("[J]have loadded.")
        time.sleep(5)

if __name__ == '__main__':
    init_log()
    """
    两个进程
    0-主线程提供rpc
    1-子进程提供任务
    """
    logging.info("=============start job-center=============")
    # 子进程
    p = Process(target=sub_proc)
    p.start()
    # 主进程
    super_proc()
    p.join()
    logging.info("=============job-center end=============")