from tkinter import *
from PIL import Image
from PIL import ImageTk
import socket
import os
import time
import fonts
import datetime
from random import randint

class WaterLevel:

    def __init__(self):
        self.getQuote()
        self.tk = Tk()

        self.windowx = self.tk.winfo_screenwidth()
        self.windowy = self.tk.winfo_screenheight()

        string = str(self.windowx) + "x" + str(self.windowy) + "+0+0"
        self.tk.geometry(string)

        self.tk.attributes("-fullscreen", True)
        self.tk.configure(background = "white")

        Cframe = Frame(self.tk,height = self.windowy, width = self.windowx, bg = "white")
        Cframe.place(x = 0, y = 0,height = self.windowy, width = self.windowx)
        con = Image.open("Images/Connecting-01.png")
        h = int(self.windowx/2)
        connecting = con.resize((h,h),Image.ANTIALIAS)
        connecting = ImageTk.PhotoImage(connecting)
        splash = Label(Cframe, image = connecting, borderwidth=0)
        splash.place(x = self.windowx/2-h/2,y = self.windowy/2-h/2)
        self.tk.update()

        fonts.loadfont("Fonts\\big_noodle_titling.ttf")
        fonts.loadfont("Fonts\\timesi.ttf")

        self.s = socket.socket()
        port = 12345

        try:
            self.s.settimeout(2)
            self.s.connect(('192.168.0.26', port))
            self.s.settimeout(None)
            print("connecting")
            self.getWaterLevel()
        except:
            self.level = "disconnected"

        self.panelScreen()

    def panelScreen(self):
        try:
            Dframe = Frame(self.tk,height = self.windowy, width = self.windowx/2, bg = "white")
            Dframe.place(x = 0, y = 0,height = self.windowy, width = self.windowx)
            Indicator = Label(Dframe, borderwidth=0)

            self.timeFrame = Frame(self.tk, height = self.windowy, width = self.windowx/2, bg = "white")
            self.timeFrame.place(x = self.windowx/2, y = 0, height = self.windowy, width = self.windowx/2)

            self.todayL = Label(self.timeFrame, borderwidth = 0, justify = CENTER)
            self.dayL = Label(self.timeFrame, borderwidth = 0, justify = CENTER)
            self.dateL = Label(self.timeFrame, borderwidth = 0, justify = CENTER)
            self.timeL = Label(self.timeFrame, borderwidth = 0, justify = CENTER)

            self.todayL.place(relx = 0.2, rely = 0.2, anchor = CENTER)
            self.dayL.place(relx = 0.6, rely = 0.2,anchor = CENTER)
            self.dateL.place(relx = 0.4, rely = 0.45,anchor = CENTER)
            self.timeL.place(relx = 0.4, rely = 0.7,anchor = CENTER)


            self.displayQuote()

            while True:
                try:
                    self.getWaterLevel()
                except:
                    self.level = "disconnected"

                file = "Images/" + self.level + "-01.png"
                h = self.windowx/2
                indicator = self.displayPicture(file,(h,h))
                Indicator.configure(image = indicator)
                Indicator.place(x = self.windowx/4-h/2,y = self.windowy/2-h/2)

                self.displayTime()

                self.tk.update()

        finally:
            self.s.close

    def getWaterLevel(self):
        level = self.s.recv(1024)
        print(level)
        if level == b'':
            self.s.close
            self.level = "disconnected"
            return
        elif level == b'Thank you for connecting':
            self.level = "Connected"

        else:
            self.level = level.decode("utf-8")

    def displayPicture(self,filename,size):
        size = (int(size[0]),int(size[1]))
        img = Image.open(filename)
        image = img.resize(size,Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image

    def getTime(self):

        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

        now = datetime.datetime.now()
        ampm = ""

        if now.hour % 12 == 0:
            ampm = "AM"
        else:
            ampm = "PM"

        hour = now.hour
        minute = now.minute

        if hour<10:
            h = "0" + str(hour)
        else:
            h = str(hour%12)

        if minute<10:
            m = "0" + str(minute)
        else:
            m = str(minute)

        self.time = h + " : " + m + " " + ampm

        self.date = str(now.day) + " " + months[now.month-1]
        self.day = now.strftime("%A")

    def getQuote(self):
        f = open('Quotes/bbob.txt', 'r')
        lines = f.readlines()
        f.close()

        delim = "*\n"

        quote = list()
        i = -1

        for line in lines:
            if line == delim:
                quote.append("")
                i = i+1
                continue
            quote[i] = quote[i] + line + "\n"

        self.myquote = ""

        while True:
            self.myquote = quote[randint(0,len(quote))]
            if len(self.myquote)<100:
                break

    def displayQuote(self):
        quoteFrame = Frame(self.timeFrame, height = self.windowy*0.15, width = self.windowx*0.4, bg = "white")
        quoteFrame.place(x = self.windowx*0, y = self.windowy*0.75+self.windowy*0.1)
        quote = Label(quoteFrame,borderwidth = 0)
        quote.configure(text = self.myquote,bg = "white", fg = "#999999", font = ("Times New Roman Italic","13"), wraplength = 500, justify = CENTER)
        quote.place(relx = 0.5,rely = 0.5, anchor = CENTER)

    def displayTime(self):

        self.getTime()

        self.todayL.configure(text = "Today is ", bg = "white", fg = "#197C6D", font = ("BigNoodleTitling","75"))

        self.dayL.configure(text = self.day, bg = "white", fg = "#4F4F4F", font = ("BigNoodleTitling","75"))

        self.dateL.configure(text = self.date, bg = "white", fg = "#B53939", font = ("BigNoodleTitling","160"))

        self.timeL.configure(text = self.time, bg = "white", fg = "#4F4F4F", font = ("BigNoodleTitling","75"))

if __name__ == '__main__':
    w = WaterLevel()
