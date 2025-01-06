from PIL import ImageGrab, ImageOps
from functions.translatordeepl import deepl_translator
import easyocr
import io

previous=None
previous_translated=None

reader= easyocr.Reader(['ja'],gpu=True)

def image_reader(coordinates):
    im =  ImageGrab.grab(bbox=coordinates)
    im = ImageOps.grayscale(im)
    byte_img = io.BytesIO()
    im.save(byte_img, format="PNG")
    byte_img = byte_img.getvalue()
    result = reader.readtext(byte_img)
    sentence = ""
    for element in result:
        sentence += element[1] + " "
    raw_text, translated = deepl_translator(sentence)
    return (raw_text, translated)
    

def auto_image_reader(coordinates):
    global previous, previous_translated
    im =  ImageGrab.grab(bbox=coordinates)
    im = ImageOps.grayscale(im)
    byte_img = io.BytesIO()
    im.save(byte_img, format="PNG")
    byte_img = byte_img.getvalue()
    result = reader.readtext(byte_img)
    sentence = ""
    for element in result:
        sentence += element[1] + " "
    if sentence == previous:
        return None
    else:
        previous = sentence
        translated =  deepl_translator(sentence)
        previous_translated = translated
        return translated