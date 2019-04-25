from tkinter import *
import socket
from threading import Thread
import time

class waterLevel:

    def __init__(self):

        self.address = "192.168.0.26"
        self.port = 12345
        self.connect()
        self.waterLevelReciever = Thread(name = 'waterLOevelReciever', target = self.getWaterLevel)
        self.exit = 0
        self.level = "0"
        self.waterLevelReciever.start()


    def connect(self):
        try:
            for i in range(1,3):
                try:
                    self.sock = socket.socket()
                    self.sock.settimeout(2)
                    self.sock.connect((self.address, self.port))
                    self.sock.settimeout(None)
                    self.recieverError = 0
                except:
                    print("Could not connect")
                    self.senderError = 1
                    self.recieverError = 1
                    self.sock.close
                    continue

                try:
                    self.sock.recv(1024)
                    self.senderError = 0
                    self.recieverError = 0
                except:
                    print("Could not recieve.")
                    self.sock.close
                    self.senderError = 1
                    continue


                if self.senderError == 0 and self.recieverError == 0:
                    self.level = "connected"
                    return

            self.senderError = 1

        except:
            self.recieverError = 1
            self.senderError = 1

    def getWaterLevel(self):
        while self.exit == 0:
            if self.level is not "disconnected":
                try:
                    self.level = self.sock.recv(4)
                    print("Hi")
                except:
                    self.level = "disconnected"
                    print("Unable to connect and recieve")
                    time.sleep(1)
                    continue

                if self.level == b'':
                    self.sock.close
                    self.senderError = 1
                    self.level = "disconnected"
                    time.sleep(2)
                    self.connect()
                    continue

                else:
                    self.level = self.level.decode("utf-8")

            else:
                self.connect()

    def exitSignal(self):
        self.exit = 1
        self.sock.close

    def returnWaterLevel(self):
        print(self.level)
        return self.level
