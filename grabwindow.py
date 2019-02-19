import time
import win32gui
from ctypes import windll

import numpy
import pywintypes
from mss import mss

import perspective_transform

# Make program aware of DPI scaling
windll.user32.SetProcessDPIAware()


def grab_window():
    while True:
        try:
            hwnd = win32gui.FindWindow("prism3d", None)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        except pywintypes.error:
            print("ETS2 Window Not Found!")
            time.sleep(5)
        else:
            width = right - left
            height = bottom - top
            game_window = {'top': top, 'left': left, 'width': width, 'height': height}
            foreground_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if foreground_window_name == "Euro Truck Simulator 2" or "American Truck Simulator":
                game_capture = numpy.array(mss().grab(game_window))
                perspective_transform.perspective_transform(game_capture)
