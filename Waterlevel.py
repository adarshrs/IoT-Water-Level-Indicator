from tkinter import *
import socket
from threading import Thread
import time

class waterLevel:

    def __init__(self):

        self.address = socket.gethostbyname("raspberrypi")
        self.port = 12345

        self.level = "No Connection"

    def connect(self):
        try:
            self.sock = socket.socket()
            self.sock.settimeout(2)
            self.sock.connect((self.address, self.port))
            self.sock.settimeout(None)

        except:# No internet
            self.level = "No Connection"
            self.sock.close
            return

        self.waterLevelReciever = Thread(name = 'waterLevelReciever', target = self.getWaterLevel)
        self.exit = 0
        self.waterLevelReciever.start()

    def getWaterLevel(self):
        while self.exit == 0:
            self.level = self.sock.recv(4)

    def exitSensor(self):
        self.exit == 1
        self.sock.close
        self.level = "Disconnected"

    def returnWaterLevel(self):
        print(self.level)
        return self.level
