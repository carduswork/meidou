# -*- coding: utf-8 -*-
import pythoncom
import pyHook
 
def onMouseEvent(event):
    # 监听鼠标事件
    print "MessageName:", event.MessageName
    print "Message:", event.Message
    print "Time:", event.Time
    print "Window:", event.Window
    print "WindowName:", event.WindowName
    print "Position:", event.Position
    print "Wheel:", event.Wheel
    print "Injected:", event.Injected
    print "---"
    print event.Position[0]
    return True
 
def onKeyboardEvent(event):
    # 监听键盘事件
    print "MessageName:", event.MessageName
    print "Message:", event.Message
    print "Time:", event.Time
    print "Window:", event.Window
    print "WindowName:", event.WindowName
    print "Ascii:", event.Ascii, chr(event.Ascii)
    print "Key:", event.Key
    print "KeyID:", event.KeyID
    print "ScanCode:", event.ScanCode
    print "Extended:", event.Extended
    print "Injected:", event.Injected
    print "Alt", event.Alt
    print "Transition", event.Transition
    print "---"
 
    # 同鼠标事件监听函数的返回值
    return True

#MouseLeftDownPosY = 0
MouseLeftDownPos = [0,0]
def WinMouseboardEvent(event):
    #global MouseLeftDownPosY
    global MouseLeftDownPos
    if event.MessageName == 'mouse left down':
        #MouseLeftDownPosY = event.Position[1]
        MouseLeftDownPos = event.Position
    else:
        if event.MessageName == 'mouse move':
            #if MouseLeftDownPosY:
            if MouseLeftDownPos[1]:
                #if event.Position[1] - MouseLeftDownPosY < -20:
                if (event.Position[1] - MouseLeftDownPos[1] < -20) and (event.Position[0] - MouseLeftDownPos[0] < -10):
                    #print "OVER",MouseLeftDownPosY
                    print "OVER",MouseLeftDownPos
                    #MouseLeftDownPosY = 0
                    MouseLeftDownPos = [0,0]
        else:
            #MouseLeftDownPosY = 0
            MouseLeftDownPos = [0,0]
    return True

def main():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    hm.MouseAll = WinMouseboardEvent#onMouseEvent
    hm.HookMouse()
    pythoncom.PumpMessages()
    

            
if __name__ == "__main__":
    main()
