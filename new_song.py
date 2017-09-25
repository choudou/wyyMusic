# -*- coding:utf-8 -*-
"""
获取所有的歌手信息
"""
import requests
import urlparse
import re
from pythonDB import DB
from bs4 import BeautifulSoup
from lxml import etree
import time,sys,Queue
import logging
import random
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(filename='logger.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
Albums = []
Songs = []
# 头部信息
headers = {
    'Host':"music.163.com",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
    'Content-Type':"application/x-www-form-urlencoded",
    'Cookie':"_ntes_nnid=754361b04b121e078dee797cdb30e0fd,1486026808627; _ntes_nuid=754361b04b121e078dee797cdb30e0fd; JSESSIONID-WYYY=yfqt9ofhY%5CIYNkXW71TqY5OtSZyjE%2FoswGgtl4dMv3Oa7%5CQ50T%2FVaee%2FMSsCifHE0TGtRMYhSPpr20i%5CRO%2BO%2B9pbbJnrUvGzkibhNqw3Tlgn%5Coil%2FrW7zFZZWSA3K9gD77MPSVH6fnv5hIT8ms70MNB3CxK5r3ecj3tFMlWFbFOZmGw%5C%3A1490677541180; _iuqxldmzr_=32; vjuids=c8ca7976.15a029d006a.0.51373751e63af8; vjlast=1486102528.1490172479.21; __gads=ID=a9eed5e3cae4d252:T=1486102537:S=ALNI_Mb5XX2vlkjsiU5cIy91-ToUDoFxIw; vinfo_n_f_l_n3=411a2def7f75a62e.1.1.1486349441669.1486349607905.1490173828142; P_INFO=m15527594439@163.com|1489375076|1|study|00&99|null&null&null#hub&420100#10#0#0|155439&1|study_client|15527594439@163.com; NTES_CMT_USER_INFO=84794134%7Cm155****4439%7Chttps%3A%2F%2Fsimg.ws.126.net%2Fe%2Fimg5.cache.netease.com%2Ftie%2Fimages%2Fyun%2Fphoto_default_62.png.39x39.100.jpg%7Cfalse%7CbTE1NTI3NTk0NDM5QDE2My5jb20%3D; usertrack=c+5+hljHgU0T1FDmA66MAg==; Province=027; City=027; _ga=GA1.2.1549851014.1489469781; __utma=94650624.1549851014.1489469781.1490664577.1490672820.8; __utmc=94650624; __utmz=94650624.1490661822.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; playerid=81568911; __utmb=94650624.23.10.1490672820",
    'Connection':"keep-alive",
    'Referer':'http://music.163.com/'
}

def get_album(url, singer_id, nextflag=0):
    params = {'id': singer_id}
    if nextflag==0:
        r = requests.get(url, params=params)
    else:
        r = requests.get(url)
    # 网页解析
    selector=etree.HTML(r.text)
    # 获取歌手图片
    img = selector.xpath('//div[@class="n-artist f-cb"]/img/@src')

    # 获取专辑信息
    singer_name = selector.xpath('//h2[@id="artist-name"]/text()')[0] if len(selector.xpath('//h2[@id="artist-name"]/text()'))>0 else None
    albumLists = selector.xpath('//ul[@id="m-song-module"]/li')
    for a in albumLists:
        album_name = a.xpath('./div/@title')[0] if len(a.xpath('./div/@title'))>0 else None
	album_date = a.xpath('./p/span[@class="s-fc3"]/text()')[0] if len(a.xpath('./p/span/text()'))>0 else None
	album_id = a.xpath('./div/a[@class="icon-play f-alpha"]/@data-res-id')[0] if len(a.xpath('./div/a[@class="icon-play f-alpha"]/@data-res-id'))>0 else None
        album_img = a.xpath('./div/img/@src')[0] if len(a.xpath('./div/img/@src'))>0 else None
	if album_cid and album_name and singer_name and album_date:
	    logging.info([album_id, album_name, singer_name, album_img, album_date])
	    Albums.append({'album_id':album_id, 'album_name':album_name, 'album_date':album_date, 'singer_name':singer_name, 'singer_id':singer_id})

    time.sleep(10)
    # 翻页
    next = selector.xpath('//a[@class="zbtn znxt"]/@href')
    if next and next[0] != 'javascript:void(0)':
        url =  urlparse.urljoin(r.url, next[0])
        get_album(url, singer_id, 1)

def save_song(url, album):
    params = {'id': album.album_id}
    r = requests.get(url, params=params)

    # 网页解析
    selector=etree.HTML(r.text)

    # 获取专辑信息
    #singer_name = selector.xpath('//p[@class="intr"]/span/@title')[0] if len(selector.xpath('//p[@class="intr"]/span/@title'))>0 else None
    #album_name = selector.xpath('//h2[@class="f-ff2"]/text()')[0] if len(selector.xpath('//h2[@class="f-ff2"]/text()'))>0 else None
    songLists = selector.xpath('//ul[@class="f-hide"]/li')
    for s in songLists:
        song_name = s.xpath('./a/text()')[0] if len(s.xpath('./a/text()'))>0 else None
	song_id = s.xpath('./a/@href')[0] if len(s.xpath('./a/@href'))>0 else None
        result = re.match('.*?(\d+)',song_id)
        if result:
            song_id = result.groups(1)[0]
        if song_id != None and song_name != None:
            Songs.append('song_id':song_id, 'song_name':song_name, 'album_id':album.album_id, 'album_name':album.album_name, 'singer_id':album.singer_id, 'singer_name':album.singer_name, 'album_date':album.album_date)
            logging.info(str(song_id)+'--'+song_name)
        else:
            logging.info(str(album.album_id)+'-- not exist')

second_param = "010001" # 第二个参数
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"

# 获取参数
def get_params(page): # page为传入页数
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): # 如果为第一页
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
        "params": params,
            "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data,proxies = proxies)
    return response.content

# 抓取热门评论，返回热评列表
def get_hot_comments(url):
    hot_comments_list = []
    hot_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n")
    params = get_params(1) # 第一页
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    hot_comments = json_dict['hotComments'] # 热门评论
    print("共有%d条热门评论!" % len(hot_comments))
    print hot_comments
    for item in hot_comments:
        comment = item['content'] # 评论内容
        likedCount = item['likedCount'] # 点赞总数
        comment_time = item['time'] # 评论时间(时间戳)
        userID = item['user']['userId'] # 评论者id
        nickname = item['user']['nickname'] # 昵称
        avatarUrl = item['user']['avatarUrl'] # 头像地址
        comment_info = unicode(userID) + u" " + nickname + u" " + avatarUrl + u" " + unicode(comment_time) + u" " + unicode(likedCount) + u" " + comment + u"\n"
        hot_comments_list.append(comment_info)
        with codecs.open(u"晴天hot.txt",'a',encoding='utf-8') as f:
                f.writelines(comment_info)
    return hot_comments_list


if __name__ == '__main__':

    singer_id = 6452
    get_album_url = 'http://music.163.com/artist/album'
    get_album(get_album_url, singer_id, 0)

    get_song_url = 'http://music.163.com/album'
    for album in Albums:
        save_song(get_song_url, album)
    #sleeptime = random.randint(0, 10)
    #time.sleep(sleeptime)
