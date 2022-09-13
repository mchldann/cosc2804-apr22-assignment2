import os
import sys
import select
from utils import is_windows

if is_windows:
    import win32event
    import win32api
    import msvcrt

    hStdin = win32api.GetStdHandle(win32api.STD_INPUT_HANDLE)


def check_key():
    if is_windows:
        return (
            win32event.WaitForSingleObject(hStdin, 1000) == win32event.WAIT_OBJECT_0
            and msvcrt.kbhit()
        )
    else:
        _, w, _ = select.select([], [sys.stdin], [], 0)
        return len(w)
