import pytesseract
import numpy as np
import cv2
import matplotlib.pyplot as plt
import re
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
resim = cv2.imread("resim.png")

gray = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
image = gray
not_gray = resim

loading=0
metin = ""
mod = ""
siyah_beyaz = None

aranan = input("aranan metin: ")


tut = 0
sayi=0
for i in range(90, 110):
    print(20,"/",sayi)
    sayi+=1
    for j in range(tut, 8):
        image = gray
        if j == 0:
            siyah_beyaz = resim
            mod = "orijin"
        elif j == 1:
            siyah_beyaz = gray
            mod = "gri"
            tut = 2
        elif j == 2:
            (thresh, siyah_beyaz) = cv2.threshold(image, i, 255, cv2.THRESH_BINARY)
            mod = "binary"
        elif j == 3:
            (thresh, siyah_beyaz) = cv2.threshold(image, i, 255, cv2.THRESH_TOZERO)
            mod = "tozero"
        elif j == 4:
            (thresh, siyah_beyaz) = cv2.threshold(image, i, 255, cv2.CALIB_CB_ADAPTIVE_THRESH)
            mod = "calib_cb"
        elif j == 5:
            image=resim
            (thresh, siyah_beyaz) = cv2.threshold(image, i, 255, cv2.THRESH_BINARY)
            mod = "binary g"
        elif j == 6:
            image=resim
            (thresh, siyah_beyaz) = cv2.threshold(image, i, 255, cv2.THRESH_TOZERO)
            mod = "tozero g"
        elif j == 7:
            image=resim
            (thresh, siyahbeyaz) = cv2.threshold(image, i, 255, cv2.CALIB_CB_ADAPTIVE_THRESH)
            mod = "calib_cb g"

        try:
            metin = pytesseract.image_to_string(siyah_beyaz, lang="eng", timeout=0.5)
            #print(metin)
        except:
            continue

        if metin.find(aranan) != -1:
            print("Metin Bulundu:")

            d = pytesseract.image_to_data(siyah_beyaz, output_type=Output.DICT)
            keys = list(d.keys())
            n_boxes = len(d['text'])
            for k in range(n_boxes):

                if re.match(aranan, d['text'][k]):
                    (x, y, w, h) = (d['left'][k], d['top'][k], d['width'][k], d['height'][k])
                    not_gray = cv2.rectangle(not_gray, (x, y), (x + w, y + h), (0, 0, 255), 2)

            print(metin[metin.find(aranan):metin.find(aranan) + len(aranan)])
            break
    if metin.find(aranan) != -1:
        break


if metin.find(aranan) == -1:
    print("Metin yok")


"""ekranda göster"""
# print(metin)

"""boyut oranla"""

if image.shape[0] > 760|image.shape[1] > 1366:
    oran = 90
    if image.shape[0] > 800|image.shape[1] > 1400:
        oran =70
    elif image.shape[0] > 900 | image.shape[1] > 1500:
            oran = 50
    elif image.shape[0] > 1000 | image.shape[1] > 1600:
            oran = 40
    width = int(image.shape[1] * oran / 100)
    height = int(image.shape[0] * oran / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

cv2.imshow("Metin Arama",not_gray)


cv2.waitKey(0)
cv2.destroyAllWindows()
