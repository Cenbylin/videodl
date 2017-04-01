#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import dl_config as cfg
from obtainers import imooc_obt,wy163_obt
'''
:容错函数
'''
def __none_platform(key, path_list):
    return None
'''
:获得媒体信息列表
'''
def get_media(platform_id, key, path_list):
    #接口字典
    switcher={
        1: imooc_obt.get_media,
        2: wy163_obt.get_media
        #blablabla多个平台....
    }
    #匹配对应平台的获取媒体方法
    fun = switcher.get(platform_id, __none_platform)
    #返回调用结果
    return fun(key, path_list)
