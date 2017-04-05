#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import pika

# 建立到达RabbitMQ Server的connection
credentials = pika.PlainCredentials('admin','12345')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1',5672,'/',credentials))
channel = connection.channel()

# 声明一个名为rpc_queue的queue
channel.queue_declare(queue='rpc_queue')


# 计算指定数字的斐波那契数
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

        # 回调函数，从queue接收到message后调用该函数进行处理


def on_request(ch, method, props, body):
    # 由message获取要计算斐波那契数的数字
    n = int(body)

    print " [.] fib(%s)" % (n,)
    # 调用fib函数获得计算结果
    response = fib(n)

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
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 只有consumer已经处理并确认了上一条message时queue才分派新的message给它
channel.basic_qos(prefetch_count=1)

# 设置consumeer参数，即从哪个queue获取消息使用哪个函数进行处理，是否对消息进行确认
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"

# 开始接收并处理消息
channel.start_consuming()