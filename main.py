# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, Qt
from configobj import ConfigObj
import os,sys,time,threading,os,urllib2,microphone,string

class Nvpu(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Nvpu,self).__init__(parent)
        #隐藏窗口边框、背景、任务栏
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        #窗口透明度
        self.setWindowOpacity(0.9)
        #载入数据
        self.Config_read()

        #主人格图片
        self.btn_min=labelBtn("main")
        self.btn_min.setParent(self)
        self.btn_min.move(100,100)
        self.btn_min.setPixmap(QtGui.QPixmap("shell/surface1.png"))
        
        #设置窗口位置
        desktop =QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        
        if not "firstboot" in self.sys_dict:
            self.move(width-400,height-400)
            self.sys_dict["firstboot"] = "1"
        else:
            self.move(int(self.sys_dict["nvpu_pos_x"]),int(self.sys_dict["nvpu_pos_y"]))

        self.MakeBtn()
        self.Alttime = 0
        self.sys_dict['NvpuHide'] = 0

        '''# 创建托盘
        self.icon = QIcon("shell/icon.png")
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip(u"女仆酱")
        self.trayIcon.show()
        # 托盘气泡消息
        self.trayIcon.showMessage(u"美豆酱", u"女仆酱已开启")
        # 托盘菜单
        self.action = QtGui.QAction(u"退出", self)#, triggered = self.out())#sys.exit)
        self.menu = QMenu(self)
        self.menu.addAction(self.action)
        self.trayIcon.setContextMenu(self.menu)
        #创建表情转换线程
        self.thread = MyThread()
        self.thread.ChangeS.connect(self.change)
        self.thread.start()'''
        #创建语音识别会话
        #self.SessionNum = 0
        #self.NewSession()


    def mouseReleaseEvent(self,event):
        global Flat
        Flat = 0
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            global Flat
            Flat = 1
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        if event.button() == QtCore.Qt.RightButton:
            if "btnClicked" in self.sys_dict and self.sys_dict["btnClicked"] != "1":
                for btn in self.BtnList:
                    btn.show()
                self.sys_dict["btnClicked"] = "1"
            else:
                for btn in self.BtnList:
                    btn.hide()
                self.sys_dict["btnClicked"] = "0"

    def mouseMoveEvent(self,event):
        try:
            if Flat and (event.buttons() == QtCore.Qt.LeftButton):
                self.move(event.globalPos() - self.dragPosition)
        except:pass
        
    def keyReleaseEvent(self, event):
         if event.key() == QtCore.Qt.Key_Escape :
             self.out()
             
    def change(self,Surface_path):
        self.btn_min.setPixmap(QtGui.QPixmap(Surface_path))
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())

    #关闭前事宜
    def out(self):
        #删除WAV缓存
        for file in os.listdir("wav"):
            try:
                os.remove("wav/"+file)
            except:pass
        #保存INI数据    
        self.Config_write()
        #关闭
        self.close
        sys.exit()

    #INI文件保存--用法self.Config_write()
    def Config_write(self):

        #记录人格位置
        self.sys_dict["nvpu_pos_x"] = self.pos().x()
        self.sys_dict["nvpu_pos_y"] = self.pos().y()
        
        for i in self.sys_dict:
            self.sys_ini[i] = self.sys_dict[i]
        self.sys_ini.write()

    #INI文件读取--用法self.sys_dict[]--有时间写成块
    def Config_read(self):
        self.sys_dict = {}
        self.sys_ini = ConfigObj("ini/sys.ini")
        for key in self.sys_ini.keys():
            print key," = ",self.sys_ini[key]
            self.sys_dict[key] = self.sys_ini[key]
            
        self.shell_dict = {}
        self.shell_ini = ConfigObj("ini/shell.ini")
        for key in self.shell_ini.keys():
            print key," = ",self.shell_ini[key]
            self.shell_dict[key] = self.shell_ini[key]

        
    #新建录音会话
    def NewSession(self):
        self.SessionNum = self.SessionNum+1
        exec('self.SessionName' + str(self.SessionNum) + '= speech_recognize()')
        exec('self.SessionName' + str(self.SessionNum) + '.NewSession.connect(self.NewSession)')
        exec('self.SessionName' + str(self.SessionNum) + '.ResultNum=self.SessionNum')
        exec('self.SessionName' + str(self.SessionNum) + '.start()')

    def MakeBtn(self):
        self.BtnNameList = ('shutdown_btn','tools_btn','skills_btn','info_btn','programs_btn','msg_btn')
        self.CircularNameList = ('Circular_RightTop','Circular_LeftBottom','Circular_RightMidde','Circular_RightBottom','Circular_LeftTop','Circular_LeftMidde')

        for name in self.CircularNameList:
            print name+' create'
            exec('self.' + name + '=labelBtn("' + name + '","1")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(r"' + self.shell_dict[name] + '"))')
            
        for name in self.BtnNameList:
            print name+' create'
            exec('self.' + name + '=labelBtn("' + name + '")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(r"' + self.shell_dict[name+'_normal'] + '"))')

        self.BtnList = (self.shutdown_btn,self.tools_btn,self.skills_btn,self.info_btn,self.programs_btn,self.msg_btn)
        self.CircularList = (self.Circular_LeftBottom,self.Circular_RightTop,self.Circular_RightMidde,self.Circular_RightBottom,self.Circular_LeftTop,self.Circular_LeftMidde) 
        for btn in self.BtnList + self.CircularList:
            btn.Clicked.connect(self.BtnCLICK)
            btn.Entered.connect(self.BtnENTER)
            btn.Leaved.connect(self.BtnLEAVE)
            btn.hide()

    def BtnCLICK(self,name):
        if name == "shutdown_btn":
            self.out()
        print name+" clicked"

    def BtnENTER(self,name):
        if str(name) == "tools_btn":
            self.Circular_LeftBottom.show()
            self.Circular_LeftBottom.timer.stop()
        elif str(name) == 'skills_btn':
            self.Circular_RightTop.show()
            self.Circular_RightTop.timer.stop()
        elif str(name) == 'msg_btn':
            self.Circular_RightMidde.show()
            self.Circular_RightMidde.timer.stop()
        elif str(name) == 'shutdown_btn':
            self.Circular_RightBottom.show()
            self.Circular_RightBottom.timer.stop()
        elif str(name) == 'programs_btn':
            self.Circular_LeftTop.show()
            self.Circular_LeftTop.timer.stop()
        elif str(name) == 'info_btn':
            self.Circular_LeftMidde.show()
            self.Circular_LeftMidde.timer.stop()
        else:pass
        
        if str(name) in self.CircularNameList:
            exec('self.' + str(name) + '.show()')
            exec('self.' + str(name) + '.timer.stop()')

        if str(name) in self.BtnNameList:
            exec('self.' + str(name) + '.setPixmap(QtGui.QPixmap(r"' + self.shell_dict[str(name+'_hover')] + '"))')
            print name+" entered"

    def BtnLEAVE(self,name):
        if str(name) in self.CircularNameList:
            exec('self.' + str(name) + '.timer.start()')
 
        if str(name) in self.BtnNameList:
            exec('self.' + str(name) + '.setPixmap(QtGui.QPixmap(r"' + self.shell_dict[str(name+'_normal')] + '"))')
            print name+" leaved"
            if str(name) == "tools_btn":
                self.Circular_LeftBottom.timer.start()
            elif str(name) == 'skills_btn':
                self.Circular_RightTop.timer.start()
            elif str(name) == 'msg_btn':
                self.Circular_RightMidde.timer.start()
            elif str(name) == 'shutdown_btn':
                self.Circular_RightBottom.timer.start()
            elif str(name) == 'programs_btn':
                self.Circular_LeftTop.timer.start()
            elif str(name) == 'info_btn':
                self.Circular_LeftMidde.timer.start()
            else:pass
            
    def KeyHide(self):
        if self.sys_dict['NvpuHide'] == 0:
            self.hide()
            self.sys_dict['NvpuHide'] = 1
        else:
            self.show()
            self.resize(500,500)
            self.sys_dict['NvpuHide'] = 0
            

        
'''class MyThread(QtCore.QThread):
    ChangeS = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(MyThread,self).__init__(parent)
    def run(self):
        while 1:
            time.sleep(0.1)
            self.ChangeS.emit("shell//D2.png")
            time.sleep(0.1)
            self.ChangeS.emit("shell//D1.png")'''


    
#QLabel图片类
class labelBtn(QtGui.QLabel):
    Clicked = QtCore.pyqtSignal(str)
    Entered = QtCore.pyqtSignal(str)
    Leaved = QtCore.pyqtSignal(str)
    
    def __init__(self,name,timeoutset=None,parent=None):
        super(labelBtn,self).__init__()
        self.setMouseTracking(True)
        self.name = name
        
        if timeoutset == "1":
            print self.name,"timeout_event_make"
            self.timer=QtCore.QTimer(self)
            self.timer.setInterval(200)
            self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.btn_timeout)
    
    def btn_timeout(self):
        print self.name,'timerId:',QtCore.QTimer.timerId(self.timer)
        print self.name,'btn_timeout'
        self.timer.stop()
        self.hide()
        
    def mouseReleaseEvent(self,event):
        self.Clicked.emit(self.name)
   
    def enterEvent(self,event):
        self.Entered.emit(self.name)
   
    def leaveEvent(self,event):
        self.Leaved.emit(self.name)
        
class balloon(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Nvpu,self).__init__(parent)
        pass
        
#语音识别部分-----------------------------------------------------------------------
class speech_recognize(QtCore.QThread):
    NewSession=QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(speech_recognize,self).__init__(parent)
    def __del__(self):
        self.exiting = True
        self.wait()
    def run(self):
        self.mic = microphone.Microphone()
        self.FILE=self.mic.listen()
        self.NewSession.emit()
        url = 'http://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=zh-CN&maxresults=10'
        audio=open(self.FILE,'rb').read()
        headers = {'Content-Type' : 'audio/L16; rate=16000'}
        try:
            req = urllib2.Request(url, audio, headers)
            response = urllib2.urlopen(req,timeout=10)
            print response.read().decode('UTF-8')
            print "translate end",self.ResultNum,self.FILE
        except:
            print u"网络状况不好或者其他错误发生"
        
        #res=requests.post(url,data=audio,timeout=0.3,headers=headers)
        #print res.text
        os.remove(self.FILE)

#鼠标键盘监控-----------------------------------------------------------------------
def KeyMouseMonitor():
    if os.name == "posix":
        #'nt' 'mac'
        pass
    else:
        import pythoncom
        import pyHook
        hm = pyHook.HookManager()
        hm.KeyDown = WinKeyboardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()
        
DoubeKeytime = 0
def WinKeyboardEvent(event):
    global DoubeKeytime
    if event.Key == 'Lmenu' or event.Key == 'Rmenu':
        if DoubeKeytime!= 0:
            if 100<(int(event.Time)-DoubeKeytime)<450:
                global nvpu
                nvpu.KeyHide()
                print u'ALT双击'+str(int(event.Time)-DoubeKeytime)
            DoubeKeytime = 0
        else:
            DoubeKeytime = int(event.Time)
    else:
        DoubeKeytime = 0
    return True

def shownvpu():
    app = QtGui.QApplication([])
    Start_Screen=QtGui.QSplashScreen(QtGui.QPixmap("shell/start.png"))
    Start_Screen.show()
    global nvpu
    nvpu = Nvpu()
    nvpu.show()
    Start_Screen.finish(nvpu)
    KeyMouseMonitor()
    app.exec_()
    
def main():
    shownvpu()
if __name__=="__main__":
    main()
