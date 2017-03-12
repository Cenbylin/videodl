#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import logging
import os.path
import subprocess
from obtainers.MediaInfo import MediaInfo

'''
转化开始
'''
def extract_proccess(dir_path, media_path):
    audio_path = os.path.join(dir_path, "audio.wav")
    subprocess.call(["ffmpeg", "-i", media_path, "-vn", "-ar", "16000", "-ac", "1", "-ab", "100k", "-f", "wav", audio_path])
    logging.info("extract successfully.")
    return MediaInfo(media_path=audio_path, media_name="audio.wav", dir_path=dir_path)