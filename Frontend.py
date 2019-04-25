from tkinter import *
from PIL import Image
from PIL import ImageTk
import fonts
import Waterlevel
import time
import sys

class imageClass:
    def __init__(self,filename):
        self.filename = "Images/" + filename + "-01.png"
        self.image = Image.open(self.filename)

    def resize(self,Isize):
        h = int(Isize[0])
        w = int(Isize[1])
        return self.image.resize((h,w),Image.ANTIALIAS)

    def loadImage(self,Isize):
        self.photoImage = ImageTk.PhotoImage(self.resize(Isize))

class font:
    def __init__(self,fontfile,fontname):
        fonts.loadfont(fontfile)
        self.fontname = fontname

    def fontParams(self,fontsize):
        return (fontname,str(fontsize))

class mainScreen:
    def __init__(self):
        try:
            self.setParams()

            self.loadFonts()
            self.loadImages()

            self.openWindow()

            self.displaySplashScreen()
            self.startWaterLevelSensor()

            self.displayTankCondition()

            self.tankCondition = Thread(name = 'TankIndicator', target = self.displayTankCondition)
            self.tankCondition.start()
        except:
            self.gui.destroy()
            sys.exit()
    def setParams(self):
        self.gui = Tk()

        self.windowx = self.gui.winfo_screenwidth()
        self.windowy = self.gui.winfo_screenheight()

        self.windowSize = str(self.windowx) + "x" + str(self.windowy) + "+0+0"

        self.u = 20*self.windowx/self.windowy

    def openWindow(self):
        self.gui.geometry(self.windowSize)

        self.gui.attributes("-fullscreen", True)
        self.gui.configure(background = "white")

    def loadFonts(self):
        self.titlefont = font("Fonts/big_noodle_titling.ttf","BigNoodleTitling")

    def loadImages(self):
        self.tank0 = imageClass("0")
        self.tank25 = imageClass("25")
        self.tank50 = imageClass("50")
        self.tank75 = imageClass("75")
        self.tank100 = imageClass("100")
        self.noConnection = imageClass("disconnected")

        self.connecting = imageClass("Connecting")

    def displaySplashScreen(self):
        splashFrame = Frame(self.gui, height = self.windowy, width = self.windowy, bg = "white")
        splashFrame.pack()

        self.connecting.loadImage((self.u*20,self.u*20))
        splashLogo = Label(splashFrame, image = self.connecting.photoImage, borderwidth = 0)
        splashLogo.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        self.gui.update()

    def startWaterLevelSensor(self):
        self.waterSensor = Waterlevel.waterLevel()

    def displayTankCondition(self):

        tankFrame = Frame(self.gui,height = self.windowy, width = self.windowx/2, bg = "white")
        tankFrame.place(x = 0, y = 0)

        imageSize = (self.u*20,self.u*20)

        self.noConnection.loadImage(imageSize)
        self.tank0.loadImage(imageSize)
        self.tank25.loadImage(imageSize)
        self.tank50.loadImage(imageSize)
        self.tank75.loadImage(imageSize)
        self.tank100.loadImage(imageSize)

        tankCondition = self.noConnection.photoImage

        tankIndicator = Label(tankFrame,borderwidth = 0)
        tankIndicator.place(relx = 0.5, rely = 0.5, anchor = CENTER)


        while True:
            level = self.waterSensor.returnWaterLevel()

            if level == "0":
                tankCondition = self.tank0.photoImage

            elif level == "25":
                tankCondition = self.tank25.photoImage

            elif level == "50":
                tankCondition = self.tank50.photoImage

            elif level == "75":
                tankCondition = self.tank75.photoImage

            else:
                tankCondition = self.noConnection.photoImage

            tankIndicator.configure(image = tankCondition)
            self.gui.update()

            time.sleep(2)

    def exitWaterLevelSensor(self):
        self.waterSensor.exitSignal()


App = mainScreen()
