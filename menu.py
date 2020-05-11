import time
import keyboard
import pyautogui
import win32api
import main
import file_edit
from os.path import isfile, join
import sys
import os
import glob

import settings

state_left = win32api.GetKeyState(0x01)


def find_file(keywords, image_path="pictures/"):
    found = glob.glob(image_path + keywords + "*")
    if not found:
        return False
    else:
        filename = os.path.basename(found[0])
        return filename


def on_move():
    while True:
        if keyboard.is_pressed('q'):
            print("Selection cancelled")
            return menu()
        a = win32api.GetKeyState(0x01)
        x, y = pyautogui.position()
        position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(position_str, end='')
        print('\b' * len(position_str), end='', flush=True)
        if a != state_left:
            if a < 0:
                time.sleep(0.1)
                return x, y


def menu(image_path="pictures/"):
    print("_____________________________")
    print("Please choose from below:")
    print("_____________________________")
    print("[1]: Quick Draw")
    print("[2]: New Drawing")
    print("[3]: New Search")
    print("[4]: Edit Image")
    print("[5]: Edit Image Outline")
    print("_____________________________")
    print("[6]: New Drawing Area")
    print("[7]: EXIT")
    print("_____________________________")
    chosen = input("Input: ")
    if chosen == "1":
        keywords = input("Please add keyword(s):\n")
        print("_____________________________")
        if find_file(keywords) is False:
            return main.new_search(keywords, quick="Y")
        else:
            return main.draw(find_file(keywords))
    elif chosen == "2":
        print("Please choose a file:")
        print("_____________________________")
        onlyfiles = [f for f in os.listdir(image_path) if isfile(join(image_path, f))]
        for image in onlyfiles:
            print("- " + image)
        print("_____________________________")
        filename = input("Input: ")
        if find_file(filename) is False:
            return print("The file doesn't exist")
        else:
            return main.draw(find_file(filename))
    elif chosen == "3":
        keywords = input("Please add keyword(s):")
        print("_____________________________")
        return main.new_search(keywords)
    elif chosen == "4":
        print("Please choose a file:")
        print("_____________________________")
        onlyfiles = [f for f in os.listdir(image_path + "downloaded/") if isfile(join(image_path + "downloaded/", f))]
        for image in onlyfiles:
            print("- " + image)
        print("_____________________________")
        filename = input("Input: ")
        if find_file(filename, image_path="pictures/downloaded/") is False:
            return print("The file doesn't exist")
        else:
            return file_edit.image_edit(find_file(filename, image_path="pictures/downloaded/"))
    elif chosen == "5":
        print("Please choose a file:")
        print("_____________________________")
        onlyfiles = [f for f in os.listdir(image_path) if isfile(join(image_path, f))]
        for image in onlyfiles:
            print("- " + image)
        print("_____________________________")
        onlyfiles = [f for f in os.listdir(image_path) if isfile(join(image_path, f))]
        for image in onlyfiles:
            print("- " + image)
        print("_____________________________")
        filename = input("Input: ")
        if find_file(filename) is False:
            return print("The file doesn't exist")
        else:
            return file_edit.image_outline(find_file(filename))
    elif chosen == "6":
        print("Please select a new drawing area by clicking on the")
        print("top left corner and on the right bottom corner of it")
        print("_____________________________")
        x1, y1 = on_move()
        print('X: ' + str(x1).rjust(4) + ' Y: ' + str(y1).rjust(4))
        x2, y2 = on_move()
        print('X2: ' + str(x2).rjust(4) + ' Y2: ' + str(y2).rjust(4))
        settings.base_pos1 = x1, y1
        settings.base_pos2 = x2, y2
        settings.full_size[0] = abs(settings.base_pos1[0]-settings.base_pos2[0])
        settings.full_size[1] = abs(settings.base_pos1[1]-settings.base_pos2[1])
        print("New drawing area selected")
        return menu()
    elif chosen == "7":
        sys.exit()
    else:
        return ()
