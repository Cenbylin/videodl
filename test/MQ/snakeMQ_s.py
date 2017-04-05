#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message
import snakemq.rpc

my_link = snakemq.link.Link()
my_packeter = snakemq.packeter.Packeter(my_link)
my_messaging = snakemq.messaging.Messaging("videodl", "127.0.0.1", my_packeter)
my_link.add_listener(("", 4000))

#rpc
rh = snakemq.messaging.ReceiveHook(my_messaging)
class MyClass(object):
    def get_fo(self):
        return "fo value"
    @snakemq.rpc.as_signal  # mark method as a signal
    def mysignal(self):
        print("signal")
srpc = snakemq.rpc.RpcServer(rh)
srpc.register_object(MyClass(), "myinstance")
my_link.loop()