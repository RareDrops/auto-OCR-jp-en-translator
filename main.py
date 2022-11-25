from tkinter import Tk,font, StringVar, RAISED, BOTH, RIGHT
from tkinter.ttk import Frame, Button, Style, Label
from functions import functions
import cv2
from PIL import ImageGrab
from configparser import ConfigParser 
import threading
import queue
#loads the configuration file and reads it
config = ConfigParser()
config.read('config.ini')


click1 = False
point1 = (0,0)

class GUI(Frame):
    def __init__(self):
        super().__init__()
        self.style = Style()
        self.initGUI()
        self.run = True

    
    def initGUI(self):
        #adds additional frame
        self.master.title("auto OCR jp-en translator")
        self.frame = Frame(self,relief=RAISED,borderwidth=1)
        self.frame.pack(expand=True,fill=BOTH) 
        self.pack(fill=BOTH, expand=True)

        #buttons
        #self.show_area_button = Button(self.master, text="Show Area", command=self.show_area).pack(side=RIGHT)
        self.area_button = Button(self.master, text="Area", command=self.area).pack(side=RIGHT)
        self.translate_button = Button(self.master, text="Translate", command=self.translate).pack(side=RIGHT)
        self.auto_translate_button = Button(self.master, text="Auto",command= self.start_translate).pack(side=RIGHT)
        self.stop_translate_button = Button(self.master,text="Stop",command=self.stop_translate).pack(side=RIGHT)
        self.master.update_idletasks() #finishes wrapping the buttons and gui(still continues to add the Label right after) This is needed to update the winfo_width of the program
        self.text_var = StringVar() #creates an instance of strinvar which is used to dynamically change the text in translated_label
        self.translated_label = Label(self.frame, textvariable=self.text_var,font=(config.get('text', 'font_style'),config.get('text','font_size')), wraplength=self.master.winfo_width()).pack(fill=BOTH)

    def area(self):
        img = ImageGrab.grab() #basically screenshots the entire screen
        img.save('Assets/screenshot.png')
        instance = MouseEvents(img)
        instance.initialize()

    def show_area(self):
        coordinates = MouseEvents.click.start_point + MouseEvents.click.end_point
        print(coordinates)
        
    #one time translation, gonna tweak later to screenshot then translate
    def translate(self):
        self.area() #screenshots then makesa the user choose the area
        coordinates = MouseEvents.click.start_point + MouseEvents.click.end_point
        translated = functions.image_reader(coordinates)
        self.text_var.set(translated)

    def start_translate(self):
        self.run=True
        self.auto_translate()
        
    #calls the function in functions.py and translatordeepl.py
    def auto_translate(self):
        coordinates = MouseEvents.click.start_point + MouseEvents.click.end_point
        #run thread
        self.queue = queue.Queue()
        ThreadedTask(coordinates,self.queue).start()
        self.master.after(100, self.process_queue)
    
    def process_queue(self):
        try:
            translated = self.queue.get_nowait()
            if translated == None:
                pass
            else:
                self.text_var.set(translated)
            #repeats auto_translate_initiator every x seconds
            if self.run == True:
                self.master.after(config.getint('translator','time_wait_to_check_for_screen_update')*1000, self.auto_translate)
        except queue.Empty:
            self.master.after(100, self.process_queue)
    
    def stop_translate(self):
        self.run=False

class ThreadedTask(threading.Thread):
    def __init__(self, coordinates, queue):
        super().__init__()
        self.queue = queue
        self.coordinates = coordinates

    def run(self):
        translated = functions.auto_image_reader(self.coordinates)
        self.queue.put(translated)


class MouseEvents:
    def __init__(self,img):
        img = cv2.imread("Assets/screenshot.png", 1)
        self.img = img

    def click(self, event,x,y,flags, params):
        global click1, point1, img
        if event == cv2.EVENT_LBUTTONDOWN:
            # if mousedown, store the x,y position of the mous
            click1 = True
            point1 = (x,y)
            MouseEvents.click.start_point = point1
        elif event == cv2.EVENT_MOUSEMOVE and click1:
            # when dragging pressed, draw rectangle in image
            img_copy = self.img.copy()
            cv2.rectangle(img_copy, point1, (x,y), (245, 245, 66),1)
            cv2.imshow("Image", img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            # on mouseUp
            click1 = False
            cv2.destroyAllWindows()
            MouseEvents.click.end_point = (x,y)
    
    def initialize(self):
        cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback("Image", self.click)
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)


def main():
    root = Tk()
    root.iconbitmap("Assets/mashiro.ico")
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family=config.get('text','font_style'))
    root.attributes('-topmost',True, '-alpha',config.getfloat('main','window_transparency'))
    root.geometry(f"{config.get('main','window_size')}+300+300")
    my_gui = GUI()
    root.mainloop()



if __name__ == "__main__":
    main()