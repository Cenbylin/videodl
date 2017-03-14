#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
视频分析器
'''
import cv2
'''
容错函数
'''
def __none_platform(media_info):
    #cv2目前的处理支持所有格式
    return __analyze_mp4(media_info)
'''
接收一个媒体对象, 返回长度和分辨率
'''
def analyze_media(media_info):
    #调用字典
    switcher = {
        'mp4':__analyze_mp4
    }
    fun = switcher.get(media_info.media_format, __none_platform)
    return fun(media_info)
'''
MP4分析器
'''
def __analyze_mp4(media_info):
    '''
    :解析视频
    '''
    videoCapture = cv2.VideoCapture(media_info.media_path)
    # 获得码率及尺寸
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = "%dx%d" % (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 获得视频长度
    fps_num = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    m, s = divmod(int(fps_num / fps), 60)
    h, m = divmod(m, 60)
    length = "%s:%s:%s" % (str(h), str(m), str(s));
    resolution = str(size)
    return length, resolution