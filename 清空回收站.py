# -*- coding:utf-8 -*-  
from winlib import shell,shellcon  
 
def QueryRecycle():  
    total_size, file_count = shell.SHQueryRecycleBin('')  
    return total_size,file_count  
 
def EmptyRecycle():  
    try:  
        shell.SHEmptyRecycleBin(None,None,  
                shellcon.SHERB_NOCONFIRMATION |  
                shellcon.SHERB_NOPROGRESSUI |  
                shellcon.SHERB_NOSOUND)  
    except shell.error:  
        pass 
 
def RemoveToRecycle(path):  
    try:  
        shell.SHFileOperation((0,  
                shellcon.FO_DELETE,  
                path,  
                None,  
                shellcon.FOF_SILENT |  
                shellcon.FOF_ALLOWUNDO |   
                shellcon.FOF_NOCONFIRMATION,  
                None,  
                None 
                ))  
    except shell.error:  
        pass 
 
if __name__=='__main__':  
    s,c = QueryRecycle()  #查询回收站
    print s,c
    if c > 0:  #若不为空
        EmptyRecycle()  #清空回收站
        print '%d files %.2f KB' % (c,s/1024.0)
    else:
        print u'空'
