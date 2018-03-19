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
    def __init__(self):  #初始化数据
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.main_url = 'http://www.pixiv.net'
        self.headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.pixiv_id = '2634764739@qq.com'
        self.password = 'huanye520'
        self.post_key = []  #存post信息的操作钥匙（登录信息）
        self.return_to = 'http://www.pixiv.net/'


    def login(self):        #登录代码
        post_key_html = se.get(self.base_url, headers=self.headers).text  #获得登录页面（喊输入框）的HTML代码
        post_key_soup = BeautifulSoup(post_key_html, 'html.parser') #使用Python自带的解析库
        self.post_key = post_key_soup.find('input')['value']# 捕获postkey #找到input对应的
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        } #所有登录信息存储为data
        se.post(self.login_url, data=data, headers=self.headers)


    def get_html(self, url, timeout, proxy=None, num_entries=5):  # proxy为代理，有的话就使用上面的代码
        if proxy is None:
            try:
                return se.get(url, headers=self.headers, timeout=timeout)  # 没有代理proxy
            except:
                if num_entries > 0:
                    print('Access to a web page error', num_entries, ' seconds will be back to the reverse number')
                    time.sleep(3)
                    return self.get_html(url, timeout, num_entries=num_entries - 1)
                else:  # 5次都不好使的话就使用代理，感觉使用代理基本遇不到
                    print('wairt to long')
                    pass

        else:
            print('wrong\n')
            pass



def get_pid(url):  #进入一个画师里面,获得作品名字
    global result_queue
    #获得名字
    html = pix.get_html(url, 3).text
    reg = r'</div><h1 class="title">(.*?)</h1><a '
    name = re.findall(reg, html)
    cate='P站画师'.decode('utf-8')
    try:
        result_queue.put((url,name[0],cate))
    except Exception as e:
        print(e)




if __name__=='__main__':
    post_db=DB('Post')           #主要的存文字数据
    picture_db=DB('Picture')     #主要存图片数据
    url_queue=LifoQueue()        #url 队列
    result_queue=LifoQueue()     #结果队列


    #获得当天的上榜画师的作品
    pix = pixiv_day()
    pix.login()
    target_url = host
    pixiv_day_html = pix.get_html(target_url, 3).text
    reg = r'<div class="ranking-image-item"><a href="(.*?)"class="work  _work'
    painter_day_urls = re.findall(reg, pixiv_day_html)  #已经获得url

    for painter_url in painter_day_urls:
        url_queue.put(parent + painter_url)                     #将当前上榜画师的url加入队列
        #print(parent + painter_url)

    print('{} pages waiting for parse'.format(url_queue.qsize()))        #到这里一点问题没有

    tasks=[]
    while 1:
        url=url_queue.get()    #取队列里面的一个url
        #print(url)
        t=Thread(target=get_pid,args=(url,))        #开启一个线程
        tasks.append(t) #加入任务队列
        if url_queue.empty():
            break
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

    x = 1
    while 1:
        url,title,cate=result_queue.get()        #取队列里面的一套url,title,cate
        #这里得试试好使不
        print(str(url) + str(title) + str(cate))
        works_html = pix.get_html(url, 3).text
        reg = r'<div class="_illust_modal _hidden ui-modal-close-box"><div class="wrapper"><span class="close ui-modal-close"><i class="_icon-12 size-2x _icon-close"></i></span><img alt=".*?" width=".*?" height=".*?" data-src="(.*?)"'
        big_img_url = re.findall(reg, works_html)      #可以获得图片url
        if big_img_url == []:  # 如果原图没找到，说明有更多图片
            reg = r'<a href="(.*?)" target="_blank" class=" _work multiple "><div class="_layout-thumbnail"><div class="page-count"><div class="icon">'
            more_url_last = re.findall(reg, works_html)  # 包含更多图片，正在获取更多图片url
            if more_url_last == []:  # 如果按上面的规则没找到更多图片，说明是漫画，规则变更
                reg = r'</a><a href="/(.*?)"target="_blank"rel="noopener"class="read-more'
                more_url_last = re.findall(reg, works_html)  # 正在获取漫画规则更多图片的url
            more_img_url = r'http://www.pixiv.net/' + str(more_url_last[0])
            jump_to_html = pix.get_html(more_img_url, 3).text  # 获取更多图片的url
            reg = r'class="full-size-container _ui-tooltip" data-tooltip=".*?"><i class="_icon-20 _icon-full-size"></i></a><img src=".*?" class="image ui-scroll-view" data-filter="manga-image" data-src="(.*?)" data-index=".*?">'
            big_img_url = re.findall(reg, jump_to_html)  # 获得原图url成功
        try:
            print('The ' + str(x) + ' pic is :' + str(big_img_url[0]))
            post_db.insertnew(id=str(x),name=title,poster=big_img_url[0],category=cate,tags=cate,status=False)    #上传文字数据
            print(big_img_url[0])
            picture_db.insertnew(pid=str(x),subid='1',url=str(big_img_url[0]))     #上传图片数据 ID 和 图片的url
            x = x + 1
        except:
            print('Error  ni dong de')
            pass

        if result_queue.empty():
            break