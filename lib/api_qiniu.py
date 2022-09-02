# -*- coding: utf-8 -*-
# flake8: noqa

import time

from django.conf import settings
from qiniu import Auth, put_file, put_data

# pip install qiniu

# 秘钥
access_key = settings.QINIU_ACCESS_KEY
secret_key = settings.QINIU_SECRET_KEY
# 要上传的空间
bucket_name = settings.QINIU_BUCKET_NAME
# 构建鉴权对象
q = Auth(access_key, secret_key)


def upload_file(path, key=None, prefix='blog/'):
    """
    prefix：前缀
    :param path: 图片的路径
    :param key: 图片上传之后的名字
    :return: 在线路径
    """
    # 上传后保存的文件名

    if not key:
        key = prefix + str(int(time.time())) + '.' + path.split('.')[-1]
    else:
        key = prefix + key + '.' + path.split('.')[-1]
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 2)

    # http://python.fengfengzhidao.com/my-python-logo.png

    put_file(token, key, path, version='v2')

    return f'http://{settings.QINIU_DOMAIN}/{key}'


def upload_data(file_data, key=None, suffix='.png', prefix='blog/'):
    """
        prefix：前缀
        :param file_data: 图片的字节数据
        :param key: 图片上传之后的名字
        :return: 在线路径
        """
    # 上传后保存的文件名

    if not key:
        key = prefix + str(int(time.time())) + suffix
    else:
        key = prefix + key + suffix
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 2)

    # http://python.fengfengzhidao.com/my-python-logo.png

    put_data(token, key, file_data)

    return f'http://{settings.QINIU_DOMAIN}/{key}'


if __name__ == '__main__':
    # file_name = upload_file('./13.jpg')
    # print(file_name)
    with open('13.jpg', 'rb')as f:
        data = f.read()
        file_name = upload_data(data)
        print(file_name)
