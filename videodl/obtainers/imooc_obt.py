#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日
:obtainer用来做视频下载
@author: Cenbylin
'''
import urllib
import json
import os.path
import uuid
import logging
from MediaInfo import MediaInfo

'''
:得到视频真实下载地址list
'''
def __get_sources(video_id):
    #根据id请求路径
    ajax_url = u"http://www.imooc.com/course/ajaxmediainfo/?mid=%s&mode=flash";
    f = urllib.urlopen(ajax_url % video_id)
    json_str = f.read()
    #结果
    data = json.loads(json_str)
    return data['data']['result']['mpath']
    
'''
:根据地址下载视频存储到本地
@param url: 地址
@param pathlist: 相对路径层级（相对于配置中的根目录）
'''
def __download_and_save(url, st_path, pathlist):
    '''
    :下载视频
    :返回路径和格式
    '''
    #后缀名
    suffix = os.path.splitext(url)[1].split(u"?")[0]
    file_name = str(uuid.uuid1()) + suffix
    
    #计算目录并且级联创建
    st_dir = os.path.join(st_path, os.path.sep.join(pathlist))
    if not os.path.exists(st_dir):
        os.makedirs(st_dir)
        
    #组合文件路径
    local_path = os.path.join(st_dir, file_name)
    
    #开启下载
    urllib.urlretrieve(url, local_path)
    
    #判断是否下载成功
    
    return st_dir, file_name, suffix.split(".")[1]

'''
:imooc拿到抓取结果地址列表
'''
def get_media(key, path_list):
    #拿到视频真实地址list
    media_url_list = __get_sources(key)
    logging.info("got %d media." % len(media_url_list))
    '''
    :处理地址列表
    '''
    counter = 0
    media_infos = []
    for media_url in media_url_list:
        #下载视频
        logging.info("downloading...%d" % counter)
        dir_path, media_name, media_format = __download_and_save(media_url, [path_list])
        media_path = os.path.join(dir_path, media_name)
        #媒体信息对象
        media_infos.append(MediaInfo(media_path, dir_path, media_name, media_format))
        logging.info("finish this")
        counter += 1
    return media_infos
