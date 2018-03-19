# PixivPWP

Hi,this is an simple tool to reduce the pressure of your manage your websit content~

## Instructions

We used the main code of ![this program](https://github.com/tangrela/k1kmz) to achieve the function of acquiring N images of the pixiv daily TOP list. Here I pay tribute to the original author.

If you want to use this program, you should use the following steps to use
1. Your must install python ,it is important!
2. ```git clone git@github.com:aimerforreimu/PixivPWP.git```
3. ```cd PixivPWP ```
4. ```pip install -r requirement.txt ```
5. Edit ```uploader.py ``` in 109 line to your token and id
6. Edit ```wp_db.py``` in 18l line to your wordpress site info
7. ```python pixivDay.py``` 
8. ```python auto_post.py``` put in some number , then wait it stop ,chekout your wordpress site , you will fell amazing  (just a joke) 

ENJOY IT! :)

## Precautions：
1. Your host mysql must open 3306 or other remote connect port!
2. If pip install error , your need to try another way or try to use search engine！
3. Maybe it will be very slowly if your host is in chian. This issue I can't fix .So I suggest you use a foreign server.

## LICENSE 
GPL V3

#中文说明

嗯哼，这是一个python小工具，用来减轻你对你网站内容的负担，也就说，这个工具可以自动采集pixiv上面的TOP150榜，然后发不到你的网站上面，如果你想的话，还可以改变各种参数来做到个性化这个小工具。

## 说明

我们使用了![这个项目](https://github.com/tangrela/k1kmz)的大部分的代码来实现这个项目的功能，向原作者致敬！

如果你想要使用这个小程序，你需要按照一下的步骤进行
1.首先，你必须要要有python环境，这是最重要的！

2. ```git clone git@github.com:aimerforreimu/PixivPWP.git```

3. ```cd PixivPWP ```

4. ```pip install -r requirement.txt ```

5. 编辑```uploader.py ``` 中的109行，添写你自己的id和token

6. Edit ```wp_db.py``` 中的18行，让他成为你自己的wordpress相关信息

7. ```python pixivDay.py``` 

8. ```python auto_post.py``` 填入你想要发布到你自己网站的图片，然后等程序结束以后，检查一下你网站的文章，你会感到很神奇（滑稽）


ENJOY IT! :)

## 注意事项
1.你的主机必须打开3306端口，或者其他远程连接mysql的端口
2.如果你使用```pip install ``` 的时候出现了错误，请自行百度
3.如果你的服务器在国内，这个程序的进度可能会变的很慢，很抱歉，原因你懂。

