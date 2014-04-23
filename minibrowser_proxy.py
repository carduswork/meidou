# -*- coding: utf-8 -*-
import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class BrowserWidget(QWidget):
    def __init__(self,HOMEPAGE = "http://www.baidu.com/",CookiesForUrl = None,parent=None):
        super(self.__class__, self).__init__(parent)
        self.browser = QWebView()
        self.lineedit = QLineEdit()

        self.CookieButton = QPushButton(u"请先登录，然后点击我")
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.CookieButton)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        self.connect(self.lineedit, SIGNAL("returnPressed()"), self.entrytext)
        self.connect(self.CookieButton, SIGNAL('clicked()'), self.CookieOk)

        self.CookiesForUrl = CookiesForUrl
        if not self.CookiesForUrl:
            self.CookiesForUrl = HOMEPAGE
            
        self.browser.load(QUrl(HOMEPAGE))
        self.browser.show()
        
    def entrytext(self):
        self.browser.load(QUrl(self.lineedit.text()))
        
    def CookieOk(self):
        self.cookies = []
        for citem in self.browser.page().networkAccessManager().cookieJar().cookiesForUrl(QUrl(self.CookiesForUrl)):
            self.cookies.append('%s=%s' % (citem.name(), citem.value()))
            #self.cookies = common.to_unicode('; '.join(self.cookiescookies))
        return self.cookies
    
class Window(QMainWindow):
    def __init__(self,TITLE = u"请登录，完成后点击按钮",parent=None):
        super(self.__class__, self).__init__(parent)
        self.browserWindow = BrowserWidget()
        self.setCentralWidget(self.browserWindow)
        self.setWindowTitle(TITLE)

        status = self.statusBar()
        status.setSizeGripEnabled(True)

        self.label = QLabel("")
        status.addWidget(self.label, 1)

        self.connect(self.browserWindow.browser, SIGNAL("loadFinished(bool)"), self.loadFinished)
        self.connect(self.browserWindow.browser, SIGNAL("loadProgress(int)"), self.loading)

        self.cookie = []
        
    def loadFinished(self, flag):
        if self.cookie:
            if self.cookie != self.browserWindow.CookieOk():
                self.cookie = self.browserWindow.CookieOk()
                print self.cookie,'diff'
        else:
            self.cookie = self.browserWindow.CookieOk()
            print self.cookie
            
        self.label.setText(u"完毕")

    def loading(self, percent):
        self.label.setText("Loading %d%%" % percent)
        self.browserWindow.lineedit.setText(self.browserWindow.browser.url().toString())

if __name__ == '__main__':
    QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, "127.0.0.1", 8087))
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
