#!/usr/local/bin/python
# encoding: utf-8
'''
任务分发，集群的从主机
@author: Cenbylin
'''
import dl_config as cfg
import json
import time
import pika
import uuid
from items.VideoItem import VideoItem

"""
注册服务
"""
# 在一个类中封装了connection建立、queue声明、consumer配置、回调函数等
class CommonRpcClient(object):
    def __init__(self):
        # 建立到RabbitMQ Server的connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

        # 声明一个临时的回调队列
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        # 此处client既是producer又是consumer，因此要配置consume参数
        # 这里的指明从client自己创建的临时队列中接收消息
        # 并使用on_response函数处理消息
        # 不对消息进行确认
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    # 比较类的corr_id属性与props中corr_id属性的值
    # 若相同则response属性为接收到的message
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def get_config(self):
        # 初始化response和corr_id属性
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # 使用默认exchange向server中定义的rpc_queue发送消息
        # 在properties中指定replay_to属性和correlation_id属性用于告知远程server
        # correlation_id属性用于匹配request和response
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_getconfig',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   # message需为字符串
                                   body="")

        while self.response is None:
            self.connection.process_data_events()

        return str(self.response)
    def submit_result(self, content):
        # 初始化response和corr_id属性
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # 使用默认exchange向server中定义的rpc_queue发送消息
        # 在properties中指定replay_to属性和correlation_id属性用于告知远程server
        # correlation_id属性用于匹配request和response
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_submitresult',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   # message需为字符串
                                   body=content)

        while self.response is None:
            self.connection.process_data_events()

        return str(self.response)
# 生成类的实例
commonRpcClient = CommonRpcClient()
def init_config():
        received = commonRpcClient.get_config()
        cfg_dict = json.loads(received)
        cfg.access_key = cfg_dict["access_key"]
        cfg.secret_key = cfg_dict["secret_key"]
        cfg.buckey = cfg_dict["buckey"]

# 获取信息
init_config()
# 创建任务连接
job_connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
job_channel = job_connection.channel()
job_channel.queue_declare(queue='dl_task', auto_delete=True)
def get_job():
    """
    获得任务item
    :return: item
    """
    # 远程获得
    received = None
    global job_channel
    try:
        received = job_channel.basic_get(queue="dl_task")
    except Exception:
        pass
    # 处理获得为空的情况
    if not received:
        #重连
        job_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        job_channel = job_connection.channel()
        job_channel.queue_declare(queue='dl_task', auto_delete=True)
        return None
    elif not received[1]:
        return None
    received_body = received[2]
    global d_tag
    d_tag = received[0].delivery_tag
    item_dict = json.loads(received_body)
    job_item = VideoItem()
    job_item.load_dict(item_dict)
    return job_item

def submit_result(old_item_id, item_list):
    """
    提交任务
    :param item_list: 
    :return: 
    """
    res_dict = {"old_item_id":old_item_id, "item_list":item_list}
    json_str = json.dumps(res_dict)
    commonRpcClient.submit_result(json_str)
    job_channel.basic_ack(delivery_tag = d_tag)

if __name__ == '__main__':
    while True:
        print "单次开始"
        if get_job():
            submit_result("1231", ["1", "2"])
        time.sleep(2)

