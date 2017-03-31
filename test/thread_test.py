#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import thread
if __name__ == '__main__':
    lock = thread.allocate_lock()
    lock.acquire()
    lock.release()