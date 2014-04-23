# -*- coding: utf-8 -*-
import sys
from Queue import deque
from PyQt4 import QtCore,QtGui,phonon

class QGraphicsPixmapItem2(QtGui.QGraphicsPixmapItem):
    def __init__(self,parent=None):
        super(QGraphicsPixmapItem2,self).__init__(parent)
        self.setAcceptHoverEvents(True)

    '''
    def pixmap(self):
        return self.pix
    
    def setPixmap(self,pix):
        self.pix = pix

    def boundingRect (self):
        return QtCore.QRectF(0,0,50,50)


    def paint(self,painter,option,widget):
        painter.drawPixmap(QtCore.QRect(0,0,50,50),QtGui.QPixmap('btn_hover.png'))
    '''

    def mousePressEvent(self,event):
        print 'mousePressEvent'

    def enterEvent(self,event):
        print 'enterEvent'

    def leaveEvent(self,event):
        print 'leaveEvent'

    def mouseReleaseEvent(self,event):
        print 'mouseReleaseEvent'

    def hoverMoveEvent(self,event):
        print 'hoverMoveEvent'

    def hoverLeaveEvent(self,event):
        print 'hoverLeaveEvent'

    def hoverEnterEvent(self,event):
        print 'hoverEnterEvent'

class yes(QGraphicsPixmapItem2):
    def __init__(self,parent=None):
        super(yes,self).__init__(parent)
        self.setPixmap(QtGui.QPixmap('ok_normal.png'))
        self.pix = 'ok_normal.png'

    def hoverLeaveEvent(self,event):
        self.setPixmap(QtGui.QPixmap('ok_normal.png'))

    def hoverEnterEvent(self,event):
        self.setPixmap(QtGui.QPixmap('ok_hover.png'))
        
class no(QGraphicsPixmapItem2):
    def __init__(self,parent=None):
        super(no,self).__init__(parent)
        self.setPixmap(QtGui.QPixmap('cancel_normal.png'))
        self.pix = 'cancel_normal.png'

    def hoverLeaveEvent(self,event):
        self.setPixmap(QtGui.QPixmap('cancel_normal.png'))

    def hoverEnterEvent(self,event):
        self.setPixmap(QtGui.QPixmap('cancel_hover.png'))

class icon2(QGraphicsPixmapItem2):
    def __init__(self,icon,parent=None):
        super(icon2,self).__init__(parent)
        if not icon:icon='ok_normal.png'
        self.setPixmap(QtGui.QPixmap(icon))
        self.pix = icon
 
    #def hoverLeaveEvent(self,event):
        #self.setPixmap(QtGui.QPixmap('cancel_normal.png'))

    def hoverEnterEvent(self,event):
        self.setPixmap(QtGui.QPixmap(self.pix))

    def paint(self,painter,option,widget):
        if self.pix != 'ok_normal.png' or self.pix != 'cancel_normal.png':
            painter.drawPixmap(QtCore.QRect(5,5,30,30),QtGui.QPixmap(self.pix))
        
class txt(QtGui.QGraphicsTextItem):
    def __init__(self,parent=None):
        super(txt,self).__init__(parent)
        #self.setText(txt)
        #self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents,True)
        
class choiceSq(QGraphicsPixmapItem2):
    def __init__(self,ph=None,father=None,num=None,parent=None):
        super(choiceSq,self).__init__(parent)
        self.setPixmap(QtGui.QPixmap('list_normal.png'))
        self.pix = 'list_normal.png'
        self.ph = ph
        self.father = father
        self.num = num

    def hoverLeaveEvent(self,event):
        self.setPixmap(QtGui.QPixmap('list_normal.png'))

    def hoverEnterEvent(self,event):
        self.setPixmap(QtGui.QPixmap('list_hover.png'))
        self.ph.stop()
        self.ph.play()

    def mousePressEvent(self,event):
        self.father.result = self.num
        print self.num
        self.father.loop.exit()
        
 
class optionScene(QtGui.QGraphicsScene):
    def __init__(self,nvpu=None,option=None,ph=None,loop=None,parent=None):
        super(optionScene,self).__init__(parent)
        self.option = option
        #self.setSceneRect(0,0,400,300)
        self.optionGroup = OptionGroup(self)
        self.optionGroup.loop = loop
        #self.optionGroup.addITEM2(ph)

        #self.option = [['','./cache/gph159821.jpg','msg'],[None,'cancel_normal.png','msg']]
        #self.option = [['cancel_normal.png','cancel_normal.png','msg'],[None,None,'msg'],[None,None,'msg'],[None,None,'msg'],[None,None,'msg']]
        
        if self.option:
            n = 0
            for i in self.option:
                self.optionGroup.addITEM3(ph,n,i)
                n += 1
            self.optionGroup.setItemPos(1366/2,768/2)
        else:
            self.optionGroup.addITEM2(ph)
            
class OneChoice():
    def __init__(self,num,background,icon,text,ph,OptionGroup):
        num = str(num)
        self.num = num
        exec('self.background' + num + '= choiceSq(ph,OptionGroup,' + num + ')')
        exec('self.text' + num + '= txt(text)')
        exec('self.icon' + num + '= icon2(icon)')        
        exec('self.background = self.background' + num)
        exec('self.icon = self.icon' + num)
        exec('self.text = self.text' + num)
        
    def setPos(self,x,y):
        exec('self.background' + self.num + '.setPos(x,y)')
        exec('self.text' + self.num + '.setPos(x+60,y+12)')
        exec('self.icon' + self.num + '.setPos(x+5,y+3)')
        
    
class OptionGroup(QtCore.QObject):
    def __init__(self,scene,parent = None):
        super(OptionGroup,self).__init__(parent)
        self.scene = scene
        self.items = deque()

    def addITEM(self,ITEM):
        self.scene.addItem(ITEM)
        self.items.append(ITEM)

    def setItemPos(self,x,y):
        if len(self.items)%2:half = 46
        else:half = 4
        Y = y-half/2-50*len(self.items)/2
        for i in self.items:
            print x
            i.setPos(x,Y)
            Y = Y + 50
        
    def addITEM3(self,ph,num,oneOption):
        C = OneChoice(num,oneOption[0],oneOption[1],oneOption[2],ph,self)
        self.scene.addItem(C.background)
        self.scene.addItem(C.icon)
        self.scene.addItem(C.text)
        self.items.append(C)
        
    def addITEM2(self,ph=None):
        ChoiceSq = choiceSq(ph,self)
        self.scene.addItem(ChoiceSq)
        self.items.append(ChoiceSq)
        
        Yes = yes()
        Yes.setPos(5,3)
        self.scene.addItem(Yes)
        self.items.append(Yes)

        txtYes = txt(u'确定')
        txtYes.setPos(70,12)
        self.scene.addItem(txtYes)
        self.items.append(txtYes)
        
        ChoiceSq2 = choiceSq(ph,self)
        ChoiceSq2.setPos(0,50)
        self.scene.addItem(ChoiceSq2)
        self.items.append(ChoiceSq2)
        
        No = no()
        No.setPos(5,53)
        self.scene.addItem(No)
        self.items.append(No)

        txtNo = txt(u'取消')
        txtNo.setPos(70,62)
        self.scene.addItem(txtNo)
        self.items.append(txtNo)

    def tail(self):
        if not self.items:return
        return self.items[-1]



class ExtenWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(ExtenWindow,self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        #self.setStyleSheet('''background-color:cyan;''')
        self.setStyleSheet('color:rgba(127,127,127,0.5);')
        self.setWindowOpacity(0.5)
        desktop = QtGui.QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        
class optionMenu(QtGui.QWidget):
    def __init__(self,nvpu=None,option=None,parent=None):
        super(optionMenu,self).__init__(parent)
        self.loop = QtCore.QEventLoop(self)
        
        #option = [['icon.png','msg'],['icon.png','msg'],['icon.png','msg']]

        self.ph = phonon.Phonon.createPlayer(phonon.Phonon.MusicCategory)
        self.ph.setTickInterval(1000)
        self.ph.setCurrentSource(phonon.Phonon.MediaSource(QtCore.QString("choice.wav")))
        self.ph.play()
        self.ph.pause()
        
        self.scene = optionScene(nvpu,option,self.ph,self.loop)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setStyleSheet("background: transparent;border:0px")
        self.view.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
        self.view.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.view.show()
        
        desktop =QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()

        
        #self.view.setPos(nvpu.pos().x()-200,nvpu.pos().y()-200)

        #self.setMouseTracking(True)
        
    def setVisible(self,visible):
        if (not visible and self.loop):
            self.loop.exit()

    def result(self):
        return self.scene.optionGroup.result
    
    def open(self):
        self.setWindowModality(QtCore.Qt.WindowModal)
        #self.setWindowModality(QtCore.Qt.WindowModal)
        self.view.show()

    def exec_(self):
        #self.setAttribute(QtCore.Qt.WA_ShowModal,True)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.view.show()
        #self.loop = QtCore.QEventLoop()
        self.loop.exec_()
        return 1




        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    option = optionMenu()
    #a = ExtenWindow()
    #a.show()
    option.view.move(400,400)
    app.exec_()












