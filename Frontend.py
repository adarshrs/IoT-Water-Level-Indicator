from tkinter import *
from PIL import Image
from PIL import ImageTk
import fonts
import Waterlevel
import time
import sys
from datetime import datetime
from threading import Thread


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
        return (self.fontname,str(int(fontsize)))

class mainScreen:
    def __init__(self):
        #try:
        self.setParams()
        self.loadFonts()
        self.loadImages()

        self.openWindow()

        self.startWaterLevelSensor()

        self.displayHub()

        self.gui.mainloop()

        #except:
        #    self.gui.destroy()
        #    sys.exit()

    #Called at initialization
    def setParams(self):
        self.gui = Tk()

        self.windowx = self.gui.winfo_screenwidth()
        self.windowy = self.gui.winfo_screenheight()

        self.windowSize = str(self.windowx) + "x" + str(self.windowy) + "+0+0"

        self.u = 20*self.windowx/self.windowy

    #Called at initialization
    def openWindow(self):
        self.gui.geometry(self.windowSize)

        self.gui.attributes("-fullscreen", True)
        self.gui.configure(background = "white")

    #Called at initialization
    def loadFonts(self):
        self.titlefont = font("Fonts/big_noodle_titling.ttf","BigNoodleTitling")

    #Called at initialization
    def loadImages(self):
        self.tank0 = imageClass("0")
        self.tank25 = imageClass("25")
        self.tank50 = imageClass("50")
        self.tank75 = imageClass("75")
        self.tank100 = imageClass("100")
        self.noConnection = imageClass("disconnected")
        self.connecting = imageClass("Connecting")

        self.IndicatorIcon = imageClass("IndicatorLogo")

        self.backButton = imageClass("BackButton")
        self.closeButton = imageClass("Close")

    #Called at initialization
    def startWaterLevelSensor(self):
        self.waterSensor = Waterlevel.waterLevel()

    #Called by indicator button... Calls startIndicator
    def displayIndicator(self,event):
        self.tankFrame = Frame(self.gui,height = self.windowy, width = self.windowx, bg = "white")
        self.tankFrame.place(x = 0, y = 0)

        imageSize = (self.u*20,self.u*20)

        self.noConnection.loadImage(imageSize)
        self.tank0.loadImage(imageSize)
        self.tank25.loadImage(imageSize)
        self.tank50.loadImage(imageSize)
        self.tank75.loadImage(imageSize)
        self.tank100.loadImage(imageSize)

        self.backButton.loadImage((self.u,self.u))

        back = Button(self.tankFrame, image = self.backButton.photoImage, bd = 0, highlightthickness=0, relief = FLAT)
        back.place(x = self.u,y = self.u)

        back.bind("<Button-1>",self.stopIndicator)

        self.startIndicator()

    #Called by displayIndicator... Calls displayTankCondition
    def startIndicator(self):
        self.waterSensor.connect()
        time.sleep(1)
        self.exitIndicator = 0

        while self.exitIndicator == 0:
            self.level = self.waterSensor.returnWaterLevel()
            self.displayTankCondition()
            time.sleep(5)

        self.waterSensor.exitSensor()

    #Called by indicator back button
    def stopIndicator(self,event):
        self.exitIndicator = 1
        self.hub.lift()

    #Called by startIndicator
    def displayTankCondition(self):

        tankCondition = self.noConnection.photoImage

        tankIndicator = Label(self.tankFrame,borderwidth = 0)
        tankIndicator.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        level = self.level

        if level == b'0':
            tankCondition = self.tank0.photoImage

        elif level == b'25':
            tankCondition = self.tank25.photoImage

        elif level == b'50':
            tankCondition = self.tank50.photoImage

        elif level == b'75':
            tankCondition = self.tank75.photoImage

        else:
            tankCondition = self.noConnection.photoImage

        tankIndicator.configure(image = tankCondition)
        self.gui.update()

    #Called at initialization
    def displayHub(self):
        self.hub = Frame(self.gui,height = self.windowy, width = self.windowx, bg = "white")
        self.hub.place(x = 0, y = 0)
        self.appsFrame = Frame(self.hub,height = self.windowy,width = self.windowx/2,bg = "white")
        self.appsFrame.place(x = 0, y = 0)
        self.timeFrame = Frame(self.hub,height = self.windowy,width = self.windowx/2,bg = "white")
        self.timeFrame.place(x = self.windowx/2 , y = 0)

        self.displayApps()

        self.displayTime()

    #Called by displayHub
    def displayApps(self):
        iconSize = (self.u*10,self.u*10)

        self.IndicatorIcon.loadImage(iconSize)

        indicator = Button(self.appsFrame,image = self.IndicatorIcon.photoImage, bd = 0, highlightthickness=0)
        indicator.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        indicator.bind("<Button-1>",self.displayIndicator)

    def displayTime(self):
        self.closeButton.loadImage((self.u,self.u))
        close = Button(self.timeFrame,image = self.closeButton.photoImage, highlightthickness=0,borderwidth = 0)
        close.place(x = (self.windowx/2)-1.5*self.u, y = 0.5*self.u)

        close.bind("<Button-1>", self.close)

        self.dayStringVar = StringVar()
        self.dateStringVar = StringVar()
        self.timeStringVar = StringVar()

        self.day = Label(self.timeFrame,textvariable = self.dayStringVar, bg = "white", fg = "#197C6D", font = self.titlefont.fontParams(self.u*2))
        self.date = Label(self.timeFrame,textvariable = self.dateStringVar, bg = "white", fg = "#B53939", font = self.titlefont.fontParams(self.u*4))
        self.time = Label(self.timeFrame,textvariable = self.timeStringVar, bg = "white", fg = "#4F4F4F", font = self.titlefont.fontParams(self.u*2))

        self.day.place(relx = 0.5, rely = 0.25, anchor = CENTER)
        self.date.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        self.time.place(relx = 0.5, rely = 0.75, anchor = CENTER)

        self.times = Thread(name = 'Time', target = self.getTime)
        self.times.start()

    #Independant thread started by displayTime
    def getTime(self):
        try:
            while True:
                self.time = datetime.now()
                self.dayString = self.time.strftime("Today  is  %A")
                self.dateString = self.time.strftime("%d %b")
                self.timeString = self.time.strftime("%I:%M %p")
                self.dayStringVar.set(self.dayString)
                self.dateStringVar.set(self.dateString)
                self.timeStringVar.set(self.timeString)
                self.gui.update()
                time.sleep(5)
        except:
            x = 0

    def close(self,event):
        try:
            self.gui.destroy()
            sys.exit()
        except:
            x = 0

App = mainScreen()
