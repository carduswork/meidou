# -*- coding: utf-8 -*-
import pythoncom
import pyHook

time = 0
def onKeyboardEvent(event):
    print event.__dict__
    global time
    if event.Key == 'Lmenu' or event.Key == 'Rmenu':
        if time!= 0:
            if 100<(int(event.Time)-time)<450:
                print u'双击'+str(int(event.Time)-time)
            time = 0
        else:
            time = int(event.Time)
    else:
        time = 0
    return True
 
def main():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
    print 'PyHook Over'
    
if __name__ == "__main__":
    main()
