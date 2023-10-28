from screen_search import *
import pyautogui as pg
import time

def searchImageAndClick(fileName, img, x, y):
    search = Search("images/buttons/" + img)
    while True:
        pos = search.imagesearch()
        print(fileName + " Đang tìm..." + img)
        if pos[0] != -1:
            print(pos)
            pg.click(pos[0] + x, pos[1] + y)
            return
        time.sleep(2)

def searchImageAndMultiClick(fileName, img, quantity, x, y):
    search = Search("images/buttons/" + img)
    while True:
        pos = search.imagesearch()
        print(fileName + " Đang tìm..." + img)
        if pos[0] != -1:
            print(pos)
            for i in range(quantity):
                pg.click(pos[0] + x, pos[1] + y)
            return True
        time.sleep(2)


def isCheckDisplayImageOnScreen(fileName, img):
    search = Search("images/buttons/" + img)
    count = 0
    while True:
        pos = search.imagesearch()
        # print(fileName + " Đang tìm..." + img)
        if pos[0] != -1:
            return True
        else:
            count += 1
        if count > 1:
            return False
        time.sleep(1)