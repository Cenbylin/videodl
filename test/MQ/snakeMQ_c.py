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
my_messaging = snakemq.messaging.Messaging("client1", "1", my_packeter)
my_link.add_connector(("127.0.0.1", 4000))

#rpc
rh = snakemq.messaging.ReceiveHook(my_messaging)
crpc = snakemq.rpc.RpcClient(rh)
proxy = crpc.get_proxy("videodl", "myinstance")
proxy.mysignal.as_signal(10)  # 10 seconds TTL
#my_link.loop()

# in a different thread:
proxy.mysignal()  # not blocking
print proxy.get_fo()  # blocks until server responds