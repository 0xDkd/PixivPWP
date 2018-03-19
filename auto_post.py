#-*- coding=utf-8 -*-
from uploader import *
from wp_db import *
from localdb import *
import StringIO
import sys
import datetime

tc='flickr' #选择图床，flickr:flickr图床，weibo:微博图床
if tc=='weibo':
    upload=Weibo()
else:
    upload=Flickr()   #使用上传Flickr方法
wp = WPDB() #初始化一个WPDB方法
#wp.create_post(title='测试',content='ojbk',tag=['test','ojbk'],category=['test'],thumbnail='122.png')
local=DB('Post')   #初始化一个DB方法叫local 在localdb里面,使用Post方法


timenow=lambda :datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log(msg):
    print u'{} - {}'.format(timenow(),msg)

load_path = r'./'

def mkdir(path):                              #创建文件夹
    path = path.strip()
    is_exist = os.path.exists(os.path.join(load_path, path))
    if not is_exist:
        print('Establishing ' + path + ' files')
        os.makedirs(os.path.join(load_path, path))
        os.chdir(os.path.join(load_path, path))
        return True
    else:
        print('Name ' + path + ' is already exist')
        os.chdir(os.path.join(load_path, path))
        return False

def postnew(i,content,path,size):   #主要的
    post,pictures=local.get_a_item()  #使用这个对象里面的一个方法 去网站爬取数据 ，主要是post 和pictures，已经有数据了        其中post是文字数据，pictures是图片URL
    if post is None:   #没找到
        log('get no post!')
        return False
    iD = post.id
    print('now ' + iD)
    title=post.name  #文章标题
    category=post.category.split(',')  #文章分类 用逗号隔开
    print(category[0])
    tag=post.tags.split(',') #文章标签
    #thumbnail=post.poster
    log(u'try to post a new post,title {}'.format(title))  #其实就是方便输出
    total=len(pictures)          #就是看有多少张图片
    print(str(i))
    thumnnail_path=None
    for picture in pictures:   # pictures是一种比较特别的数据类型，可以使用picture.url获得图片的url
        if 'sinaimg.cn' in picture.url:  #上传到新浪图床 肯定不会用啦
            wb_img_url=picture.url
        else:
            print(str(picture.url))
            wb_img_url=upload.get_image(picture.url,i,size)     # 下载并上传图片到flickr 返回flickr的链
        print(category[0])
        content +='\n<img src="{pic}" alt="{alt}" title="{title}" />'.format(pic=wb_img_url,alt=category[0].encode('utf-8'),title=category[0].encode('utf-8'))
        if thumnnail_path is None:
            thumnnail_path=wb_img_url
        sys.stdout.write('upload {}/{}\r'.format(i,total))
        sys.stdout.flush()
        if i == size:        #只有相等时才会上传网站数据库
            try:
                title = '【P站日榜】' + path
                wp.create_post(title=title, content=content, tag=tag, category=category)
                local.update(id=post.id, status=True)  # 使用local里面的上传到本地数据库
            except Exception as e:
                print('Error :' + str(e))
    return content



if __name__=='__main__':
    i = 1
    size = input('Please input post pictures numbers:')
    content=''  #文章里面写的内容
    path = datetime.datetime.now().strftime('%Y-%m-%d')  # 现在
    mkdir('pixiv/' + path)  # 创建文件夹
    while 1:
        #try:
        if tc=='weibo':  #没用
            upload._login()   #微博登录，调用upload
        content=postnew(i,content,path,size)   #使用postnew方法 主要的东西
        i += 1
        if content==False:
            time.sleep(3)
        else:
            log('{} create new posts success!'.format(timenow()))
            time.sleep(5)
'''                
        except Exception as e:
            log('error :'+str(e))
            print('\ntry again')
            time.sleep(5)
'''




