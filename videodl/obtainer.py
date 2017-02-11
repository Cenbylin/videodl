#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日
:用来做信息获得和视频下载
@author: Cenbylin
'''
import urllib
import json
import os.path
import uuid
import dlconfig as cfg

'''
:得到视频真实下载地址list
'''
def get_sources(video_id):
    #请求路径
    ajax_url = u"http://www.imooc.com/course/ajaxmediainfo/?mid=%d&mode=flash";
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
def download_and_save(url, pathlist):
    #uuid作为文件名，保留原文件后缀
    file_name = str(uuid.uuid1()) + os.path.splitext(url)[1].split(u"?")[0]
    
    #计算目录并且级联创建
    dir = os.path.join(cfg.st_path, os.path.sep.join(pathlist))
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    #组合文件路径
    local_path = os.path.join(dir, file_name)
    
    #开启下载
    urllib.urlretrieve(url, local_path)
    
    

if __name__ == '__main__':
    url_list = get_sources(2666)
    download_and_save(url_list[2],["1","2"])