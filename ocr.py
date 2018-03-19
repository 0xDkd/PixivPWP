#-*- coding=utf-8 -*-
import requests
from PIL import Image
from StringIO import StringIO

upload_url = 'http://api.yundama.com/api.php?method=upload'
query_url = 'http://api.yundama.com/api.php?method=result&cid='

#云打码的用户名、密码
username = ''
password = ''


def upload(img):
    data = {
        'username': username,
        'password': password,
        'codetype': '1005',
        'appid': '1',
        'appkey': '22cc5376925e9387a23cf797cb9ba745',
        'timeout': '60',
        'method': 'upload'
    }
    file_ = {'file': img}
    r = requests.post(upload_url, data=data, files=file_)
    retdata = r.json()
    if retdata["ret"] == 0:
        print '上传成功'
        return retdata['cid']
    else:
        print '上传失败'
        return False


def query_cid(cid):
    url = query_url + str(cid)
    while 1:
        r = requests.get(url)
        retdata = r.json()
        if retdata["ret"] == 0:
            code = retdata["text"]
            print u'识别验证码：{}'.format(code)
            return code
            break


def captch(img):
    cid = upload(img)
    if cid <> False:
        code = query_cid(cid)
        return code
    else:
        return 'abcd'
