#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import dl_config as cfg
from db_access import VideoDB
import logging
'''
日志初始化
'''
def init_log():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='../log/merge_data.log',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-8s: %(levelname)-5s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    init_log()
    db_from = VideoDB(cfg.db_host, cfg.db_port, "edu_video", cfg.db_authdb, cfg.db_username, cfg.db_password)
    db_to = VideoDB(cfg.db_host, cfg.db_port, "test_edu_video", cfg.db_authdb, cfg.db_username, cfg.db_password)
    counter = 0
    while True:
        to_item = db_to.get_novideo_item()
        logging.info("get 1")
        if not to_item:
            break
        #拿到同url的旧记录
        from_item = db_from.get_item_byurl(to_item.url)
        #更新字段
        if from_item:
            to_item.memory_path = from_item.memory_path
            to_item.length = from_item.length
            to_item.resolution = from_item.resolution
            to_item.coding_format = from_item.coding_format
            to_item.audio_path = from_item.audio_path
        else:
            logging.info("none")
            to_item.memory_path = "NotSupported"
        db_to.update_video_item(to_item)
        counter = counter + 1
        logging.info("finish %d" % counter)