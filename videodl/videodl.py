#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017年2月10日
@author: Cenbylin
主程序
'''
import logging
import os.path
import traceback
import time
import copy
import dl_config as cfg
from dl_exceptions import NoDataException
from obtainers.obt_exceptions import NotSupportedException
from db_access import VideoDB
import  qiniu_cloud
import obtainer
import video_analyzer
import audio_extractor

'''
日志初始化
'''
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

def rollback(id_list):
    """
    异常回滚
    :param id_list:
    :return:
    """
    for objectId in id_list:
        db.delete_video_item(objectId)
    
if __name__ == '__main__':
    history_id_list = []
    '''
    :不断执行
    '''
    #初始化日志
    init_log()
    #连接获得数据库实例
    db = VideoDB(cfg.db_host, cfg.db_port, cfg.db_name, cfg.db_authdb, cfg.db_username, cfg.db_password)
    while True:
        try:
            '''
           获得任务
            '''
            video_item = db.get_novideo_item()
            # 无数据抛出异常
            if not video_item:
                raise NoDataException()
            logging.info("=============================")
            logging.info("Proccess item(%s)." % str(video_item._id))

            '''
            下载媒体
            '''
            logging.info("video id is %s." % video_item.url)
            logging.info("Begin downloading.")
            # 算得item目录名
            path_list = [cfg.st_path, str(video_item.table_num), str(video_item.lesson_id)]
            media_infos = None
            try:
                media_infos= obtainer.get_media(video_item.table_num, video_item.url, path_list)
            except NotSupportedException:
                # 加标识
                video_item.memory_path = "NotSupported"
                db.update_video_item(video_item)
                # 外层抛
                raise NotSupportedException
            logging.info("got %d media." % len(media_infos))

            continue

            '''
            视频分析，包装item
            '''
            logging.info("analyze media and create item.")
            items = []
            for media_info in media_infos:
                item = copy.copy(video_item)
                #暂存绝对路径、名字
                item.memory_path = [media_info.media_path, media_info.media_name]
                #获得信息
                item.coding_format = media_info.media_format
                item.length, item.resolution = video_analyzer.analyze_media(media_info)
                items.append(item)

            '''
            音频提取和分析
            '''
            logging.info("extract audio.")
            res_audio = audio_extractor.extract_proccess(os.path.sep.join(path_list), items[-1].memory_path[0])

            '''
            云存储
            '''
            logging.info("start qiniu-cloud engine")
            #1、存音频
            audio_path = '%s/%s' % ('/'.join(path_list[1:]), "audio.wav")
            qiniu_cloud.create_task(res_audio.media_path, audio_path, True)
            logging.info("finish upload qiniu-cloud")
            logging.info("remove dir")
            try:
                os.rmdir(os.path.sep.join(path_list))
            except Exception,e:
                logging.info("rmdir failed")

            #2、存视频，同时更新音频存储字段
            for item in items:
                #最终存储路径
                final_path = '%s/%s' % ('/'.join(path_list[1:]), item.memory_path[1])
                qiniu_cloud.create_task(item.memory_path[0], final_path, True)
                item.memory_path = final_path
                item.audio_path = audio_path
            '''
            入库
            '''
            for item in items:
                db.insert_video_item(item)
                history_id_list.append(item._id)
            logging.info("success and insert into db.")
            #删除原始记录
            logging.info("delete the template item of db.")
            db.delete_video_item(video_item._id)
            logging.info("ALL finish.")
        except NoDataException:
                logging.error("No pre-data in database, waiting for retry...")
                # 没有待处理的数据，等待重新获得
                time.sleep(5)
        except NotSupportedException:
                logging.error("NotSupport, put a note and get next one..")
                # 不支持，跳下一个
                time.sleep(1)
        except IOError:
            logging.error("Get data failed for NetWork's problem, waiting for retry...")
            # 网络原因，无法获得请求结果
            '''
            :删除已经产生的数据
           '''
            rollback(history_id_list)
            time.sleep(2)
        except Exception,e:
            rollback(history_id_list)
            print traceback.format_exc()
        finally:
            history_id_list = []
            logging.info("=============================")


