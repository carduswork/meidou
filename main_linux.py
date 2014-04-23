#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, Qt, phonon
from configobj import ConfigObj
import os,sys,urllib2,urllib,microphone,time,googlevoice,re
import msc_wrapper,threading

true = True
null = None
false = False

#主窗口
class Nvpu(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Nvpu,self).__init__(parent)
        self.window_attribute()
        #载入数据
        self.Config_read()
        #主人格图片
        #self.btn_min=labelBtn("main")
        self.btn_min=QtGui.QLabel('main')
        self.btn_min.setParent(self)
        self.btn_min.move(100,100)
        self.btn_min.setStyleSheet('color:rgba(0,0,0,10%);')
        self.btn_min.setPixmap(QtGui.QPixmap(paltform_path("shell/surface1.png")))
        
        #设置窗口位置
        desktop =QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        
        if not "firstboot" in self.sys_dict:
            self.move(width-400,height-400)
            self.firstboot = "1"
        else:
            self.move(int(self.sys_dict["nvpu_pos_x"]),int(self.sys_dict["nvpu_pos_y"]))
        self.resize(500,500)
        
        self.MakeBtn()
        self.sys_dict['NvpuHide'] = 0
        self.mouse_call = 0
        self.LastFocusBtnNum = 0
        self.FocusBtnNum = 0
        self.sys_dict["btnClicked"] = "0"

        font = QtGui.QFont()
        font.setPixelSize(12)   #设置字号32,以像素为单位
        font.setFamily("SimSun")#设置字体，宋体
        #font.setWeight(13)     #设置字型,不加粗
        font.setBold(True)
        font.setItalic(False)   #设置字型,不倾斜
        font.setUnderline(False)#设置字型,无下划线

        pa = QtGui.QPalette()
        pa.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,0,0))
        
        self.mark_msg=labelBtn("mark")
        self.mark_msg.setParent(self)
        self.mark_msg.move(150,280)
        self.mark_msg.setPalette(pa)
        self.mark_msg.setFont(font)
        
        self.mark_msg_timer=QtCore.QTimer(self)
        self.mark_msg_timer.setInterval(3000)
        self.connect(self.mark_msg_timer,QtCore.SIGNAL("timeout()"),self.mark_msg_timeout)

        self.balloon_timer=QtCore.QTimer(self)
        self.balloon_timer.setInterval(10000)
        self.connect(self.balloon_timer,QtCore.SIGNAL("timeout()"),self.message_timeout)
        '''
        # 创建托盘
        self.icon = QtGui.QIcon("shell/icon.png")
        self.trayIcon = QtGui.QSysself.firstboottemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip(u"女仆酱")
        self.trayIcon.show()
        # 托盘气泡消息
        self.trayIcon.showMessage(u"美豆酱", u"女仆酱已开启")
        # 托盘菜单
        self.action = QtGui.QAction(u"退出", self)#, triggered = self.out())#sys.exit)
        self.menu = QtGui.QMenu(self)
        self.menu.addAction(self.action)
        self.trayIcon.setContextMenu(self.menu)
        '''
        #创建表情转换线程
        #self.thread = MyThread()
        #self.thread.ChangeS.connect(self.change)
        #self.thread.start()
        
        #创建语音识别会话
        #self.SessionNum = 0
        #self.NewSession()
        #msc_wrapper.regStart()

    def window_attribute(self):
        if os.name == 'nt':
            #隐藏窗口边框、背景、任务栏
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.SplashScreen)           
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)# | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        #窗口透明度
        self.setWindowOpacity(0.9)

    def setballoon(self,balloon):
        self.balloon = balloon
        if not "firstboot" in self.sys_dict:
            self.balloon.move_postion(self.pos().x(),self.pos().y())
            self.firstboot = "1"
        else:
            self.balloon.move(int(self.sys_dict["balloon_pos_x"]),int(self.sys_dict["balloon_pos_y"]))

    def setMsgWindow(self,msgWindow):
        self.msgWindow = msgWindow
        
    def message(self,msg,msgtype = None,timeout = 0):
        if msgtype == 'mark':
            if timeout:
                self.mark_msg_timer.stop()
                self.mark_msg_timer.setInterval(timeout)
                self.mark_msg_timer.start()
            else:
                self.mark_msg_timer.stop()
                self.mark_msg_timer.start()
            self.mark_msg.hide()
            self.mark_msg.setText(msg)
            self.mark_msg.show()
        else:
            if timeout:
                self.balloon_timer.stop()
                self.balloon_timer.setInterval(timeout)
                self.balloon_timer.start()
            else:
                self.balloon_timer.stop()
                self.balloon_timer.start()
            self.balloon.settext(msg)
            self.balloon.show()

    def message_timeout(self):
        self.balloon.settext('')
        self.balloon.hideit()

    def mark_msg_timeout(self):
        self.mark_msg.setText('')
            
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
                _pos = event.globalPos() - self.dragPosition
                if self.balloon: self.balloon.move_postion(_pos.x(),_pos.y())
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
        if not "firstboot" in self.sys_dict:self.firstboot = "1"
        #停止讯飞语音识别
        msc_wrapper.regEnd()
        #删除WAV缓存
        for file in os.listdir(paltform_path("wav")):
            try:os.remove(paltform_path("wav/"+file))
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
        self.sys_dict["balloon_pos_x"] = self.balloon.pos().x()
        self.sys_dict["balloon_pos_y"] = self.balloon.pos().y()

        if not "firstboot" in self.sys_dict:self.sys_dict["firstboot"] = "1"

        for i in self.sys_dict:
            self.sys_ini[i] = self.sys_dict[i]
        self.sys_ini.write()

    #INI文件读取--有时间写成块--用法self.sys_dict[]
    def Config_read(self):
        self.sys_dict = {}
        self.sys_ini = ConfigObj(paltform_path("/ini/sys.ini"))
        for key in self.sys_ini.keys():
            self.sys_dict[key] = self.sys_ini[key]
            
        self.shell_dict = {}
        self.shell_ini = ConfigObj(paltform_path("/ini/shell.ini"))
        for key in self.shell_ini.keys():
            self.shell_dict[key] = self.shell_ini[key]

    #新建录音会话
    def NewSession(self):
        self.SessionNum = self.SessionNum+1
        exec('self.SessionName' + str(self.SessionNum) + '= speech_recognize()')
        exec('self.SessionName' + str(self.SessionNum) + '.NewSession.connect(self.NewSession)')
        exec('self.SessionName' + str(self.SessionNum) + '.regResult[str].connect(self.XunfeiResult,QtCore.Qt.QueuedConnection)')
        exec('self.SessionName' + str(self.SessionNum) + '.ResultNum=self.SessionNum')
        exec('self.SessionName' + str(self.SessionNum) + '.start()')

    #讯飞
    def XunfeiResult(self,res):
        self.balloon.text.setText(unicode(res, 'utf-8', 'ignore'))
        print res
        '''
        url = 'http://www.xiaohuangji.com/ajax.php?'
        pathDict={
                  'para':res,
                  }
        pathData=urllib.urlencode(pathDict)

        req=urllib2.Request(url,pathData)
        resp=urllib2.urlopen(req)
        html = resp.read()
        print 'got res',html.decode('utf-8')
        if googlevoice.get(html):
                self.ph = phonon.Phonon.createPlayer(phonon.Phonon.MusicCategory)
		self.ph.setTickInterval(1000)
		self.ph.setCurrentSource(phonon.Phonon.MediaSource(QtCore.QString("test.mp3")))
		self.ph.play()
	'''
        
    def MakeBtn(self):
        self.BtnNameList = ('programs_btn','info_btn','tools_btn','shutdown_btn','msg_btn','skills_btn')
        
        self.CircularBtnNameList = ('Circular_LeftBottom','Circular_RightTop','Circular_RightMidde',
                                    'Circular_RightBottom','Circular_LeftTop','Circular_LeftMidde')
        self.CircularSecondBtnNameList = ('Circular_LeftBottom1', 'Circular_LeftBottom2', 'Circular_LeftBottom3',
                                          'Circular_RightTop1',   'Circular_RightTop2',   'Circular_RightTop3',
                                          'Circular_RightMidde1', 'Circular_RightMidde2', 'Circular_RightMidde3',
                                          'Circular_RightBottom1','Circular_RightBottom2','Circular_RightBottom3',
                                          'Circular_LeftTop1',    'Circular_LeftTop2',    'Circular_LeftTop3',
                                          'Circular_LeftMidde1',  'Circular_LeftMidde2',  'Circular_LeftMidde3')
        for name in self.CircularBtnNameList:
            exec('self.' + name + '=labelBtn("' + name + '","1")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[name] + '")))')
            
        for name in self.CircularSecondBtnNameList:
            exec('self.' + name + '=labelBtn("' + name + '")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[name+'_normal'] + '")))')
            
        for name in self.BtnNameList:
            exec('self.' + name + '=labelBtn("' + name + '")')
            exec('self.' + name + '.setParent(self)')
            exec('self.' + name + '.move(' + self.shell_dict[name+'_x'] + ',' + self.shell_dict[name+'_y'] + ')')
            exec('self.' + name + '.setPixmap(QtGui.QPixmap(paltform_path(r"' + self.shell_dict[name+'_normal'] + '")))')
            
        self.BtnList = (self.programs_btn,self.info_btn,self.tools_btn,self.shutdown_btn,self.msg_btn,self.skills_btn)
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
            btn.Moved.connect(self.BtnMOVE)
            btn.hide()

        for btn in self.CircularBtnList:
            btn.Clicked.connect(self.BtnCLICK)
            btn.Entered.connect(self.BtnENTER)
            btn.Leaved.connect(self.BtnLEAVE)
            btn.Btn_timeout.connect(self.Btn_TIMEOUT)
            btn.Extra_show.connect(self.BtnEXTRA_SHOW)
            btn.hide()

    def BtnMOVE(self,name,x,y):
        try:QtGui.QToolTip.showText(QtCore.QPoint(x,y),self.shell_dict[str(name)+'_tip'].decode('utf-8'),self)
        except:pass
    
    def BtnCLICK(self,name):
        print name+" clicked"
        if name == "shutdown_btn":self.out()
        if name == "Circular_RightBottom1":os.popen('shutdown -s')
        if name == "Circular_RightBottom2":os.popen('shutdown -l')
        if name == "Circular_RightBottom3":os.popen('shutdown -r')

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
            self.balloon.hideit()
            self.sys_dict['NvpuHide'] = 1
        else:
            self.show()
            self.balloon.show()
            self.resize(500,500)
            self.setFocus()
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.activateWindow()
            print 'self.activateWindow()'
            print self.hasFocus()
            self.sys_dict['NvpuHide'] = 0
         
    def MouseHide(self,MouseLeftDownPos):
        if time.time()-self.mouse_call > 0.1:
            if self.sys_dict['NvpuHide'] == 0:
                self.hide()
                self.sys_dict['NvpuHide'] = 1
            else:
                self.show()
                self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
                self.activateWindow()
                self.move(MouseLeftDownPos[0]-250,MouseLeftDownPos[1]-250)
                if self.balloon: self.balloon.move_postion(MouseLeftDownPos[0]-250,MouseLeftDownPos[1]-250)
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


    
#图标类重写
class labelBtn(QtGui.QLabel):
    Clicked = QtCore.pyqtSignal(str)
    Entered = QtCore.pyqtSignal(str)
    Leaved = QtCore.pyqtSignal(str)
    Moved = QtCore.pyqtSignal(str,int,int)
    Btn_timeout = QtCore.pyqtSignal(str)
    Extra_show = QtCore.pyqtSignal(str)
    
    def __init__(self,name,timeoutset=None,parent=None):
        super(labelBtn,self).__init__()
        self.setMouseTracking(True)
        self.name = name
        
        if timeoutset == "1":
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
        
    def mouseMoveEvent(self,event):
        self.Moved.emit(self.name,event.globalPos().x(),event.globalPos().y())
        
    def enterEvent(self,event):
        self.Entered.emit(self.name)
   
    def leaveEvent(self,event):
        self.Leaved.emit(self.name)

#仿ubuntu下的气泡提示，左击进入提示，右击关闭
class msgWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(msgWindow,self).__init__(parent)
        self.btn_min=labelBtn("background")
        self.btn_min.setParent(self)
        #self.btn_min.setStyleSheet('color:rgba(0,0,0,10%);')
        self.pix = QtGui.QPixmap(paltform_path("balloon/msgWindow.png"))
        self.btn_min.setPixmap(self.pix)#272 88

        self.setAttribute(QtCore.Qt.WA_NoSystemBackground,True)
        self.setWindowOpacity(1.0)
        self.window_attribute()

        self.msg = QtGui.QLabel('msg')
        #self.msg.move(19,25)
        self.msg.setParent(self)

        self.title = QtGui.QLabel('title')
        self.title.move(17,11)
        self.title.setParent(self)
        
        font = QtGui.QFont()
        font.setPixelSize(15)   #设置字号32,以像素为单位
        font.setFamily("SimSun")#设置字体，宋体
        #font.setWeight(13)     #设置字型,不加粗
        font.setBold(True)
        font.setItalic(False)   #设置字型,不倾斜
        font.setUnderline(False)#设置字型,无下划线

        pa = QtGui.QPalette()
        pa.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255))
        
        self.title.setPalette(pa)
        self.title.setFont(font)
        
        font.setPixelSize(12)
        pa.setColor(QtGui.QPalette.WindowText,QtGui.QColor(232,232,232))
        
        self.msg.setPalette(pa)
        self.msg.setFont(font)
 
        #自动换行
        self.msg.adjustSize()#让QLabel能够自动判断并换行显示：
        self.msg.setGeometry(QtCore.QRect(19,27,202,24*2)) #四倍行距
        self.msg.setWordWrap(True)
        self.msg.setAlignment(QtCore.Qt.AlignTop)

        #self.title.setText(u' ')
        #self.msg.setText(u' '*20)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(6000)
        self.timer.start()
        self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.timeout)

        desktop =QtGui.QApplication.desktop()
        self.dwidth = desktop.width()
        self.dheight = desktop.height()
        
        self.msg_queue = []
        self.setGeometry(self.dwidth-40-self.pix.size().width(),100,self.pix.size().width(),self.pix.size().height())
        
    def timeout(self):
        self.setWindowOpacity(0.4)
        time.sleep(0.2)
        self.hide()

    def cal_img(self,pointX,pointY):
        img = QPixmap.grabWindow(
            QApplication.desktop().winId()).toImage()
        rgb = img.pixel(pointX, pointY)
        red10 = QtGui.qRed(rgb)
        green10 =QtGui.qGreen(rgb)
        blue10 = QtGui.qBlue(rgb)
        print pointX, pointY,red10,green10,blue10
            
    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            import webbrowser
            webbrowser.open("http://tieba.baidu.com/home/msg?un=gph159821&fr=home")
            self.hide()
        if event.button() == QtCore.Qt.RightButton:
            self.hide()

    def enterEvent(self,event):
        self.timer.stop()
        self.setWindowOpacity(0.4)

    def leaveEvent(self,event):
        self.timer.start()
        self.setWindowOpacity(0.8)

        
    def window_attribute(self):
        if os.name == 'nt':
            #隐藏窗口边框、背景、任务栏
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.SplashScreen)           
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)# | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        #窗口透明度
        self.setWindowOpacity(0.8)

    def showMsg(self,msg,title = None,icon = None):
        self.timer.stop()
        self.setWindowOpacity(0.8)
        self.title.setText(str(title).decode('utf-8'))
        self.msg.setText(msg)
        self.show()
        self.timer.start()
        
class mainThread(QtCore.QThread):
    '''
    处理主要事件的主线程，如最开始的初始化
    '''
    msgSignal = QtCore.pyqtSignal(str,str,str)
    chatSignal = QtCore.pyqtSignal(str,str,str)
    def __init__(self,parent=None):
        super(mainThread,self).__init__(parent)

    def setMsgWindow(self,MsgWindow):
        self.msgWindow = MsgWindow
        self.msgSignal.connect(self.msgWindow.showMsg)

    def setMianWindow(self,MianWindow):
        self.nvpu = MianWindow
        self.chatSignal.connect(self.nvpu.message)
        
    def run(self):
        if not "firstboot" in self.nvpu.sys_dict:
            #self.msgSignal.emit(u'第一次开启，初始化开始','Start','')
            self.chatSignal.emit(u'第一次开启，初始化开始','mark','')

            #读取贴吧Cookies
            
            if os.name == "nt":
                try:
                    import GetCacheCookies
                    baidu_cookie = GetCacheCookies.getcachecookies('.baidu.com')
                except:pass  
            if baidu_cookie:
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
            if baidu_cookie:
                pass










            
#人物对话框        
class balloon(QtGui.QWidget):
    def __init__(self, parent=None):
        super(balloon,self).__init__(parent)
        self.btn_min=labelBtn("background")
        self.btn_min.setParent(self)
        #self.btn_min.setStyleSheet('color:rgba(0,0,0,10%);')
        self.btn_min.setPixmap(QtGui.QPixmap(paltform_path("balloon/balloon1.png")))

        self.teachbox = None
        self.inputbox = None
        self.communicatebox = None

        self.setAttribute(QtCore.Qt.WA_NoSystemBackground,True)
        self.setWindowOpacity(1.0)
        self.window_attribute()

        #self.text = QtGui.QLabel('text')
        self.text=labelBtn("background")
        self.text.move(25,25)
        self.text.setParent(self)

        font = QtGui.QFont()
        font.setPixelSize(16)   #设置字号32,以像素为单位
        font.setFamily("SimSun")#设置字体，宋体
        #font.setWeight(13)     #设置字型,不加粗
        font.setBold(True)
        font.setItalic(False)   #设置字型,不倾斜
        font.setUnderline(False)#设置字型,无下划线

        pa = QtGui.QPalette()
        pa.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,0,0))

        self.text.setPalette(pa)
        self.text.setFont(font)

        #非自动换行
        #self.add_text(u'欢迎使用我，这里是由黑月编写的桌面助手。。。。balabala什么的还是不要了吧')

        #自动换行
        self.text.adjustSize()#让QLabel能够自动判断并换行显示：
        self.text.setGeometry(QtCore.QRect(7,7,202,25*4)) #四倍行距
        self.text.setWordWrap(True)
        self.text.setAlignment(QtCore.Qt.AlignTop)
        #self.text.setText(u'欢迎使用我，这里是由黑月编写的桌面助手。。。。balabala什么的还是不要了吧')

    def window_attribute(self):
        if os.name == 'nt':
            #隐藏窗口边框、背景、任务栏
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.SplashScreen)          
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)# | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        #窗口透明度
        self.setWindowOpacity(0.9)

    def reset_balloon(self):
        pass

    def finish(self):
        self.communicatebox.destroy()
        self.teachbox.destroy()
        self.inputbox.destroy()

    def get_position(self, side):
        pass

    def hideit(self):
        self.hide()
        pass

    def clear(self):
        pass

    def settext(self,text):
        self.text.setText(text)
    
    def add_text(self,text):
        _text = []
        alltext = ''
        i = int(len(text)/10)+1
        p = 0
        while i:
            print i,p
            _text.append(str(text[p:p+9])+'\n')
            print text[p:p+9]
            p = p + 9
            i = i - 1
        for i in _text:
            alltext = alltext + i
        self.text.setText(alltext.decode('utf-8'))
        print alltext.decode('utf-8')
        self.text.show()

    def add_images(self):
        pass

    def move_postion(self,x,y):
        self.move(x-80,y-85)
        pass
    
    def mouseReleaseEvent(self,event):
        print 'mouseReleaseEvent'
        global Flat
        Flat = 0
        
    def mousePressEvent(self,event):
        print 'mousePressEvent'
        if event.button() == QtCore.Qt.LeftButton:
            global Flat
            Flat = 1
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self,event):
        print 'mouseMoveEvent'
        self.mouse_call = time.time()
        try:
            if Flat and (event.buttons() == QtCore.Qt.LeftButton):
                self.move(event.globalPos() - self.dragPosition)
                _pos = event.globalPos() - self.dragPosition
                if self.balloon: self.balloon.move_postion(_pos.x(),_pos.y())
        except:pass
        
def ntpath(path):
    if os.name == 'nt': # XXX
        path = unicode(path, 'mbcs').encode('utf-8')


#消息提醒线程
class msgThread(QtCore.QThread):
    msgSignal = QtCore.pyqtSignal(str,str,str)
    def __init__(self,parent=None):
        super(msgThread,self).__init__(parent)

        #http://tieba.baidu.com/f/user/json_userinfo
        #http://tb.himg.baidu.com/sys/portrait/item/894d6770683135393832317d21
        
    def setMsgWindow(self,MsgWindow):
        self.msgWindow = MsgWindow
        self.msgSignal.connect(self.msgWindow.showMsg)
        
    def tiebamsg(self):
        msg = ''
        header = {
                'Cookie': 'BAIDUID=74AAE03D9A0B02CC7AACC4E092EE1583:FG=1; BAIDU_WISE_UID=wapp_1393159513840_622; BDUSS=ndlTWpIcXpPZFJ1SUdMMGZTdXYtcmJPTWhHUDRJVFkzOTZKeFRualh0bGVlakZUQVFBQUFBJCQAAAAAAAAAAAEAAACJTX0hZ3BoMTU5ODIxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF7tCVNe7QlTb; SSUDB=ndlTWpIcXpPZFJ1SUdMMGZTdXYtcmJPTWhHUDRJVFkzOTZKeFRualh0bGVlakZUQVFBQUFBJCQAAAAAAAAAAAEAAACJTX0hZ3BoMTU5ODIxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF7tCVNe7QlTb; locale=zh; BDRCVFR[YG-Oj537bb0]=mk3SLVN4HKm; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[eYjbPwSqvSs]=mk3SLVN4HKm; IM_=1; cflag=65535%3A1; H_PS_PSSID=5329_1453_5223_4264_5567_4759_5516',
                'Referer': 'http://tieba.baidu.com/',
                'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
                }

        req=urllib2.Request("http://message.tieba.baidu.com/i/msg/get_data",headers=header)
        data = urllib2.urlopen(req,timeout = 3).read()
        if data:exec('msg_data =' + data[18:-2])
        if msg_data:
            if msg_data[0]:
                msg = msg + '新粉丝'+str(msg_data[0])+','
            if msg_data[3]:
                msg = msg + '新回复'+str(msg_data[3])+','
            if msg_data[4]:
                msg = msg + '新精品'+str(msg_data[4])+','
            if msg_data[8]:
                msg = msg + '@我的'+str(msg_data[8])+','
            if msg_data[9]:
                msg = msg + '回收站提醒'+str(msg_data[9])
        if msg:msg=msg+','
        req=urllib2.Request("http://msg.baidu.com/msg/msg_dataGetmsgCount",headers=header)
        data2 = urllib2.urlopen(req,timeout = 3).read()
        if data2:exec('msg_data2 =' + data2[1:-2])
        if data2:
            if msg_data2['sysMsgNum']!='0':
                msg = msg + '系统消息'+msg_data2['sysMsgNum']+','
            if msg_data2['actMsgNum']!='0':
                msg = msg + '活动消息'+msg_data2['actMsgNum']+','
            if msg_data2['mailMsgNum']!='0':
                msg = msg + '新私信'+ msg_data2['mailMsgNum']+','
        print msg.decode('utf-8')
        return msg

    def run(self):
        while 1:
            #if 1:
            try:
                msg = self.tiebamsg()
                if msg:self.msgSignal.emit(msg.decode('utf-8'),u'贴吧消息','')
            except Exception,ex:print ex
            time.sleep(20)

#语音识别部分-----------------------------------------------------------------------
class speech_recognize(QtCore.QThread):
    NewSession=QtCore.pyqtSignal()
    regResult = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(speech_recognize,self).__init__(parent)
        
    def __del__(self):
        self.exiting = True
        self.wait()
        
    def run(self):
        self.mic = microphone.Microphone()
        self.FILE=self.mic.listen()
        self.NewSession.emit()
        if os.path.getsize(self.FILE)>0:
            #讯飞语音识别
            res = msc_wrapper.sendwav(self.FILE)
            if res and u'失败' in res:
                msc_wrapper.regEnd()
                msc_wrapper.regStart()
            else:
                if res:self.regResult.emit(res.decode('utf-8'))
        #Google语音识别
        '''
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
        '''
        
        #res=requests.post(url,data=audio,timeout=0.3,headers=headers)
        #print res.text
        os.remove(self.FILE)

def paltform_path(path):
    if os.name == "nt":
        if path.startswith(r'/'):
            return path[1:]
        else:
            return path
    else:
        if path.startswith(r'/'):
            return sys.path[0]+path
        else:
            return sys.path[0]+r'/'+path
        

class Application(object):
    def __init__(self):
        self.DoubeKeytime = 0
        self.MouseLeftDownPos = [0,0]
    
    def run(self):
        self.app = QtGui.QApplication([])
        self.Start_Screen=QtGui.QSplashScreen(QtGui.QPixmap(paltform_path("/shell/start.png")))
        self.Start_Screen.show()
        self.nvpu = Nvpu()
        self.nvpu.show()

        self.balloon = balloon()
        self.nvpu.setballoon(self.balloon)

        self.msgWindow = msgWindow()
        self.nvpu.setMsgWindow(self.msgWindow)




            
        
        self.Start_Screen.finish(self.nvpu)

        #self.nvpu.XunfeiResult('早上好')
        #self.nvpu.message('test')
        #self.nvpu.message('test','mark')

        self.msgThread = msgThread()
        self.msgThread.setMsgWindow(self.msgWindow)
        self.msgThread.start()

        self.MainThread = mainThread()
        self.MainThread.setMsgWindow(self.msgWindow)
        self.MainThread.setMianWindow(self.nvpu)
        self.MainThread.start()
        
        #进入事件循环
        self.KeyMouseMonitor()
        self.app.exec_()

    def test(self):
        print 'test'
        
    #鼠标键盘监控-----------------------------------------------------------------------
    def KeyMouseMonitor(self):
        if os.name == "nt":
            #'nt' 'mac' "posix"
            import pythoncom
            import pyHook
            self.hm = pyHook.HookManager()
            self.hm.KeyDown = self.WinKeyboardEvent
            self.hm.HookKeyboard()
            #self.hm.MouseAll = self.WinMouseboardEvent
            #self.hm.HookMouse()
            pythoncom.PumpMessages()
        else:
            pass

    def WinKeyboardEvent(self,event):
        if event.Key == 'Lmenu' or event.Key == 'Rmenu':
            if self.DoubeKeytime!= 0:
                if 100<(int(event.Time)-self.DoubeKeytime)<450:
                    self.nvpu.KeyHide()
                    print u'ALT双击'+str(int(event.Time)-self.DoubeKeytime)
                self.DoubeKeytime = 0
            else:
                self.DoubeKeytime = int(event.Time)
        else:
            self.DoubeKeytime = 0
        return True

    def WinMouseboardEvent(self,event):
        if event.MessageName == 'mouse left down':#middle
            self.MouseLeftDownPos = event.Position
        else:
            if event.MessageName == 'mouse move':
                if self.MouseLeftDownPos[1]:
                    if (event.Position[1] - self.MouseLeftDownPos[1] < -20) and (event.Position[0] - self.MouseLeftDownPos[0] < -10):
                        #print "OVER",self.MouseLeftDownPos,time.time()
                        self.nvpu.MouseHide(self.MouseLeftDownPos)
                        self.MouseLeftDownPos = [0,0]
            else:
                self.MouseLeftDownPos = [0,0]
        return True

        
if __name__=="__main__":
    app = Application()
    app.run()
    app.test()
