from tkinter import Tk,font, StringVar, RAISED, BOTH, RIGHT
from tkinter.ttk import Frame, Button, Style, Label
from functions import functions
import pyWinhook as pyHook
import win32gui
import cv2
from PIL import ImageGrab

#next task:
#ocr feature
#translate feature


click1 = False
point1 = (0,0)

class GUI(Frame):
    def __init__(self):
        super().__init__()
        self.style = Style()
        self.initGUI()
        self.run = False

    
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
        self.master.update_idletasks()
        self.text_var = StringVar()
        self.translated_label = Label(self.frame, textvariable=self.text_var,font=(24), wraplength=self.master.winfo_width()).pack(fill=BOTH)

    def area(self):
        img = ImageGrab.grab()
        img.save('Assets/screenshot.png')
        instance = MouseEvents(img)
        instance.initialize()

    def show_area(self):
        coordinates = MouseEvents.click.start_point + MouseEvents.click.end_point
        print(coordinates)
        
    
    def translate(self):
        coordinates = MouseEvents.click.start_point + MouseEvents.click.end_point
        translated = functions.image_reader(coordinates)
        self.text_var.set(translated)

    def auto_translate(self):
        coordinates = MouseEvents.click.start_point + MouseEvents.click.end_point
        translated = functions.auto_image_reader(coordinates)
        if translated == None:
            pass
        else:
            self.text_var.set(translated)
        #repeats the code program every 2 seconds
        if self.run == True:
            self.master.after(2000, self.auto_translate)
    
    def start_translate(self):
        self.run=True
        self.auto_translate()

    def stop_translate(self):
        self.run=False




        
        

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
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Arial")
    root.attributes('-topmost',True, '-alpha',0.6)
    root.geometry("400x200+300+300")
    my_gui = GUI()
    root.mainloop()



if __name__ == "__main__":
    main()