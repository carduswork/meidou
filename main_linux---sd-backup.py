#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, Qt
from configobj import ConfigObj
import os,sys,urllib2,microphone,time

MouseLeftDownPos = [0,0]

class Nvpu(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Nvpu,self).__init__(parent)

        self.window_attribute()
        #载入数据
        self.Config_read()

        #主人格图片
        self.btn_min=labelBtn("main")
        self.btn_min.setParent(self)
        self.btn_min.move(100,100)
        self.btn_min.setPixmap(QtGui.QPixmap(paltform_path("shell/surface1.png")))
        
        #设置窗口位置
        desktop =QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        
        if not "firstboot" in self.sys_dict:
            self.move(width-400,height-400)
            self.sys_dict["firstboot"] = "1"
        else:
            self.move(int(self.sys_dict["nvpu_pos_x"]),int(self.sys_dict["nvpu_pos_y"]))
        self.resize(500,500)
        
        self.MakeBtn()
        self.sys_dict['NvpuHide'] = 0
        self.mouse_call = 0
        self.LastFocusBtnNum = 0
        self.FocusBtnNum = 0
        self.sys_dict["btnClicked"] = "0"
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

    def window_attribute(self):
        if os.name == 'nt':
            #隐藏窗口边框、背景、任务栏
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.SplashScreen)
            pass            
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)# | QtCore.Qt.Tool)
            pass
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        #窗口透明度
        self.setWindowOpacity(0.9)
        
    def mouseReleaseEvent(self,event):
        global Flat
        Flat = 0
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            global Flat
            Flat = 1
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        if event.button() == QtCore.Qt.RightButton:
            self.RightMenuShow()

    def RightMenuShow(self):
        if self.sys_dict["btnClicked"] != "1":
            for btn in self.BtnList:
                btn.show()
            self.sys_dict["btnClicked"] = "1"
        else:
            for btn in self.BtnList:
                btn.hide()
            self.sys_dict["btnClicked"] = "0"
    
    def mouseMoveEvent(self,event):
        self.mouse_call = time.time()
        try:
            if Flat and (event.buttons() == QtCore.Qt.LeftButton):
                self.move(event.globalPos() - self.dragPosition)
        except:pass
        
    def keyReleaseEvent(self, event):
         print event.key()#Qt.Key_Left Qt.Key_Up Qt.Key_Right Qt.Key_Down
         if event.key() == QtCore.Qt.Key_Menu :
             self.RightMenuShow()
         elif event.key() == QtCore.Qt.Key_Escape :
             self.out()
         elif event.key() == QtCore.Qt.Key_Left or event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Right or event.key() == QtCore.Qt.Key_Down:
             if self.sys_dict["btnClicked"] == "1":
                 print 'Qt.Key_Left Qt.Key_Up Qt.Key_Right Qt.Key_Down Press'
                 if event.key() == QtCore.Qt.Key_Left:
                    if self.FocusBtnNum == 5:
                        self.FocusBtnNum = 0
                        self.LastFocusBtnNum = 5
                    else:
                        self.LastFocusBtnNum = self.FocusBtnNum
                        self.FocusBtnNum = self.FocusBtnNum + 1
                    self.ChangebtnFoucus()
                    
                 if event.key() == QtCore.Qt.Key_Right:
                    if self.FocusBtnNum == 0:
                        self.FocusBtnNum = 5
                        self.LastFocusBtnNum = 0
                    else:
                        self.LastFocusBtnNum = self.FocusBtnNum
                        self.FocusBtnNum = self.FocusBtnNum - 1
                    self.ChangebtnFoucus()
                    
    def ChangebtnFoucus(self):
        print 'ChangebtnFoucus',self.FocusBtnNum
        print self.BtnNameList[self.FocusBtnNum]
        print 'self.' + self.BtnNameList[self.FocusBtnNum] + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[self.BtnNameList[self.FocusBtnNum]+'_hover'] + '")))'
        print 'self.' + self.BtnNameList[self.LastFocusBtnNum] + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[self.BtnNameList[self.LastFocusBtnNum]+'_normal'] + '")))'
        exec('self.' + self.BtnNameList[self.FocusBtnNum] + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[self.BtnNameList[self.FocusBtnNum]+'_hover'] + '")))')
        exec('self.' + self.BtnNameList[self.LastFocusBtnNum] + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[self.BtnNameList[self.LastFocusBtnNum]+'_normal'] + '")))')
        
    def change(self,Surface_path):
        self.btn_min.setPixmap(QtGui.QPixmap(Surface_path))
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())

    #关闭前事宜
    def out(self):
        #删除WAV缓存
        for file in os.listdir(paltform_path("wav")):
            try:
                os.remove(paltform_path("wav/"+file))
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

    #INI文件读取--有时间写成块--用法self.sys_dict[]
    def Config_read(self):
        self.sys_dict = {}
        self.sys_ini = ConfigObj(paltform_path("/ini/sys.ini"))
        for key in self.sys_ini.keys():
            print key," = ",self.sys_ini[key]
            self.sys_dict[key] = self.sys_ini[key]
            
        self.shell_dict = {}
        self.shell_ini = ConfigObj(paltform_path("/ini/shell.ini"))
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
        self.BtnNameList = ('programs_btn','info_btn','tools_btn','shutdown_btn','msg_btn','skills_btn')
        #self.BtnNameList = ('shutdown_btn','tools_btn','skills_btn','info_btn','programs_btn','msg_btn')
        self.CircularBtnNameList = ('Circular_LeftBottom','Circular_RightTop','Circular_RightMidde',
                                    'Circular_RightBottom','Circular_LeftTop','Circular_LeftMidde')
        self.CircularSecondBtnNameList = ('Circular_LeftBottom1', 'Circular_LeftBottom2', 'Circular_LeftBottom3',
                                          'Circular_RightTop1',   'Circular_RightTop2',   'Circular_RightTop3',
                                          'Circular_RightMidde1', 'Circular_RightMidde2', 'Circular_RightMidde3',
                                          'Circular_RightBottom1','Circular_RightBottom2','Circular_RightBottom3',
                                          'Circular_LeftTop1',    'Circular_LeftTop2',    'Circular_LeftTop3',
                                          'Circular_LeftMidde1',  'Circular_LeftMidde2',  'Circular_LeftMidde3')
        for name in self.CircularBtnNameList:
            print name+' create'
            exec('self.' + name + '=labelBtn("' + name + '","1")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[name] + '")))')
            
        for name in self.CircularSecondBtnNameList:
            print name+' create'
            exec('self.' + name + '=labelBtn("' + name + '")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[name+'_normal'] + '")))')
            
        for name in self.BtnNameList:
            print name+' create'
            exec('self.' + name + '=labelBtn("' + name + '")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[name+'_normal'] + '")))')
        ('programs_btn','info_btn','tools_btn','shutdown_btn','msg_btn','skills_btn')
        self.BtnList = (self.programs_btn,self.info_btn,self.tools_btn,self.shutdown_btn,self.msg_btn,self.skills_btn)
        #self.BtnList = (self.shutdown_btn,self.tools_btn,self.skills_btn,self.info_btn,self.programs_btn,self.msg_btn)
        self.CircularBtnList = (self.Circular_LeftBottom,self.Circular_RightTop,self.Circular_RightMidde,
                                self.Circular_RightBottom,self.Circular_LeftTop,self.Circular_LeftMidde)
        self.CircularSecondBtnList = (self.Circular_LeftBottom1,  self.Circular_LeftBottom2,  self.Circular_LeftBottom3,
                                      self.Circular_RightTop1,    self.Circular_RightTop2,    self.Circular_RightTop3,
                                      self.Circular_RightMidde1,  self.Circular_RightMidde2,  self.Circular_RightMidde3,
                                      self.Circular_RightBottom1, self.Circular_RightBottom2, self.Circular_RightBottom3,
                                      self.Circular_LeftTop1,     self.Circular_LeftTop2,     self.Circular_LeftTop3,
                                      self.Circular_LeftMidde1,   self.Circular_LeftMidde2,   self.Circular_LeftMidde3)
        
        for btn in self.BtnList + self.CircularSecondBtnList:
            btn.Clicked.connect(self.BtnCLICK)
            btn.Entered.connect(self.BtnENTER)
            btn.Leaved.connect(self.BtnLEAVE)
            btn.hide()

        for btn in self.CircularBtnList:
            btn.Clicked.connect(self.BtnCLICK)
            btn.Entered.connect(self.BtnENTER)
            btn.Leaved.connect(self.BtnLEAVE)
            btn.Btn_timeout.connect(self.Btn_TIMEOUT)
            btn.Extra_show.connect(self.BtnEXTRA_SHOW)
            btn.hide()
        
    def BtnCLICK(self,name):
        print name+" clicked"
        if name == "shutdown_btn":
            self.out()

    def BtnENTER(self,name):
        print name+" entered"
        
        if str(name) == "tools_btn":
            self.Circular_LeftBottom.extra_show()
            self.Circular_LeftBottom.timer.stop()
        elif str(name) == 'skills_btn':
            self.Circular_RightTop.extra_show()
            self.Circular_RightTop.timer.stop()
        elif str(name) == 'msg_btn':
            self.Circular_RightMidde.extra_show()
            self.Circular_RightMidde.timer.stop()
        elif str(name) == 'shutdown_btn':
            self.Circular_RightBottom.extra_show()
            self.Circular_RightBottom.timer.stop()
        elif str(name) == 'programs_btn':
            self.Circular_LeftTop.extra_show()
            self.Circular_LeftTop.timer.stop()
        elif str(name) == 'info_btn':
            self.Circular_LeftMidde.extra_show()
            self.Circular_LeftMidde.timer.stop()
        else:pass
        
        if str(name) in self.CircularBtnNameList:
            exec('self.' + str(name) + '.extra_show()')
            exec('self.' + str(name) + '.timer.stop()')
            
        if str(name) in self.CircularSecondBtnNameList:
            exec('self.' + str(name)[:-1] + '.extra_show()')
            exec('self.' + str(name) + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[str(name)+'_hover'] + '")))')
            exec('self.' + str(name)[:-1] + '.timer.stop()')
            
        if str(name) in self.BtnNameList:
            exec('self.' + str(name) + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[str(name+'_hover')] + '")))')

    def BtnLEAVE(self,name):
        print name+" leaved"

        if str(name) in self.CircularSecondBtnNameList:
            exec('self.' + str(name)[:-1] + '.timer.start()')
            exec('self.' + str(name) + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[str(name)+'_normal'] + '")))')
            
        if str(name) in self.CircularBtnNameList:
            exec('self.' + str(name) + '.timer.start()')
 
        if str(name) in self.BtnNameList:
            exec('self.' + str(name) + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[str(name+'_normal')] + '")))')
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
            
    def Btn_TIMEOUT(self,name):
        for i in (1,2,3):
            print 'self.'+str(name)+str(i)+'.hide()'
            exec('self.'+str(name)+str(i)+'.hide()')

    def BtnEXTRA_SHOW(self,name):
        for i in (1,2,3):
            print 'self.'+str(name)+str(i)+'.show()'
            exec('self.' + str(name)+str(i) + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[str(name)+str(i)+'_normal'] + '")))')
            exec('self.' + str(name)+str(i)+'.show()')
            
    def KeyHide(self):
        if self.sys_dict['NvpuHide'] == 0:
            self.hide()
            self.sys_dict['NvpuHide'] = 1
        else:
            self.show()
            self.resize(500,500)
            self.setFocus()
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.activateWindow()
            print 'self.activateWindow()'
            print self.hasFocus()
            self.sys_dict['NvpuHide'] = 0
         
    def MouseHide(self):
        if time.time()-self.mouse_call > 0.1:
            if self.sys_dict['NvpuHide'] == 0:
                self.hide()
                self.sys_dict['NvpuHide'] = 1
            else:
                self.show()
                self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
                self.activateWindow()
                self.move(MouseLeftDownPos[0]-250,MouseLeftDownPos[1]-250)
                self.resize(500,500)
                self.sys_dict['NvpuHide'] = 0
            self.mouse_call = 0
        else:
            self.mouse_call = 0
        
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


    
#图标类
class labelBtn(QtGui.QLabel):
    Clicked = QtCore.pyqtSignal(str)
    Entered = QtCore.pyqtSignal(str)
    Leaved = QtCore.pyqtSignal(str)
    Btn_timeout = QtCore.pyqtSignal(str)
    Extra_show = QtCore.pyqtSignal(str)
    
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
        self.Btn_timeout.emit(self.name)
        print self.name,'timerId:',QtCore.QTimer.timerId(self.timer)
        print self.name,'btn_timeout'
        self.timer.stop()
        self.hide()
        
    def extra_show(self):
        self.Extra_show.emit(self.name)
        print self.name,'extra_show'
        self.show()
        
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
            exec('rest ='+ str(response.read().decode('UTF-8')))
            if rest:
                if rest['status'] == 0:
                    googlevoice.get(str(rest['hypotheses'][0]['utterance']))
            print "translate end",self.ResultNum,self.FILE
        except Exception,e:
            print e
        
        #res=requests.post(url,data=audio,timeout=0.3,headers=headers)
        #print res.text
        os.remove(self.FILE)

#鼠标键盘监控-----------------------------------------------------------------------
def KeyMouseMonitor():
    if os.name == "nt":
        #'nt' 'mac' "posix"
        import pythoncom
        import pyHook
        hm = pyHook.HookManager()
        hm.KeyDown = WinKeyboardEvent
        hm.HookKeyboard()
        hm.MouseAll = WinMouseboardEvent
        hm.HookMouse()
        pythoncom.PumpMessages()
    else:
        pass
        
DoubeKeytime = 0
def WinKeyboardEvent(event):
    global DoubeKeytime,nvpu
    #nvpu.WinKeyEVENT(event.Key)
    if event.Key == 'Lmenu' or event.Key == 'Rmenu':
        if DoubeKeytime!= 0:
            if 100<(int(event.Time)-DoubeKeytime)<450:
                nvpu.KeyHide()
                print u'ALT双击'+str(int(event.Time)-DoubeKeytime)
            DoubeKeytime = 0
        else:
            DoubeKeytime = int(event.Time)
    else:
        DoubeKeytime = 0
    return True

#MouseLeftDownPos = [0,0]
def WinMouseboardEvent(event):
    global MouseLeftDownPos
    if event.MessageName == 'mouse left down':#middle
        MouseLeftDownPos = event.Position
    else:
        if event.MessageName == 'mouse move':
            if MouseLeftDownPos[1]:
                if (event.Position[1] - MouseLeftDownPos[1] < -20) and (event.Position[0] - MouseLeftDownPos[0] < -10):
                    print "OVER",MouseLeftDownPos,time.time()
                    global nvpu
                    nvpu.MouseHide()
                    MouseLeftDownPos = [0,0]
        else:
            MouseLeftDownPos = [0,0]
    return True
    
def paltform_path(path):
    if os.name == "nt":
        if path.startswith(r'/'):
            return path[1:]
        else:
            return path
    else:
        if path.startswith(r'/'):
            print sys.path[0]+path
            return sys.path[0]+path
        else:
            print sys.path[0]+r'/'+path
            return sys.path[0]+r'/'+path
        
def shownvpu():
    app = QtGui.QApplication([])
    Start_Screen=QtGui.QSplashScreen(QtGui.QPixmap(paltform_path("/shell/start.png")))
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
