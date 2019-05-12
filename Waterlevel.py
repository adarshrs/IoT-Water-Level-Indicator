import time
import urllib
import socket
import urllib.request
from bs4 import BeautifulSoup

class waterLevel:
    def __init__(self):
        self.address = socket.gethostbyname("raspberrypi")
        self.address = "http://" + self.address
        self.level = "No connection"

    def checkLevel(self):
        try:
            server = urllib.request.urlopen(self.address)
            code = server.read()
            code = code.decode("utf8")
            server.close()
            soup = BeautifulSoup(code, 'html.parser')
            self.level = soup.p.string[:soup.p.string.find("%")]
        except:
            self.level = "No connection"

        return self.level
