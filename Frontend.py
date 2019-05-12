from PIL import Image as imlib
from tkinter import *
from PIL import ImageTk
import fonts
import Waterlevel
import time
import sys
from datetime import datetime
from threading import Thread
import winsound

class imageClass:
    def __init__(self,filename):
        self.filename = "Images/" + filename + "-01.png"
        self.image = imlib.open(self.filename)

    def resize(self,Isize):
        h = int(Isize[0])
        w = int(Isize[1])
        return self.image.resize((h,w),imlib.ANTIALIAS)

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
        self.c = 0
        self.setParams()
        self.loadFonts()
        self.loadImages()

        self.openWindow()

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

        self.timeRefreshRate = 60
        self.indicatorRefreshRate = 300

    #Called at initialization
    def openWindow(self):
        self.gui.geometry(self.windowSize)

        self.gui.attributes("-fullscreen", True)
        self.gui.configure(background = "#E5D9B5")

    #Called at initialization
    def loadFonts(self):
        self.titlefont = font("Fonts/big_noodle_titling.ttf","BigNoodleTitling")
        self.labelfont = font("Fonts/timesi.ttf","Times New Roman Italic")

    #Called at initialization
    def loadImages(self):
        self.tank0 = imageClass("0")
        self.tank25 = imageClass("25")
        self.tank50 = imageClass("50")
        self.tank75 = imageClass("75")
        self.tank100 = imageClass("100")
        self.noConnection = imageClass("disconnected")
        self.connecting = imageClass("Connecting")

        self.closeButton = imageClass("Close")

        self.bottomBar = imageClass("bar")

        self.refresh = imageClass("refresh")
        self.blank = imageClass("blank")

        self.notfilling = imageClass("notfilling")
        self.filling = imageClass("filling")
        self.filled = imageClass("filled")

    #Called by displayHub
    def startWaterLevelSensor(self):
        self.connecting.loadImage((self.u*12,self.u*12))
        loading = Label(self.tankFrame,image = self.connecting.photoImage, bd = 0)
        loading.place(relx = 0.5, rely = 0.15, anchor = N)
        self.waterSensor = Waterlevel.waterLevel()

    #Called by displayHub... Calls startIndicator
    def displayIndicator(self):
        imageSize = (self.u*12,self.u*12)
        self.noConnection.loadImage(imageSize)
        self.tank0.loadImage(imageSize)
        self.tank25.loadImage(imageSize)
        self.tank50.loadImage(imageSize)
        self.tank75.loadImage(imageSize)
        self.tank100.loadImage(imageSize)

        self.blank.loadImage((self.u*12,self.u*14))

        while True:
            self.refreshIndicator(5)
            for i in range(1,self.indicatorRefreshRate+1):
                time.sleep(1)

    #Called by displayIndicator... Calls displayTankCondition
    def refreshIndicator(self,event):
        self.refTime = datetime.now()
        self.refreshed.set(" Last updated 0 min ago.")
        time.sleep(1)

        self.level = self.waterSensor.checkLevel()
        self.displayTankCondition()

    #Called by refreshIndicator
    def displayTankCondition(self):

        blank = Label(self.tankFrame,borderwidth = 0, image = self.blank.photoImage)
        blank.place(relx = 0.5, rely = 0.08, anchor = N)

        tankCondition = self.noConnection.photoImage

        tankIndicator = Label(self.tankFrame,borderwidth = 0)
        tankIndicator.place(relx = 0.5, rely = 0.08, anchor = N)

        l = StringVar()
        levelLabel = Label(self.tankFrame,borderwidth = 0, textvariable = l, font = self.titlefont.fontParams(self.u*1.2), bg = "#E5D9B5")
        levelLabel.place(relx = 0.5,rely = 0.64, anchor = N)
        fg = ""

        level = self.level

        if level == "0":
            tankCondition = self.tank0.photoImage
            l.set("0 %")
            fg = "#B53939"

        elif level == "25":
            tankCondition = self.tank25.photoImage
            l.set("25 %")
            fg = "#944754"

        elif level == "50":
            tankCondition = self.tank50.photoImage
            l.set("50 %")
            fg = "#74566F"

        elif level == "75":
            tankCondition = self.tank75.photoImage
            l.set("75 %")
            fg = "#54658A"

        elif level == "100":
            tankCondition = self.tank100.photoImage
            l.set("100 %")
            fg = "#3474A5"

        else:
            tankCondition = self.noConnection.photoImage
            l.set("Press refresh to retry")
            fg = "#B3B3B3"

        tankIndicator.configure(image = tankCondition)
        levelLabel.configure(fg = fg)
        self.gui.update()

    #Called at initialization
    def displayHub(self):
        self.hub = Frame(self.gui,height = self.windowy, width = self.windowx, bg = "#E5D9B5")
        self.hub.place(x = 0, y = 0)

        self.timeFrame = Frame(self.hub,height = self.windowy,width = self.windowx/2,bg = "#E5D9B5")
        self.timeFrame.place(x = self.windowx/2 , y = 0)

        self.tankFrame = Frame(self.hub, height = self.windowy, width = self.windowx/2, bg = "#E5D9B5")
        self.tankFrame.place(x = 0, y = 0)

        self.bottomBar.loadImage((self.windowx+2*self.u,self.u*0.6))
        bottomBar = Label(self.hub, image = self.bottomBar.photoImage)
        bottomBar.place(x = -self.u, y = self.windowy+self.u*0.1,anchor = SW)

        self.displayRefreshStatus()

        self.displayFillButton()

        self.displayTime()

        self.startWaterLevelSensor()

        self.ind = Thread(name = 'Indicator', target = self.displayIndicator)
        self.ind.start()

    #Called by displayHub
    def displayFillButton(self):
        buttonSize = (self.u*5,(250/938)*self.u*5)
        self.notfilling.loadImage(buttonSize)
        self.filling.loadImage(buttonSize)
        self.filled.loadImage(buttonSize)

        self.fillButtonFrame = Frame(self.tankFrame, bg = "#E5D9B5", height = buttonSize[1], width = buttonSize[0])
        self.fillButtonFrame.place(relx = 0.5, rely = 0.9, anchor = S)



        self.fillingButtonFrame = Frame(self.fillButtonFrame, bg = "#E5D9B5",height = buttonSize[1], width = buttonSize[0])
        self.fillingButtonFrame.place(x = 0, y = 0)

        self.filledButtonFrame = Frame(self.fillButtonFrame, bg = "#E5D9B5",height = buttonSize[1], width = buttonSize[0])
        self.filledButtonFrame.place(x = 0, y = 0)

        self.notfillingButtonFrame = Frame(self.fillButtonFrame, bg = "#E5D9B5",height = buttonSize[1], width = buttonSize[0])
        self.notfillingButtonFrame.place(x = 0, y = 0)




        self.notfillingButton = Button(self.notfillingButtonFrame, image = self.notfilling.photoImage, borderwidth = 0, highlightthickness = 0)
        self.notfillingButton.pack()
        self.notfillingButton.bind("<Button-1>",self.fillingFunc)

        self.fillingButton = Button(self.fillingButtonFrame, image = self.filling.photoImage, borderwidth = 0, highlightthickness = 0)
        self.fillingButton.pack()
        self.fillingButton.bind("<Button-1>",self.stopfillingFunc)

        self.filledButton = Button(self.filledButtonFrame, image = self.filled.photoImage, borderwidth = 0, highlightthickness = 0)
        self.filledButton.pack()
        self.filledButton.bind("<Button-1>",self.filledFunc)

        self.stopFillingFlag = 0

    #Called by displayHub
    def displayRefreshStatus(self):
        self.refresh.loadImage((self.u*0.5,self.u*0.5))

        self.refreshFrame = Frame(self.tankFrame, height = 2*self.u, width = 10*self.u, bg = "#E5D9B5")
        self.refreshFrame.place(relx = 0.5, rely = 0.75, anchor = N)

        refreshButton = Button(self.refreshFrame,image = self.refresh.photoImage, borderwidth = 0, highlightthickness = 0)
        refreshButton.pack(side = LEFT)

        refreshButton.bind('<Button-1>',self.refreshIndicator)


        self.refreshed = StringVar()
        refreshLabel = Label(self.refreshFrame,textvariable = self.refreshed, fg = "#5D5D5D", bg = "#E5D9B5", font = self.labelfont.fontParams(self.u*0.4))
        refreshLabel.pack(side = LEFT)

        self.refTime = datetime.now()

    #Called by displayHub
    def displayTime(self):
        self.closeButton.loadImage((self.u*0.7,self.u*0.7))
        close = Button(self.timeFrame,image = self.closeButton.photoImage, highlightthickness=0,borderwidth = 0)
        close.place(x = (self.windowx/2)-1.5*self.u, y = 0.5*self.u)

        close.bind("<Button-1>", self.close)

        self.dayStringVar = StringVar()
        self.dateStringVar = StringVar()
        self.timeStringVar = StringVar()

        self.day = Label(self.timeFrame,textvariable = self.dayStringVar, bg = "#E5D9B5", fg = "#197C6D", font = self.titlefont.fontParams(self.u*2.2))
        self.date = Label(self.timeFrame,textvariable = self.dateStringVar, bg = "#E5D9B5", fg = "#B53939", font = self.titlefont.fontParams(self.u*3.7))
        self.time = Label(self.timeFrame,textvariable = self.timeStringVar, bg = "#E5D9B5", fg = "#4F4F4F", font = self.titlefont.fontParams(self.u*1.5))

        self.day.place(relx = 0.95, rely = 0.64, anchor = E)
        self.date.place(relx = 0.95, rely = 0.82, anchor = E)
        self.time.place(relx = 0.95, rely = 0.52, anchor = E)

        #self.day.place(relx = 0.1, rely = 0.25, anchor = W)
        #self.date.place(relx = 0.1, rely = 0.5, anchor = W)
        #self.time.place(relx = 0.1, rely = 0.75, anchor = W)


        self.times = Thread(name = 'Time', target = self.getTime)
        self.times.start()

    #Independant thread started by displayTime
    def getTime(self):
        #try:
        while True:
            self.time = datetime.now()
            #self.dayString = self.time.strftime("Today  is  %A")
            self.dayString = self.time.strftime("%A")
            self.dateString = self.time.strftime("%d %b")
            self.timeString = self.time.strftime("%I:%M %p")

            self.dayStringVar.set(self.dayString)
            self.dateStringVar.set(self.dateString)
            self.timeStringVar.set(self.timeString)

            refStr = " Last updated "
            if self.time.minute>55:
                refStr = refStr + str(60 - self.time.minute + self.refTime.minute) + " min ago."

            else:
                refStr = refStr + str(self.time.minute - self.refTime.minute) + " min ago."


            self.refreshed.set(refStr)

            self.gui.update()
            for i in range(1,self.timeRefreshRate+1):
                time.sleep(1)
        #except:
        #    x = 0

    #Called by Close button
    def close(self,event):
        try:
            self.gui.destroy()
            sys.exit()
        except:
            x = 0

    #Called by notFilling button
    def fillingFunc(self,event):
        self.indicatorRefreshRate = 30
        self.fillingButtonFrame.lift()
        self.gui.update()

        self.stopFillingFlag = 0

        self.fill = Thread(name = 'Fill', target = self.filler)
        self.fill.start()

    #Called by fillingFunc
    def filler(self):
        while self.level != b'100':
            if self.stopFillingFlag == 1:
                return

        self.filledButtonFrame.lift()

        self.confirmFilled = 0

        self.beeper = Thread(name = 'Beep', target = self.beep)
        self.beeper.start()

    #Called by filler
    def beep(self):
        while self.confirmFilled == 0:
            winsound.Beep(500,500)
            winsound.Beep(500,500)
            winsound.Beep(500,500)
            time.sleep(2)

    #Called by filling button
    def stopfillingFunc(self,event):
        self.stopFillingFlag = 1
        self.notfillingButtonFrame.lift()
        self.indicatorRefreshRate = 300

    #Called by filled button
    def filledFunc(self,event):
        self.confirmFilled = 1
        self.notfillingButtonFrame.lift()

    def close(self,event):
        exit()



App = mainScreen()
