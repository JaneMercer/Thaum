import psutil
import win32gui
import win32ui
import win32process
import ctypes
import numpy as np
import cv2
import time


def enum_window_callback(hwnd, pid_and_windows):
    pid, windows = pid_and_windows
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == current_pid and win32gui.IsWindowVisible(hwnd):
        windows.append(hwnd)


def get_window(w_name):
    try:
        instansess = [item for item in psutil.process_iter() if item.name() == w_name]
        _PIDs = [item.pid for item in instansess]

        if instansess:
            window_HWNDs = []

            for pid in _PIDs:
                win32gui.EnumWindows(enum_window_callback, [pid, window_HWNDs])

            return (window_HWNDs, _PIDs)
        else:
            print("Process ", w_name, " was not found.")
            return ([], [])

    except Exception as e:
        print(e)
        return ([], [])


def resize(im, coef):  # resizes the image by coef
    MAX_SIZE = 2000
    MIN_SIZE = 10
    width = int(im.shape[1] * coef)
    height = int(im.shape[0] * coef)
    dsize = (width, height)

    if width > MIN_SIZE or height > MIN_SIZE or height < MAX_SIZE or width < MAX_SIZE:
        return cv2.resize(im, dsize)
    else:
        print("Resized image is to small or to big. No resizing was done.")
        return im


def process_image(im):  # processes the image the way you want
    image2 = resize(im, 0.9)
    hsv = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([86, 165, 254]), np.array([93, 174, 256]))  # masks specific color range
    nonzero = cv2.findNonZero(mask)
    x, y, w, h = cv2.boundingRect(nonzero)
    temp = mask[y:y+h, x:x+w]
    res = cv2.copyMakeBorder(temp.copy(), 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=(0,0,0))
    res = cv2.bitwise_not(res)

    # blank_image = image2.copy()
    # blank_image[:] = (0, 0, 255)
    # res = cv2.bitwise_and(blank_image, blank_image, mask=mask)  # applies mask to the image and shows result on black bg
    return res


def win_create_bitmap(window, w, h, left, top):
    # hwndDC = win32gui.GetDC(window)
    hwndDC = win32gui.GetWindowDC(window)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    result = ctypes.windll.user32.PrintWindow(window, saveDC.GetSafeHdc(),
                                              1)  # BOOL PrintWindow(HWND hwnd,HDC  hdcBlt,UINT nFlags;
    if result == 1:
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = np.fromstring(bmpstr, dtype='uint8')
        img.shape = (h, w, 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(window, hwndDC)

    if result:
        return img, result
    else:
        return None, result


def get_image_(window):
    # print("|DEBUG| Current window HNDL: ", window)
    bbox = win32gui.GetWindowRect(window)
    left, top, right, bot = bbox
    w = right - left
    h = bot - top

    if (w > 0 and h > 0):
        try:
            win_img, bool_img = win_create_bitmap(window, w, h, left, top)
            if bool_img:
                cv_img = cv2.cvtColor(win_img, cv2.COLOR_RGBA2RGB)
                result = process_image(cv_img)
                # cv2.imshow("screen",result)
                # cv2.waitKey()
                return result

        except Exception as e:
            print(e)
            return []
    else:
        print(" ... Ops!Window to small. \n")
        return []
