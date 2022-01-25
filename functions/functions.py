from PIL import ImageGrab, ImageOps
from functions.translatordeepl import deepl_translator
import easyocr

previous=None
previous_translated=None

reader= easyocr.Reader(['ja'],gpu=True)

def image_reader(coordinates):
    im =  ImageGrab.grab(bbox=coordinates)
    im = ImageOps.grayscale(im)
    im.save("./Assets/screenshot_area.png")
    result = reader.readtext("./Assets/screenshot_area.png")
    sentence = ""
    for element in result:
        sentence += element[1] + " "
    translated = deepl_translator(sentence)
    return translated
    

def auto_image_reader(coordinates):
    global previous, previous_translated
    im =  ImageGrab.grab(bbox=coordinates)
    im = ImageOps.grayscale(im)
    im.save("./Assets/screenshot_area.png")
    result = reader.readtext("./Assets/screenshot_area.png")
    sentence = ""
    for element in result:
        sentence += element[1] + " "
    if sentence == previous:
        return previous_translated
    else:
        previous = sentence
        translated =  deepl_translator(sentence)
        previous_translated = translated
        return translated