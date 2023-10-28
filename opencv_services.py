import cv2
import numpy as np
import pyautogui
import pytesseract
import os
import matplotlib.font_manager as fm
from PIL import Image, ImageDraw, ImageFont

PATH_FOLDER_IMAGES = os.path.join(os.path.curdir,'images','buttons')
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

def is_exist_file(path_img):
    if not os.path.isfile(path_img):
        if not os.path.isfile(os.path.join(PATH_FOLDER_IMAGES, path_img)):
            return f'{path_img} not found'
    return True

def get_default_font():
    prop = fm.FontProperties()
    default_font = prop.get_name()
    return default_font

def create_image_from_text(text, image_path, font=None, font_size=24, padding = 10):
    if font is None:
        font = get_default_font()

    font_scale = font_size / 24.0
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)

    image_width = text_size[0] + 2 * padding
    image_height = text_size[1] + 2 * padding

    image = np.zeros((image_height, image_width, 4), dtype=np.uint8)
    image.fill(255)

    text_x = padding
    text_y = padding + text_size[1]
    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imwrite(image_path, image)


def click_on_text(target_text):
    try:
        screen = pyautogui.screenshot()
        print(type(screen))
        screen = np.array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        text = pytesseract.image_to_string(screen)
        if target_text in text:
            text_location = text.index(target_text)
            text_center = pyautogui.locateCenterOnScreen(target_text)
            pyautogui.click(text_center)
            print("Text found and clicked!")
        else:
            print("Text not found on the screen.")
    except Exception as e:
        print("An error occurred:", str(e))

def click_on_image(description = '', path_imgs = '', x = 0, y = 0, click_quantity = 1, threshold = 0.8):
    while True:
        for path_img in path_imgs:
            try:
                if not os.path.isfile(path_img):
                    if not os.path.isfile(os.path.join(PATH_FOLDER_IMAGES, path_img)):
                        return f'{description} not found'

                print(f" Looking for {description} ({path_img})")

                icon = cv2.imread(path_img)
                screen = pyautogui.screenshot()
                screen = np.array(screen)
                screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

                result = cv2.matchTemplate(screen, icon, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = np.where(result >= threshold)
                if len(loc[0]) > 0 and len(loc[1]) > 0:
                    top_left = (loc[1][0], loc[0][0])
                    icon_center = ((top_left[0] + icon.shape[1] // 2) + x, (top_left[1] + icon.shape[0] // 2) + y)
                    for click in click_quantity:
                        pyautogui.click(icon_center)

                    return icon_center
                else:
                    print(f"{description} not found on the screen.")
            except Exception as e:
                print("An error occurred:", str(e))

def find_image_on_screen(image_path):
    try:
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(image_path, 0)
        template_width, template_height = template.shape[::-1]

        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)

        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                bottom_right = (pt[0] + template_width, pt[1] + template_height)
                pyautogui.click(bottom_right)

            print("Clicked on", len(loc[0]), "occurrences of the image.")
        else:
            print("Image not found on the screen.")

    except Exception as e:
        print("An error occurred:", str(e))



if __name__ == '__main__':
    # Văn bản bạn muốn tạo hình ảnh và tìm trên màn hình
    text = "Login"
    image_path = "text_image.png"

    # Tạo hình ảnh từ văn bản
    create_image_from_text(text, image_path)

    # Tìm và click vào hình ảnh trên màn hình
    find_image_on_screen(image_path)