# coding=utf-8
import re
import requests
import sys
import urllib
import os
reload(sys)
sys.setdefaultencoding("utf-8")
class Zhihu:
    def __init__(self):
        print "开始抓取知乎日报"
    #抓取网页的数据
    def getSources(self,url):
        html = requests.get(url)
        return html.text
    # 获取单个图片信息里的所有信息
    def getItem(self,html):
        items = re.findall('<div class="box">(.*?)</div>',html,re.S)
        return items
    #获取单个图片信息并解析图片内容
    def getImages(self,item,i,count):
        items = {}
        url="http://daily.zhihu.com"
        items['title']= re.search('<span class="title">(.*?)</span>',item,re.S).group(1)
        items['img']=re.search('<img src="(.*?)"',item,re.S).group(1)
        items['link']=url+re.search('<a href="(.*?)"',item,re.S).group(1)
        self.downloadsImgs(items['img'],i,count)
        return items
    #下载图片
    def downloadsImgs(self,img,i,count):
        print "正在下载:" + str(i) + "/"+str(count)
        web = urllib.urlopen(img, str(i) + ".jpg")
        jpg = web.read();
        file = open("imgs/"+str(i) + ".jpg", "wb")
        file.write(jpg);
        file.close()
    #保存信息到zhihu.txt文件
    def saveInfo(self,infos):
        f=open("file/zhihu.txt","w")
        for each in infos:
            f.writelines(each['title']+'\n')
            f.writelines(each['img']+'\n')
            f.writelines(each['link']+'\n')
        f.close()
if __name__=="__main__":
    zhihu = Zhihu()
    if not os.path.exists("file"):
        print os.mkdir("file")
    if not os.path.exists("imgs"):
        print os.mkdir("imgs")
    url="http://daily.zhihu.com/"
    html = zhihu.getSources(url)
    items = zhihu.getItem(html)
    count = len(items)
    infos=[]
    i=0;
    for each in items:
        i=i+1
        info = zhihu.getImages(each,i,count)
        infos.append(info)
    print "知乎日报信息抓取完毕，正在保存信息"
    zhihu.saveInfo(infos)
    print "保存完毕"
