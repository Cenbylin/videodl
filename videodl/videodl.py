#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日
@author: Cenbylin
'''
import dlconfig as cfg
import cv2
from dbaccess import VideoDB
import obtainer

if __name__ == '__main__':
    #连接获得数据库实例
    db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)
    '''
    :不断执行
    '''
    while True:
        #获得待下载视频的videoitem
        video_item = db.get_novideo_item()
        #拿到视频真实地址list
        media_url_list = obtainer.get_sources(video_item.url)
        '''
        :处理地址列表
        '''
        for media_url in media_url_list:
            #下载视频
            media_path, media_format = obtainer.download_and_save(media_url, [str(video_item.lessonNum)])
            video_item.memoryPath = media_path
            video_item.codingFormat = media_format
            '''
            :解析视频
            '''
            videoCapture = cv2.VideoCapture(media_path)
            #获得码率及尺寸
            fps =  videoCapture.get(cv2.CAP_PROP_FPS)
            size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                    int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            #获得视频长度
            fps_num = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
            m, s = divmod(int(fps_num/fps), 60)
            h, m = divmod(m, 60)
            video_item.length = "%s:%s:%s" % (str(h), str(m), str(s));
            video_item.resolution = str(size)
            #入库
            db.insert_video_item(video_item)
        '''   
        :删除临时记录
        '''
        db.delete_video_item(video_item)
            
