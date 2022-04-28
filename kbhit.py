import win32event
import win32api
import msvcrt
import sys
import select

hStdin = win32api.GetStdHandle(win32api.STD_INPUT_HANDLE);

def check_key():
    return win32event.WaitForSingleObject(hStdin,1000) == win32event.WAIT_OBJECT_0 and msvcrt.kbhit()