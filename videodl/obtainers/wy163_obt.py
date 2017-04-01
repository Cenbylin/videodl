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
import requests
import time
from MediaInfo import MediaInfo

def GetMiddleStr(content,startStr,endStr):
  startIndex = content.index(startStr)
  if startIndex>=0:
    startIndex += len(startStr)
  endIndex = content.index(endStr, startIndex)
  return content[startIndex:endIndex]

def __get_sources(lessonId_courseId):
    """
    得到视频真实下载地址list
    :param lessonId:
    :param courseId:
    :return:
    """
    temparr = str(lessonId_courseId).split(",")
    lessonId = temparr[0]
    courseId = temparr[1]
    # 创建session
    s = requests.session()
    s.get("http://study.163.com/course/courseLearn.htm?courseId=%s" % courseId)
    sessionId = s.cookies["NTESSTUDYSI"]
    othercookie = s.cookies["EDUWEBDEVICE"]
    time_str = str(int(time.time() * 1000))
    url = "http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr"
    querystring = {time_str: ""}
    payload = "callCount=1&scriptSessionId=%24%7BscriptSessionId%7D190&httpSessionId=" \
              + sessionId + "&c0-scriptName=LessonLearnBean&c0-methodName=getVideoLearnInfo&c0-id=0" \
              + "&c0-param0=string%3A" + courseId + "&c0-param1=string%3A" + lessonId + "&batchId=" + time_str
    response = s.request("POST", url, data=payload, params=querystring)
    urls = response.text.split("\n")[4]
    hdUrl = GetMiddleStr(urls, "mp4HdUrl=\"", "\";s1.")
    return [hdUrl]

def __download_and_save(url, pathlist):
    """
    根据地址下载视频存储到本地
    :param url:
    :param pathlist:
    :return: 返回路径和格式
    """

    #后缀名
    suffix = os.path.splitext(url)[1].split(u"?")[0]
    file_name = str(uuid.uuid1()) + suffix
    
    #计算目录并且级联创建
    st_dir = os.path.sep.join(pathlist)
    if not os.path.exists(st_dir):
        os.makedirs(st_dir)
        
    #组合文件路径
    local_path = os.path.join(st_dir, file_name)
    
    #开启下载
    urllib.urlretrieve(url, local_path)
    
    #判断是否下载成功
    
    return st_dir, file_name, suffix.split(".")[1]


def get_media(key, path_list):
    """
    imooc拿到抓取结果地址列表
    :param key:
    :param path_list:
    :return:
    """
    #拿到视频真实地址list
    media_url_list = __get_sources(key)
    logging.info("got %d media." % len(media_url_list))
    '''
    :处理地址列表
    '''
    counter = 0
    media_infos = []
    #取最后一个
    media_url = media_url_list[-1]
    print "url:",media_url
    #下载视频
    logging.info("downloading...%d" % counter)
    dir_path, media_name, media_format = __download_and_save(media_url, path_list)
    media_path = os.path.join(dir_path, media_name)
    #媒体信息对象
    media_infos.append(MediaInfo(media_path, dir_path, media_name, media_format))
    logging.info("finish this")
    return media_infos
if __name__ == '__main__':
    lessonId = "1003687003"
    courseId = "1004219036"
    # 创建session
    s = requests.session()
    s.get("http://study.163.com/course/courseLearn.htm?courseId=%s" % courseId)
    sessionId = s.cookies["NTESSTUDYSI"]
    othercookie = s.cookies["EDUWEBDEVICE"]
    time_str = str(int(time.time()*1000))
    url = "http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr"
    querystring = {time_str: ""}
    payload = "callCount=1&scriptSessionId=%24%7BscriptSessionId%7D190&httpSessionId="\
              + sessionId + "&c0-scriptName=LessonLearnBean&c0-methodName=getVideoLearnInfo&c0-id=0"\
              +"&c0-param0=string%3A"+courseId+"&c0-param1=string%3A"+lessonId+"&batchId="+time_str
    response = s.request("POST", url, data=payload, params=querystring)
    print response.text




    '''
        c = requests.cookies.RequestsCookieJar()
        c.set('__utma', '129633230.35777634.1491030902.1491030902.1491030902.1', path='/', domain='.study.163.com')
        c.set('__utmb', "129633230.2.9.1491030903407", path='/', domain='.study.163.com')
        c.set('__utmc', "129633230", path='/', domain='.study.163.com')
        c.set('__utmz', "129633230.1491030902.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)", path='/', domain='.study.163.com')
        s.cookies.update(c)
        '''