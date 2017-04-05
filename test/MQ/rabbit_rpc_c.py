#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import pika
import uuid


# 在一个类中封装了connection建立、queue声明、consumer配置、回调函数等
class FibonacciRpcClient(object):
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

        # 定义回调函数

    # 比较类的corr_id属性与props中corr_id属性的值
    # 若相同则response属性为接收到的message
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        # 初始化response和corr_id属性
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # 使用默认exchange向server中定义的rpc_queue发送消息
        # 在properties中指定replay_to属性和correlation_id属性用于告知远程server
        # correlation_id属性用于匹配request和response
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   # message需为字符串
                                   body=str(n))

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)

# 生成类的实例
fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
# 调用实例的call方法
response = fibonacci_rpc.call(30)
print " [.] Got %r" % (response,)