# -*- coding: utf-8 -*- 
import urllib2,urllib
import cookielib

#f = open("cookies.txt","r")
cookie = '''['BAIDUID=69024D1AF52F837A0BD8F1B7009118CF:FG=1', 'H_PS_TIPFLAG=O', 'H_PS_TIPCOUNT=1', 'BDUSS=k5eEt6RUFKdzVMSDdISjdZSnFoUm9oNXZ4VXhnd0NXb2Y3ZDl4N2dRbmtLRFJUQVFBQUFBJCQAAAAAAAAAAAEAAACJTX0hZ3BoMTU5ODIxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOSbDFPkmwxTTE', 'BDSVRTM=97', 'H_PS_PSSID=4684_5067_1465_5186_5224_5213_4264_4759_5243']'''
cookies = cookie.replace("', '","; ").replace("['","").replace("']","")
hearder = {'cookie': cookies,}
req=urllib2.Request("http://wapp.baidu.com/",headers = hearder)
resp=urllib2.urlopen(req)
print resp.read()
