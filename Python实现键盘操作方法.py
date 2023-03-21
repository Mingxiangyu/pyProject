import time

import win32api
import win32con


class MyLibrary(object):
    # VK_CODE为键盘编码
    # 注意：此方法被操作界面必须在顶层
    def keybd_event(self, VK_CODE):
        # @Keyboard
        # input
        VK_CODE = int(VK_CODE)
        print(":::VK_CODE:", VK_CODE)
        win32api.keybd_event(VK_CODE, 0, 0, 0)
        win32api.keybd_event(VK_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)
        print(":::press", str(VK_CODE), "successfully!")
        time.sleep(2)


if __name__ == '__main__':
    # 键盘按下方向向下键
    MyLibrary().keybd_event(40)

'''
常见键盘编码：（来自百度）
ESC键VK_ESCAPE (27) 
回车键：VK_RETURN (13) 
TAB键：VK_TAB (9) 
Caps Lock键：VK_CAPITAL (20) 
Shift键：VK_SHIFT (16) 
Ctrl键：VK_CONTROL (17) 
Alt键：VK_MENU (18) 
空格键：VK_SPACE (32) 
退格键：VK_BACK (8) 
左徽标键：VK_LWIN (91) 
右徽标键：VK_RWIN (92) 
鼠标右键快捷键：VK_APPS (93) 
Insert键：VK_INSERT (45) 
Home键：VK_HOME (36) 
Page Up：VK_PRIOR (33) 
PageDown：VK_NEXT (34) 
End键：VK_END (35) 
Delete键：VK_DELETE (46) 
方向键(←)：VK_LEFT (37) 
方向键(↑)：VK_UP (38) 
方向键(→)：VK_RIGHT (39) 
方向键(↓)：VK_DOWN (40) 
F1键：VK_F1 (112) 
F2键：VK_F2 (113) 
F3键：VK_F3 (114) 
F4键：VK_F4 (115) 
F5键：VK_F5 (116) 
F6键：VK_F6 (117) 
F7键：VK_F7 (118) 
F8键：VK_F8 (119) 
F9键：VK_F9 (120) 
F10键：VK_F10 (121) 
F11键：VK_F11 (122) 
F12键：VK_F12 (123) 
Num Lock键：VK_NUMLOCK (144) 
小键盘0：VK_NUMPAD0 (96) 
小键盘1：VK_NUMPAD1 (97) 
小键盘2：VK_NUMPAD2 (98) 
小键盘3：VK_NUMPAD3 (99) 
小键盘4：VK_NUMPAD4 (100) 
小键盘5：VK_NUMPAD5 (101) 
小键盘6：VK_NUMPAD6 (102) 
小键盘7：VK_NUMPAD7 (103) 
小键盘8：VK_NUMPAD8 (104) 
小键盘9：VK_NUMPAD9 (105) 
小键盘。：VK_DECIMAL (110) 
小键盘*：VK_MULTIPLY (106) 
小键盘+：VK_ADD (107) 
小键盘-：VK_SUBTRACT (109) 
小键盘/：VK_DIVIDE (111) 
Pause Break键：VK_PAUSE (19) 
Scroll Lock键：VK_SCROLL (145)

'''
