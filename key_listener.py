from pynput import keyboard
from functions import get_screen

# shift + z для создания скрина. Хранить в памяти только 2 последних скрина. по shift + {1,2,3,4+}
# запускать определение текста на скринах и поиск цепочки размером соотв. кнопке - вывести результат
# ctrl + q для выхода
EXIT = {keyboard.KeyCode(char='c'), keyboard.Key.ctrl_l}
MAKE_SCREEN = [{keyboard.KeyCode(char='z'), keyboard.Key.shift},
               {keyboard.KeyCode(char='Z'), keyboard.Key.shift}]
FIND_CHAIN = [{keyboard.KeyCode(char='1'), keyboard.Key.tab},
               {keyboard.KeyCode(char='2'), keyboard.Key.tab},
               {keyboard.KeyCode(char='3'), keyboard.Key.tab},
               {keyboard.KeyCode(char='4'), keyboard.Key.tab},
               {keyboard.KeyCode(char='5'), keyboard.Key.tab},
               {keyboard.KeyCode(char='6'), keyboard.Key.tab},
               {keyboard.KeyCode(char='7'), keyboard.Key.tab},
               {keyboard.KeyCode(char='8'), keyboard.Key.tab}]

# The currently active modifiers
current = set()
screen_arr = []

def on_press(key):
    #EXIT
    if key in EXIT:
        current.add(key)
        if all(k in current for k in EXIT):
            print("Exiting..")
            listener.stop()
    #MAKE A SCREENSHOT
    elif any([key in comb for comb in MAKE_SCREEN]):
        current.add(key)
        if any(all(k in current for k in comb) for comb in MAKE_SCREEN):
            print('Click!')
            screen_arr = get_screen()
            # TODO: append to screen_arr (it has to have <=2 images, if new comes in - [0] erases)
    #FIND CHAIN
    elif any([key in comb for comb in FIND_CHAIN]):
        current.add(key)
        print(key)
        if any(all(k in current for k in comb) for comb in FIND_CHAIN):
            for k in current:
                try:
                    length = int(k.char)
                except Exception:
                    pass
            print('Chain size: {}\n'.format(length))
#            TODO: check if the are 2 screenshots
#            TODO: find the chain




# if any([key in comb for comb in KeyComb_Quit]):
# if any(all(k in current for k in comb) for comb in EXIT):


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


def run():
    global listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
