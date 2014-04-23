# -*- coding: utf-8 -*-
import os,sqlite3,pythoncom,urllib2,urllib
#from win32com.shell import shell, shellcon
from winlib import shell, shellcon
COOKIE = {}
true = True
null = None
false = False

def get_special_folder_path(path_name):
    for maybe in """
        CSIDL_COMMON_STARTMENU CSIDL_STARTMENU CSIDL_COMMON_APPDATA
        CSIDL_LOCAL_APPDATA CSIDL_APPDATA CSIDL_COMMON_DESKTOPDIRECTORY
        CSIDL_DESKTOPDIRECTORY CSIDL_COMMON_STARTUP CSIDL_STARTUP
        CSIDL_COMMON_PROGRAMS CSIDL_PROGRAMS CSIDL_PROGRAM_FILES_COMMON
        CSIDL_PROGRAM_FILES CSIDL_FONTS""".split():
        if maybe == path_name:
            csidl = getattr(shellcon, maybe)
            return shell.SHGetSpecialFolderPath(0, csidl, False)
    raise ValueError, "%s is an unknown path ID" % (path_name,)

def GetpathFromLink(lnkpath):
    pythoncom.CoInitialize()
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Load(lnkpath)
    path = shortcut.GetPath(shell.SLGP_SHORTPATH)[0]
    return path

#query values from table  
def query_values(conn,table_name): 
    cu = conn.cursor() 
  
    try: 
        cu.execute('select * from %s' %table_name) 
    except sqlite3.Error,e: 
        print 'query data failed:',e.args[0] 
        return
    return cu.fetchall()

def readChromeCookies(db_name,host):
    conn = sqlite3.connect(db_name)
    #解决编码问题
    conn.text_factory = str
    allcookie = []
    for i in query_values(conn,'cookies'):
        if host == i[1]:
            allcookie.append(i[2]+'='+i[3])
    conn.close()
    COOKIE['chrome'] = ';'.join(allcookie)

def readFirefoxCookies(db_name,host):
    try:
        from pysqlite2 import dbapi2 as sqlite3
        conn = sqlite3.connect(db_name)
        #解决编码问题
        conn.text_factory = str
        allcookie = []
        for i in query_values(conn,'moz_cookies'):
            if host == i[6]:
                allcookie.append(i[4]+'='+i[5])
            conn.close()
        COOKIE['firefox'] = ';'.join(allcookie)
    except:print 'load pysqlite2 fail'
    
def read360seCookies(path,host):
    path = path.replace(r'APPLIC~1\360se.exe',r'User Data\Default\Cookies').replace(r'Application\360se.exe',r'User Data\Default\Cookies')
    if os.path.isfile(path):
        conn = sqlite3.connect(path)
        #解决编码问题
        conn.text_factory = str
        allcookie = []
        for i in query_values(conn,'cookies'):
            if host == i[1]:
                allcookie.append(i[2]+'='+i[3])
        conn.close()
        COOKIE['360se'] = ';'.join(allcookie)
        
def getcachecookies(host):
    if os.path.isfile(os.getenv('LOCALAPPDATA')+'\\Google\\Chrome\\User Data\\Default\\Cookies'):
        readChromeCookies(os.getenv('LOCALAPPDATA')+'\\Google\\Chrome\\User Data\\Default\\Cookies',host)

        
    rootdir = os.getenv('APPDATA')+'\\Mozilla\\Firefox\\Profiles'
    for parent,dirnames,filenames in os.walk(rootdir):
        for dirname in  dirnames:
            if '.default' in dirname:
                if os.path.isfile(parent+'\\'+dirname+'\\cookies.sqlite'):
                    readFirefoxCookies(parent+'\\'+dirname+'\\cookies.sqlite',host)

    Explorlist = ('firefox.exe','chrome.exe',
                  '360se.exe','360chrome.exe',
                  '360CHR~1.EXE',)

    for parent,dirnames,filenames in os.walk(get_special_folder_path("CSIDL_COMMON_STARTMENU")):
        for filename in filenames:
            if os.path.splitext(os.path.join(parent,filename))[1][1:] == 'lnk':
                exepath = GetpathFromLink(os.path.join(parent,filename))
                for i in Explorlist:
                    if i in exepath:
                        if '360se.exe' == i:read360seCookies(exepath,host)

    for parent,dirnames,filenames in os.walk(get_special_folder_path("CSIDL_PROGRAMS")):
        for filename in filenames:
            if os.path.splitext(os.path.join(parent,filename))[1][1:] == 'lnk':
                exepath = GetpathFromLink(os.path.join(parent,filename))
                for i in Explorlist:
                    if i in exepath:
                        if '360se.exe' == i:read360seCookies(exepath,host)


    return COOKIE

def getTiebaCount():
    countGroup = []
    num = 0#;exits = 1
    baidu_cookie = getcachecookies('.baidu.com')
    for i in baidu_cookie:
        url = 'http://tieba.baidu.com/f/user/json_userinfo'
        header = {
                'Cookie': baidu_cookie[i],
                'Referer': 'http://tieba.baidu.com/',
                'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
                }
        req = urllib2.Request(url,headers=header)
        res = urllib2.urlopen(req,timeout = 3).read()
        #print res
        exec('data='+res)
        if data['no'] != 0:
            print u'cookies 错误'
            del baidu_cookie[i]
            break
        else:
            if data['data']['is_login']:
                print i,u'cookie 有效'
                '''
                for t in countGroup:
                    print data['data']['user_name_weak'],t[0]
                    if data['data']['user_name_weak'] == t[0]:
                        exits = 0
                ''' 
                data2 = []
                data2.append(data['data']['user_name_weak'])
                data2.append('http://tb.himg.baidu.com/sys/portrait/item/'+data['data']['user_portrait'])
                data2.append(baidu_cookie[i])
                countGroup.append(data2)
                num += 1
    result = []
    [result.append(i) for i in countGroup if not i in result]
    return result

if __name__=="__main__":
    #print getcachecookies('.baidu.com')
    print getTiebaCount()
