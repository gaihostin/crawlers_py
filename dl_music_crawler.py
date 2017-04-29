#!/usr/bin/python
#-*- coding:utf-8 -*-


import requests
import urllib
import urllib2
import json
import sys
import time


def download(url, name):
    try:
        req = urllib2.Request(url)
        req.add_header('User-agent', 'Mozilla 5.10')
        data = urllib2.urlopen(req).read()
        with open(name + '.mp3', 'wb') as file:
            file.write(data)
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print "Error, code:", e.code
        elif hasattr(e, 'reason'):
            print "Reason", e.reason
        else:
            print 'Noexception'

def crawl_music(word):
    res1 = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='+word)
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']['song']['list']
    mids = []
    songmids = []
    srcs = []
    songnames = []
    singers = []
    songids = []
    songIdmap = {}
    for j in jm1:
        try:
            mids.append(j['media_mid'])
            songmids.append(j['songmid'])
            songnames.append(j['songname'])
            songids.append(j['songid'])
            singers.append(j['singer'][0]['name'])
            songIdmap[j['songid']] = j['songname']
        except:
            print('wrong')
    url_src = "http://ws.stream.qqmusic.qq.com/{0}.m4a?fromtag=46"
    for id in songids:
        url = url_src.format(id)
        print "begin download....%s"%url
        download(url, songIdmap[id])

if __name__ == '__main__':
    word = '周杰伦'
    crawl_music(word)
    word = 'taylor swift'
    crawl_music(word)
