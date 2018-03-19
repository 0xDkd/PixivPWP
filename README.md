# PixivPWP

Hi,this is an simple tool to reduce the pressure of your manage your websit content~

## Instructions：

We used the main code of ![this program](https://github.com/tangrela/k1kmz) to achieve the function of acquiring N images of the pixiv daily TOP list. Here I pay tribute to the original author.
---
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
[![License](https://poser.pugx.org/hfo4/cloudreve/license)](https://packagist.org/packages/hfo4/cloudreve)
