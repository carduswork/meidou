# -*- coding: utf-8 -*-
import urllib2,urllib,re,mp3play,time
#from win32com.client import Dispatch
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get(keyword):
    #keyword = '君子一言'
    print 'Google Voice',keyword.decode('utf-8')
    keyword = keyword.decode('utf-8')
    '''
    url = 'http://www.baidu.com/baidu?word='+keyword+'&tn=bds&rn=100'
    req=urllib2.Request(url)
    resp=urllib2.urlopen(req)
    html = resp.read()

    hzDict = {}
    pat = re.compile(u'([\u4300-\u9fa5]+)', re.U)
    line = html.decode('utf-8')
    rs = pat.findall(line)
    if rs:
        for word in rs:
            if word in hzDict:
                hzDict[word] += 1
            else:
                hzDict[word] = 1
    keymax = ''
    Dictmax = 0

    for key in hzDict:
        if hzDict[key] > 2 and keyword != key:
            if hzDict[key] > Dictmax:
                keymax = key
                Dictmax = hzDict[key]
    print keymax,Dictmax
    print hzDict[keymax]

    if keyword in keymax:
        keymax = keymax.replace(keyword,'')

    url = 'http://translate.google.cn/translate_tts?'
    Dict = {'ie':'UTF-8',
            'q':keymax.encode('utf-8'),#'驷马难追',
            'tl':'zh-CN',
            'total':'1',
            'idx':'0',
            'textlen':'5',
                }
    '''
    url = 'http://translate.google.cn/translate_tts?'
    Dict = {'ie':'UTF-8',
            'q':keyword.encode('utf-8'),#'驷马难追',
            'tl':'zh-CN',
            'total':'1',
            'idx':'0',
            'textlen':len(keyword),
                }
    Data=urllib.urlencode(Dict)
    print Data
    header = {
            'Referer': 'http://translate.google.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
            'Accept': '*/*',
            'Host': 'translate.google.cn',
            }
    req=urllib2.Request(url,data=Data, headers=header)
    resp=urllib2.urlopen(req)
    html = resp.read()

    mp3 = open('test.mp3','wb')
    mp3.write(html)
    mp3.close()

    return True
'''
    clip = mp3play.load(r'test.mp3')
    clip.play()
    print 'play'
    time.sleep(min(5, clip.seconds()))
    clip.stop()

    mp = Dispatch("WMPlayer.OCX")
    tune = mp.newMedia("test.mp3")
    mp.currentPlaylist.appendItem(tune)
    mp.controls.play()
    #mp.controls.stop()
    '''
if __name__ == "__main__":
    get('starting')
