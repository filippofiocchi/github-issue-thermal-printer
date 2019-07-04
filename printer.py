import qrcode
import serial
import adafruit_thermal_printer
import subprocess
import time
from PIL import Image, ImageDraw
from bitlyshortener import Shortener
from urllib.request import urlopen
import re
from github import Github
import github
import sqlite3
from bs4 import BeautifulSoup
import os

g = Github(os.environ['TOKEN_GITHUB'])
tokens_pool = [os.environ['TOKEN_BITLY']]
connection = sqlite3.connect(os.environ['DATABASE_NAME'])
cursor = connection.cursor()
number_character = 29

class Printer():
    def __init__(self,url):
         ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
         uart = serial.Serial("/dev/ttyS0", baudrate=19200, timeout=3000)
         self._printer = ThermalPrinter(uart)
         self._printer.warm_up()
         shortener = Shortener(tokens=tokens_pool, max_cache_size=8192)
         urls=[url]
         self._urlshort = shortener.shorten_urls(urls)
         self._url = url
         self._last = self._url.rfind('/')
         self._n_issue = self._url[self._last+1:len(self._url)]
         qrcode_image = qrcode.make(self._urlshort[0])
         mode = 'RGB' 
         size = (200, 200)
         color = (255, 255, 255)
         new_image = Image.new(mode, size, color)
         resize_qrcode_image = qrcode_image.resize((75,75), Image.ANTIALIAS)
         new_image.paste(resize_qrcode_image, (int(200/2-100/2), int(200/2-100/2)))
         self._qrcode_logo = '/home/pi/qrcode.png'
         new_image.save(self._qrcode_logo)
         self.url = url
         self._html = urlopen(self._url)
         self._soup = BeautifulSoup(self._html,'lxml')
         self._title = self._soup.find('span', class_="js-issue-title").text
         self._repository = self._soup.find('strong', itemprop="name").text
         self._title2 = str((self._title).strip())
         self._out = [(self._title2[i:i+number_character]) for i in range(0, len(self._title2), number_character)]

    def print_receipt(self):
         self._printer.size = adafruit_thermal_printer.SIZE_LARGE
         self._printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER 
         self._printer.feed(1)
         self._printer.print((self._repository).strip())        
         self._printer.feed(1)
         self._printer.size = adafruit_thermal_printer.SIZE_MEDIUM
         self._printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
         for i in range(len(self._out)):
              self._printer.print(self._out[i])
              time.sleep(2)
         self._printer.feed(1)
         self._printer.size = adafruit_thermal_printer.SIZE_MEDIUM
         self._printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER         
         self._printer.print(' #'+self._n_issue )
         self._printer.feed(1)
         subprocess.run(['lp','-d','name of your thermal printer', '-o', 'fit-to-page',self._qrcode_logo ])
         self._printer.feed(1)
         time.sleep(7)

def get_url(url1) :
     cursor.execute("SELECT * FROM database1 WHERE urls=?",(url1,))
     result=(cursor.fetchall())
     print(url1)
     if str(result) != '[]' :
         print('already print')
     else :
         print('to print')
         printer = Printer(url1)
         printer.print_receipt()
         cursor.execute(" INSERT INTO database1 VALUES (?)",(url1,))
     connection.commit()   

for repo in g.get_user().get_repos():
     reponame = ''
     matches = ''
     all_url = []
     reponame = str(repo.name)
     repo = g.get_user().get_repo(reponame)
     url = repo.issues_url
     url_base = url[0:8]+url[12:22]+url[28:-9]
     pattern = re.compile(r'[a-zA-Z=,\" (]*(?P<number>[0-9]+)[)]+')
     for  r in repo.get_issues():
         p = str(r)
         match = str(pattern.findall(p))
         all_url.append([url_base+'/'+match[2:-2]])
     i = 0
     while i < len(all_url) :
         urli = (str(all_url[i]))
         url = urli[2:-2]
         get_url(url)
         i+=1
connection.close()        