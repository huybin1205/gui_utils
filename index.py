import pyautogui as pg, time, os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm
import pytesseract
import cv2
import numpy as np

PATH_FOLDER_IMAGES = os.path.join(os.path.curdir,'images','buttons')
PATH_TESSERACT_OCR = os.path.join(os.path.curdir,'Tesseract-OCR','tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = PATH_TESSERACT_OCR

def text_to_image(text, font_size=12, image_path='text_image.png'):
    # Lấy font mặc định của hệ thống
    default_font_path = fm.findfont(fm.FontProperties())
    
    # Tạo một hình ảnh trống với background trong suốt
    image = Image.new('RGBA', (1, 1), color=(255, 255, 255, 255))
    
    # Chọn phông chữ
    font = ImageFont.truetype(default_font_path, font_size)
    
    # Tính toán kích thước văn bản
    text_width, text_height = font.getsize(text)
    
    # Tạo lại hình ảnh với kích thước phù hợp với văn bản
    image = image.resize((text_width, text_height))
    
    # Tạo một hình ảnh mới với kích thước phù hợp với văn bản và background trong suốt
    image = Image.new('RGBA', (text_width, text_height), color=(255, 255, 255, 255))
    
    # Vẽ văn bản nằm chính giữa hình ảnh
    draw = ImageDraw.Draw(image)
    text_x = (text_width - draw.textsize(text, font=font)[0]) // 2
    text_y = (text_height - draw.textsize(text, font=font)[1]) // 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
    
    # Lưu hình ảnh thành tệp
    image.save(image_path)
    print(f"Đã chuyển đổi văn bản thành hình ảnh và lưu thành công: {image_path}")

def searchImageAndClick(description = '', path_imgs = '', x = 0, y = 0, click_quantity = 1, confidence = 0.8):
    if type(path_imgs) is str:
        path_imgs = [path_imgs]

    while True:
        for path_img in path_imgs:
            try:
                isExist = True
                if not os.path.isfile(path_img):
                    isExist = False
                    if os.path.isfile(os.path.join(PATH_FOLDER_IMAGES, path_img)):
                        isExist = True
                        path_img = os.path.join(PATH_FOLDER_IMAGES, path_img)

                if isExist:
                    print(f" Looking for {description} ({path_img})")
                    position = pg.locateCenterOnScreen(path_img, grayscale=True, confidence=confidence)
                    if position != None:
                        for click in range(click_quantity):
                            pg.click(position)

                        return position
                    else:
                        print(f"{description} not found on the screen.")
                else:
                    print(f'{description} not found')

            except Exception as e:
                print("An error occurred:", str(e))

def click_on_text(texts, lang='eng', x_extra = 0, y_extra = 0, click_quantity = 1, click_index_image = -1):
    positions = []
    while True:
        for text in texts:
            words = str(text).split(' ')

            if len(words) == 1 & click_index_image != -1:
                click_index_image = 0

            for word in words:
                print(f" Looking for {word}")

                # Take a screenshot of the main screen
                screenshot = pg.screenshot()

                # Convert the screenshot to grayscale
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

                # Loại bỏ nhiễu bằng bộ lọc Gauss
                img = cv2.GaussianBlur(img, (5, 5), 0)

                # Tăng cường đối tượng bằng làm tăng độ tương phản
                img = cv2.convertScaleAbs(img, alpha=1, beta=0)

                # Apply image thresholding to separate text from background
                _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                # cv2.imshow('Original Image', img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # return
                # Find the provided text (text) on the grayscale screenshot 
                # using the provided language (lang)
                config = r'--oem 3 --psm 6'
                data = pytesseract.image_to_data(img,lang=lang, output_type='data.frame',config=config)

                # Find the coordinates of the provided text (text)
                try:
                    click_index_images = range(click_index_image, len(data[data['text'] == word]['left']))
                    for i in click_index_images:
                        position = data[data['text'] ==
                                    word]['left'].iloc[i], data[data['text'] == word]['top'].iloc[i]
                        
                        if len(position) > 1:
                            # Text was found, return the coordinates
                            positions.append(position)
                        else:
                            print(f"{word} not found on the screen.")
                except Exception as e:
                    print("An error occurred:", str(e))

        if len(positions) > 0:
            if click_index_image == -1:
                for position in positions:
                    pg.click(position)
                
                return positions
            else:
                print(positions)
                y_counts = {}
                x_sums = {}
                
                for x, y in positions:
                    if y in y_counts:
                        y_counts[y] += 1
                        x_sums[y] += x
                    else:
                        y_counts[y] = 1
                        x_sums[y] = x
                
                sorted_y_counts = sorted(y_counts.items(), key=lambda x: x[1], reverse=True)
                most_common_y = sorted_y_counts[0][0]
                x_average = x_sums[most_common_y] / y_counts[most_common_y]    

                for click in range(click_quantity):
                    pg.click((x_average + x_extra ,most_common_y + y_extra))

                return [(x_average, most_common_y)]

if __name__ == '__main__':
    # click_on_image('Task',[r"buttons_web\tasks.png"])
    # click_on_text(['Work items'],lang='eng',click_index_image=2)
    pass