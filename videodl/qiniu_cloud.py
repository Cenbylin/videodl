#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
七牛云存储接口
V0.1不做队列，同步处理
'''
'''
初始化
'''
from qiniu import Auth,put_file
from dl_config import access_key,secret_key,buckey
import os
#七牛授权
qn = Auth(access_key, secret_key)

def create_task(local_path, dis_path, to_delete=False):
    """
    创建任务接口
    :param local_path: 本地路径
    :param dis_path: 目标路径（相对）
    :param to_delete: 是否在处理完成后删除
    :return: 目标路径
    """
    # 生成上传 Token，可以指定过期时间等
    token = qn.upload_token(buckey, dis_path, 3600)
    ret, info = put_file(token, dis_path, local_path)
    #判断删除
    if to_delete:
        os.remove(local_path)
    return dis_path