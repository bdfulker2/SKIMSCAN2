# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


import smtplib
import sys
import os
import urllib
import time
import bluetooth
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Raspi Pi Pin Config
RST = 24    # on the PiOLED this pin isn't used
#note the following are onlyu used with SPI
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
disp.begin

time.sleep(3)

disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()
ellipsis = ".   "
count = 0

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

ipAddress = "Hello Ben"
macAddress = "What What"

BT_RET_CHARACTER = 'M'
BT_SEND_CHARACTER = 'P'
bluetooth_return_value = 0

def attempt_connection(BT_RET_CHARACTER):
    #uuid = "eba2b472-e69c-11e8-847c-3b2a22f8eff6"
    bd_addr = "B8:27:EB:8B:1D:38"
    
    port = 1
    
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    sock.send(BT_SEND_CHARACTER)
    
    sock.close()
    
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print "Accepted connection from ",address

    data = client_sock.recv(1024)
    print "received [%s]" % data
    
    client_sock.close()
    server_sock.close()
    
    if(data == BT_RET_CHARACTER):
        print( "Skimmer Found!!!")
        print ("Skip This Pump!!")
        #get_address()
    else:
        print ("Comm Not Possible or Not Skimmer Dev")
        
    
def check_internet_connect(): 
    try:
        url = "https://www.google.com/"
        urllib.urlopen(url)
        status = "Connected"
    except urllib2.URLError, e:
        status = "Not connected"
    
    print status 
    if  (status == "Connected"):
        mail_ip_address()

    return


def mail_ip_address(): 
    #set server
    server = smtplib.SMTP('smtp.gmail.com',587)

    #Connect to Server
    server.ehlo()
    server.starttls()
    

    #Login to Server
    server.login('skimscanfgcu', 'Skimscan1!')

    #set message Header
    fromaddr = "skimscanfgcu@gmail.com"
    toaddr = "skimscanfgcu@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Todays RaspberryPI CSS Device IP address" 

    #attach body of email to MIME message
    body = "IP = " + ipAddress + "- MAC = " + macAddress
    msg.attach(MIMEText(body, 'plain'))

    #convert object to a string
    text = msg.as_string()

    #send email message
    server.sendmail(fromaddr, toaddr, text)
    print(body)


while (True):
    draw.rectangle((0,0, width, height), outline=0, fill=0)
    draw.text((0,24),"Scanning" + ellipsis, font=font, fill=255)
    disp.image(image)
    disp.display()
    
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)

    print("found %d devices" % len(nearby_devices))
    
    for addr, name in nearby_devices:
        if (name == "HC-05") or (name == "HC-03") or (name == "HC-06"):
            draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            draw.text((0, 12), "Potential Skimmer", font=font, fill=255)
            draw.text((0, 24), name + " found.", font=font, fill=255)
            draw.text((0,36), "Skip this pump.", font=font, fill=255)
            
            attempt_connection()
            
            disp.image(image)
            disp.display()
            time.sleep(5)
            
    count += 1
    if count == 1:
        ellipsis = "..  "
    elif count == 2:
        ellipsis = "... "
    elif count == 3:
        ellipsis = "...."
    else:
        ellipsis = ".   "
        count = 0
#check_internet_connect()
##mail_ip_address()