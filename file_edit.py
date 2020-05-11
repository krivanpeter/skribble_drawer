import os
from PIL import Image
import settings
import cv2
import menu
import main


def image_edit(filename, quick="N", image_path="pictures/"):
    image_file = Image.open(image_path + "downloaded/" + filename)
    if image_file.width > settings.img_final_sizes[0]\
            or image_file.height > settings.img_final_sizes[1]:
        image_file.thumbnail(settings.img_final_sizes)
    image_file.save(image_path + filename, "PNG")
    image_file.close()

    print("Image has been edited")
    if quick != "Y":
        delete_dowloaded = input("Delete downloaded file (Y/N): ")
        if delete_dowloaded == "y":
            os.remove(image_path + "downloaded/" + filename)
            print("Downloaded file deleted")
        next_step = input("Next to outline (Y/N): ")
        if next_step == "y":
            return image_outline(filename)
        else:
            return menu.menu()
    else:
        os.remove(image_path + "downloaded/" + filename)
        print("Downloaded file deleted")
        return image_outline(filename, quick="Y")
    return menu()


def image_outline(filename, quick="N", image_path="pictures/"):
    image = cv2.imread(image_path + filename, 0)
    edges = cv2.Canny(image, 200, 250)
    edges = cv2.bitwise_not(edges)
    cv2.imwrite(image_path + filename, edges)
    print("Image has been outlined")
    if quick != "Y":
        next_step = input("Next to drawing (Y/N): ")
        if next_step == "y":
            return main.draw(filename)
        else:
            return menu.menu()
    else:
        return main.draw(filename)
    return menu.menu()
