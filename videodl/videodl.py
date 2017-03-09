#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日
@author: Cenbylin
主程序
'''
import dl_config as cfg
import cv2
from db_access import VideoDB
import obtainer.imooc_obt as imooc_obt
import subprocess
import time
import os.path
import uuid
import logging
from dl_exceptions import NoDataException

history_id_list = []
history_path_list = []
def extract_proccess(dir_path, media_path):
    audio_path = os.path.join(dir_path, "audio.wav")
    subprocess.call(["ffmpeg", "-i", media_path, "-vn", "-ar", "8000", "-ac", "1", "-ab", "100k", "-f", "wav", audio_path])
def dl_proccess(db):
    history_dir = ''
    #获得待下载视频的videoitem
    video_item = db.get_novideo_item()
    #无数据抛出异常
    if not video_item:
        raise NoDataException()
    else:
        logging.info("=============================")
        logging.info("Proccess item(%s)." % str(video_item._id))
    temp_id = video_item._id
    logging.info("video id is %s." % video_item.url)
    #拿到视频真实地址list
    media_url_list = imooc_obt.get_sources(video_item.url)
    #算得item目录名
    dir_uuid = uuid.uuid1()
    logging.info("got %d media." % len(media_url_list))
    '''
    :处理地址列表
    '''
    for media_url in media_url_list:
        #下载视频
        logging.info("downloading...")
        dir_path, media_name, media_format = imooc_obt.download_and_save(media_url, [str(video_item.table_num),
                                                               str(video_item.lesson_id), 
                                                               str(dir_uuid)])
        media_path = os.path.join(dir_path, media_name)
        video_item.memory_path = media_path
        video_item.coding_format = media_format
        #记录
        history_path_list.append(media_path)
        history_dir = dir_path
        '''
        :解析视频
        '''
        videoCapture = cv2.VideoCapture(media_path)
        #获得码率及尺寸
        fps =  videoCapture.get(cv2.CAP_PROP_FPS)
        size = "%dx%d" % (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
                int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        #获得视频长度
        fps_num = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        m, s = divmod(int(fps_num/fps), 60)
        h, m = divmod(m, 60)
        video_item.length = "%s:%s:%s" % (str(h), str(m), str(s));
        video_item.resolution = str(size)
        #入库
        db.insert_video_item(video_item)
        history_id_list.append(video_item._id)
        logging.info("success and insert into db.")
    '''   
    :删除临时记录
    '''
    db.delete_video_item(temp_id)
    logging.info("delete the template item of db.")
    '''
    :抽取音频
    '''
    extract_proccess(history_dir, history_path_list[-1])
def init_log():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../log/dl.log',
                filemode='w')
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-8s: %(levelname)-5s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    
if __name__ == '__main__':
    '''
    :不断执行
    '''
    #初始化日志
    init_log()
    #连接获得数据库实例
    db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)
    while True:
        try:
            dl_proccess(db)
        except NoDataException:
            logging.error("No pre-data in database, waiting for retry...")
            #没有待处理的数据，等待重新获得
            time.sleep(5)
        except IOError:
            logging.error("Get data failed for NetWork's problem, waiting for retry...")
            #网络原因，无法获得请求结果
            '''
            :删除已经完成的部分
            '''
            for objectId in history_id_list:
                db.delete_video_item(objectId)
            time.sleep(2)
        except Exception,e:  
            print Exception,":",e
        finally:
            history_id_list = []
            history_path_list = []
            logging.info("=============================")
