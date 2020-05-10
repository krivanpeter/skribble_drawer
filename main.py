import os
import time

import cv2
import keyboard
import numpy as np

from pynput.mouse import Button

import menu
import settings
from file_edit import image_edit


def pixel_difference(image):
    x_diff = settings.base_pos1[0] + ((settings.full_size[0]-image.shape[0]) / 2)
    y_diff = settings.base_pos1[1] + ((settings.full_size[1]-image.shape[1]) / 2)
    differences = [x_diff, y_diff]
    return differences


def load_image(filename, image_path="pictures/"):
    image = cv2.imread(image_path + filename)
    image = cv2.flip(image, 1)
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if settings.full_size[1] < image.shape[0] or settings.full_size[0] < image.shape[1]:
        image = cv2.resize(image, (settings.full_size[1], settings.full_size[0]))
    return image


def load_positions(image):
    difference = pixel_difference(image)
    black_pixels = np.all(image < 130, axis=2)
    indices = np.where(black_pixels)

    pos_x = np.rint(indices[0] + difference[0])
    pos_y = np.rint(indices[1] + difference[1])

    # Calculate continuous pixels on Y axis
    deleted_x = 0
    deleted_y = 0
    h = 1
    while h < len(pos_y) - 1:
        if pos_x[h] == pos_x[h-1] or pos_x[h] == deleted_x + 1:
            if pos_y[h] == pos_y[h - 1] + 1 or pos_y[h] == deleted_y + 1:
                if pos_y[h] == pos_y[h + 1] - 1:
                    deleted_x = pos_x[h]
                    deleted_y = pos_y[h]
                    pos_x = np.delete(pos_x, h)
                    pos_y = np.delete(pos_y, h)
                    # h -= 1
        h += 1
    return pos_x, pos_y


def draw(filename):
    time.sleep(2)
    image = load_image(filename, image_path="pictures/")
    pos_x, pos_y = load_positions(image)

    # WHILE Clicker
    print("Drawing in progress")
    i = 0
    while i != len(pos_x):
        if keyboard.is_pressed('q'):
            print("Drawing stopped")
            time.sleep(1)
            return menu.menu()
        if pos_x[i] != len(pos_x)-1:
            settings.mouse.position = (pos_x[i], pos_y[i])
            settings.mouse.click(Button.left, 1)
            i += 1
            time.sleep(0.0001)
    print("Drawing Finished!")
    return menu.menu()


def new_search(keywords, quick="N"):
    path_to_dir = r'C:\Users\kriva\PycharmProjects\skribbl\pictures\downloaded'
    _search_params = {
        'q': keywords + " simple drawing",
        'num': 1,
    }
    settings.gis.search(search_params=_search_params, path_to_dir=path_to_dir)
    for file in os.listdir("pictures/downloaded/"):
        os.rename(r'pictures/downloaded/' + file, 'pictures/downloaded/' + keywords + ".png")
    filename = keywords + ".png"
    print("Download is in progress")
    print("Searching and downloading done for " + keywords + " keyword(s)")
    if quick != "Y":
        next_step = input("Next to edit (Y/N): ")
        if next_step == "y":
            return image_edit(filename)
        else:
            return menu.menu()
    else:
        return image_edit(filename, quick="Y")
    return menu.menu()


def main():
    menu.menu()


if __name__ == "__main__":
    main()
