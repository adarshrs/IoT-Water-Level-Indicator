from tkinter import *
import socket
from threading import Thread
import time

class waterLevel:

    def __init__(self):

        try:
            self.address = socket.gethostbyname("raspberrypi")
        except:
            self.address = "Unknown"

        self.port = 12345

        self.level = "No Connection"



    def connect(self):
        if self.address == "Uknown":
            try:
                self.address = socket.gethostbyname("raspberrypi")
            except:
                self.level = "No Connection"
                return

        try:
            self.sock = socket.socket()
            self.sock.settimeout(2)
            self.sock.connect((self.address, self.port))
            self.sock.settimeout(None)

        except:# No internet
            print("Connection Error")
            self.level = "No Connection"
            self.sock.close
            return

        self.getWaterLevel()

    def getWaterLevel(self):
        self.level = self.sock.recv(4)

    def exitSensor(self):
        self.sock.close

    def returnWaterLevel(self):
        print(self.level)
        return self.level
