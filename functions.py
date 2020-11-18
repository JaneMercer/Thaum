from getWindow import get_image_, get_window
from cv2 import imshow, waitKey

exe_name = 'java.exe'
window_HWNDs = []

def get_screen():
    global window_HWNDs
    if not window_HWNDs:
        res_window_HWNDs, all_PIDs = get_window(exe_name)  # tries to find a new window handle by process name
        window_HWNDs = res_window_HWNDs

    if window_HWNDs:  # if window handle was found
        for curr_window_hwnd in window_HWNDs:
            result = get_image_(curr_window_hwnd)
            if not result: print("OPS!")
        else:
            imshow('screen', result)
            k = waitKey(33)
            return result

    else:
        print("Sorry, No window was found")
        run = 0
