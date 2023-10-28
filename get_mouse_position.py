import pyautogui as pg
import os, time

while True:
    print(pg.position())
    time.sleep(1)
    # 1571  583    
    pg.move((1571,583))