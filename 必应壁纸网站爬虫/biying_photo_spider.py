# Author:YFAN
import requests
import lxml.etree
from time import sleep
import os

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    #",referer": "https://www.mzitu.com/tag/ugirls/"
}
#获取页面总数
def getpage(url):
    #1 请求数据
    response = requests.get(url, headers=headers)
    #2 整理成xml文档
    xml = lxml.etree.HTML(response.text)
    #3 抽取想要的element 以下是获取类名为page的div标签下的span标签体内容 获取到的内容为：1 / 99
    page = xml.xpath('//div[@class="page"]/span')#<div class="page"><a href="/">上一页</a><span>1 / 99</span><a href="/?p=2">下一页</a></div>
    #4 通过对字符串分割操作来获取必应壁纸网页页数
    str=page[0].text.split(' ')[2]
    return (int)(str)

#遍历页面
def foreachurlpages(url,page,pages,path):
    i=page
    while i<=pages:
        temp=url+"?p={i}".format(i=i)
        print("第{page}页开始下载，当前页url：{url}".format(page=i,url=temp))
        count=foreachImage(temp,path)
        print("第{page}页已下载完成".format(page=i))
        i=i+1
        if (count == 0):
            print("网络出现错误，第{page}页重新下载")
            i=i-1
        os.system('cls')


def foreachImage(url,path):
    response = requests.get(url, headers=headers)
    xml = lxml.etree.HTML(response.text)
    imgname = xml.xpath('//div[@class="description"]/h3')
    imgurl = xml.xpath('//div[@class="card progressive"]/a')
    print("当前页面有{}张壁纸".format(len(imgurl)))
    count = 0
    for n, u in zip(imgname, imgurl):
        name = n.text.split(' ')[0]
        url = getRealImgUrl(u.xpath('@href')[0])#u.xpath('@src')[0]
        count += 1
        # 拼接链接
        # url = url[0:-21] + '1920x1080.jpg?imageslim'
        print("第{}张壁纸 描述：{}  壁纸url：{}".format(count,name,url))
        download(name,url,path)
    return count

# 获取真实图片url链接
def getRealImgUrl(url):
    url = 'https://bing.ioliu.cn' + url
    response = requests.get(url, headers=headers)
    xml = lxml.etree.HTML(response.text)
    element = xml.xpath('//img[@data-progressive]')[0]
    return element.attrib['data-progressive']


def download(name,url,path):
    response = requests.get(url, headers=headers)  # 反爬虫，模拟浏览器提交
    # 休眠
    sleep(2)
    NAME=""
    for i in range(len(name)):
        if name[i] not in '/\*:"?<>|':
            NAME+=name[i]
    filename = path +'\\'+ NAME + ".jpg"
    with open(filename, "wb") as f:
        f.write(response.content)
        f.close()

if __name__ == '__main__':
    url="https://bing.ioliu.cn/"#壁纸网页url
    pages=getpage(url)#获取页面总数，并且转换为int类型
    print("壁纸总页数：{pages}".format(pages=pages))#打印必应壁纸页数
    path = input("输入图片存储路径：")
    page=(int)(input("从第几页开始下载（1-{}）：".format(pages)))
    if page<=0 or page>pages:
        print("页数不在范围内")
        print("3秒后退出")
        sleep(1)
        print("2秒后退出")
        sleep(1)
        print("1秒后退出")
        sleep(1)
    else:
        foreachurlpages(url,page,pages,path)
        print("下载完成")
        print("3秒后退出")
        sleep(1)
        print("2秒后退出")
        sleep(1)
        print("1秒后退出")
        sleep(1)
