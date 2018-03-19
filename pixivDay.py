#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from threading import Thread
from Queue import LifoQueue
from localdb import DB

from bs4 import BeautifulSoup
import time

host='https://www.pixiv.net/ranking.php?mode=daily'
se = requests.session()
parent = 'https://www.pixiv.net'

class pixiv_day():
    def __init__(self):  #Initliaze 
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.main_url = 'http://www.pixiv.net'
        self.headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.pixiv_id = ''  #put in your pivix user_name
        self.password = ''  #put in your pivix password
        self.post_key = []  #Store login data ,Don't edit this!
        self.return_to = 'http://www.pixiv.net/'


    def login(self):        #Login
        post_key_html = se.get(self.base_url, headers=self.headers).text  #GET input HTML
        post_key_soup = BeautifulSoup(post_key_html, 'html.parser') 
        self.post_key = post_key_soup.find('input')['value']
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        } #Store all info to data
        se.post(self.login_url, data=data, headers=self.headers)


    def get_html(self, url, timeout, proxy=None, num_entries=5):  #  auto check use proxy or not
        if proxy is None:
            try:
                return se.get(url, headers=self.headers, timeout=timeout)  
            except:
                if num_entries > 0:
                    print('Access to a web page error', num_entries, ' seconds will be back to the reverse number')
                    time.sleep(3)
                    return self.get_html(url, timeout, num_entries=num_entries - 1)
                else:  # Use proxy
                    print('wairt to long')
                    pass

        else:
            print('wrong\n')
            pass



def get_pid(url):  #Entry 
    global result_queue
    #Get name
    html = pix.get_html(url, 3).text
    reg = r'</div><h1 class="title">(.*?)</h1><a '
    name = re.findall(reg, html)
    cate='P站画师'.decode('utf-8')
    try:
        result_queue.put((url,name[0],cate))
    except Exception as e:
        print(e)




if __name__=='__main__':
    post_db=DB('Post')           #Main text data
    picture_db=DB('Picture')     #Main pictures data
    url_queue=LifoQueue()        #url queue
    result_queue=LifoQueue()     #result queue


    #GET TOP 
    pix = pixiv_day()
    pix.login()
    target_url = host
    pixiv_day_html = pix.get_html(target_url, 3).text
    reg = r'<div class="ranking-image-item"><a href="(.*?)"class="work  _work'
    painter_day_urls = re.findall(reg, pixiv_day_html)  #GET URL

    for painter_url in painter_day_urls:
        url_queue.put(parent + painter_url)                     #Add this picture author to queue
        #print(parent + painter_url)

    print('{} pages waiting for parse'.format(url_queue.qsize()))        

    tasks=[]
    while 1:
        url=url_queue.get()    #GET ONE URL
        #print(url)
        t=Thread(target=get_pid,args=(url,))        #Open on thread
        tasks.append(t) #add to queue
        if url_queue.empty():
            break
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

    x = 1
    while 1:
        url,title,cate=result_queue.get()        #GET data
        
        print(str(url) + str(title) + str(cate))
        works_html = pix.get_html(url, 3).text
        reg = r'<div class="_illust_modal _hidden ui-modal-close-box"><div class="wrapper"><span class="close ui-modal-close"><i class="_icon-12 size-2x _icon-close"></i></span><img alt=".*?" width=".*?" height=".*?" data-src="(.*?)"'
        big_img_url = re.findall(reg, works_html)      #Get pictures url
        if big_img_url == []:  # MORE pictures model
            reg = r'<a href="(.*?)" target="_blank" class=" _work multiple "><div class="_layout-thumbnail"><div class="page-count"><div class="icon">'
            more_url_last = re.findall(reg, works_html)  # get more pictures
            if more_url_last == []:  # if not pictures 
                reg = r'</a><a href="/(.*?)"target="_blank"rel="noopener"class="read-more'
                more_url_last = re.findall(reg, works_html)  # 
            more_img_url = r'http://www.pixiv.net/' + str(more_url_last[0])
            jump_to_html = pix.get_html(more_img_url, 3).text  # 
            reg = r'class="full-size-container _ui-tooltip" data-tooltip=".*?"><i class="_icon-20 _icon-full-size"></i></a><img src=".*?" class="image ui-scroll-view" data-filter="manga-image" data-src="(.*?)" data-index=".*?">'
            big_img_url = re.findall(reg, jump_to_html)  # 
        try:
            print('The ' + str(x) + ' pic is :' + str(big_img_url[0]))
            post_db.insertnew(id=str(x),name=title,poster=big_img_url[0],category=cate,tags=cate,status=False)    #上传文字数据
            print(big_img_url[0])
            picture_db.insertnew(pid=str(x),subid='1',url=str(big_img_url[0]))     #upload data and get data
            x = x + 1
        except:
            print('Error! Pelase connect author in Github : )')
            pass

        if result_queue.empty():
            break
