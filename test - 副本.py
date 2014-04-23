# -*- coding: utf-8 -*-
import urllib,urllib2
import GetCacheCookies
baidu_cookie = GetCacheCookies.getcachecookies('.baidu.com')
true = True
null = None
false = False
for i in baidu_cookie:
    url = 'http://tieba.baidu.com/f/user/json_userinfo'
    header = {
            'Cookie': baidu_cookie[i],
            'Referer': 'http://tieba.baidu.com/',
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
            }
    req = urllib2.Request(url,headers=header)
    res = urllib2.urlopen(req,timeout = 3).read()
    exec('data='+res)
    print res
    if data['no'] != 0:
        print u'cookies 错误'
        del baidu_cookie[i]
    else:
        print i,u'cookie 有效'
        print data['data']['session_id']
        print data['data']['user_portrait']
        print data['data']['user_name_weak']
        print data['data']['user_is_verify']
        print data['data']['is_login']
        print data['data']['weak_pwd']
        print data['data']['is_half_user']
        print data['data']['source_id']
        print data['data']['no_un']
        print data['data']['mobilephone']
        print data['data']['email']
        print data['data']['open_uid']
        print data['data']['client_msg_count']
        print data['data']['user_open_space']

        
