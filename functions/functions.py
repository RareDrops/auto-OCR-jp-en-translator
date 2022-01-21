from PIL import ImageGrab, ImageOps, Image
#import pytesseract
from functions.translatordeepl import deepl_translator
import easyocr

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#def image_reader(coordinates):
#    im = ImageGrab.grab(bbox=coordinates)
#    im = ImageOps.grayscale(im)
#    im = ImageOps.invert(im.convert("L"))
#    im.save("./Assets/screenshot_area.png")
#    result = pytesseract.image_to_string(Image.open('./Assets/screenshot_area.png'), lang='jpn')
#    result = "".join(result.split()) #removes whitespace
#    deepl_translator(result)
#    return image_reader


reader= easyocr.Reader(['ja'])

def image_reader(coordinates):
    im =  ImageGrab.grab(bbox=coordinates)
    im = ImageOps.grayscale(im)
    im.save("./Assets/screenshot_area.png")
    result = reader.readtext("./Assets/screenshot_area.png")
    sentence = ""
    for element in result:
        sentence += element[1] + " "
    deepl_translator(sentence)
    