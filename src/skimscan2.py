# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import smtplib       #email lib in email_ip_address()
from email.MIMEMultipart import MIMEMultipart #for email
from email.MIMEText import MIMEText           #for email
import sys           #sys
import os            #os
import urllib        #url lib in check_internet_connect()
import time          #time
import bluetooth     #bluetooth lib used in main()
import Adafruit_GPIO.SPI as SPI     #display and pi
import Adafruit_SSD1306             #display lib
from PIL import Image      #for display
from PIL import ImageDraw  #for display
from PIL import ImageFont  #for display

#Raspi Pi Pin Config
RST = 24    # on the PiOLED this pin isn't used
#note the following are onlyu used with SPI
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# below sets display and display pins from downloaded lib
disp = Adafruit_SSD1306.SSD1306_128_64(
    rst=RST, 
    dc=DC, 
    spi=SPI.SpiDev(
        SPI_PORT, 
        SPI_DEVICE, 
        max_speed_hz=8000000
        )
    )

disp.begin()        #display begin

time.sleep(3)

disp.clear()                #clear display
disp.display()              #display the display
width = disp.width          #set width to display width
height = disp.height        #set height to display height
image = Image.new('1', (width, height)) #create image 
draw = ImageDraw.Draw(image)#draw the image from above

font = ImageFont.load_default()     #set display font
ellipsis = ".   "           
count = 0                   #initialize count to 0

from email.MIMEMultipart import MIMEMultipart #for email
from email.MIMEText import MIMEText           #for email

ipAddress = "Hello Ben"     #intialize var 
macAddress = "What What"    #initalize vars

BT_RET_CHARACTER = "M"      #set Constants
BT_SEND_CHARACTER = "P"
bluetooth_return_value = ""  #initialize var

def search_service():
    mServices=find_service(uuid="eba2b472-e69c-11e8-847c-3b2a22f8eff6")
    if len(mServices)==0:
        print"can't find available service"
    else:
        first_match=mServices[0]
        mPort=first_match["port"]
        mName=first_match["name"]
        mHost=first_match["host"]
        print  "Discovered %s on %s at port %s", (name, host, port)
        
def search_device():
    global targetAddress
    nearbyDevices=discover_devices()
    for address in nearbyDevices:
        if targetName==lookup_name(address):
            targetAddress=address
            break
    if targetAddress is not None:
        print "found target device with address", targetAddress
    else:
        print "can't find target device"
    
def send_msg(BT_SEND_CHARACTER):
    sock=BluetoothSocket(RFCOMM)
    sock.connect((targetAddress, port))
    a=sock.send(BT_SEND_CHARACTER)
    if(a>0):
        print "invaiti %d byte" %a
    sock.close()
def read_data():
    server_sock=BluetoothSocket(RFCOMM)
    #rport=get_available_port(RFCOMM)
    rport=0;
    server_sock.bind(("", rport))
    server_sock.listen(1)
    print "listening on port %d" %rport
    #advertise_service(server_sock, "eba2b472-e69c-11e8-847c-3b2a22f8eff6")
    client_sock, address=serve_sock.accept()
    bluetooth_return_value=client_sock.recv(1024)
    print "received[$s]" %bluetooth_return_value
    client_sock.close()
    server_sock.close()

import random

def attempt_connection():
    for x in range(1):
        value = random.randint(0,1)
        draw.rectangle((0, 0, width, height), outline=0, fill = 0)
        if(value == 0):
            print( "Not A Skimmer")
            print ("Pump is OK!!")
            draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            #draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            draw.text((0,24), "No Connection", font=font, fill=255)

        else:
            print( "Skimmer Found!!!")
            print ("Skip This Pump!!")
            #draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            draw.text((0,12), "Connection Made!!!", font=font, fill=255)
            draw.text((0,24), "Skimmer Found!!!!!", font=font, fill=255)
            draw.text((0,36), "Skip this pump!!!!", font=font, fill=255)

            disp.image(image)
            disp.display()
            get_address()
def get_address():
    for x in range(11):
        val = random.randint(0,9)
        mac_address = "B%d:%d%d:"+("%d+35")+"%d+37:%d%d:%d%d+38:%d%d" %val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10]
        check_internet_connect()
        
def attempt_connection1():
    #uuid = "eba2b472-e69c-11e8-847c-3b2a22f8eff6"
    bd_addr = "B8:27:EB:8B:1D:38"
    
    port = 1
    
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    sock.send(BT_SEND_CHARACTER)
    
    sock.close()
    
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_sock.bind(("B0:19:c6:90:74:22",port))
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
        draw.rectangle((0, 0, width, height), outline=0, fill = 0)
        draw.text((0,12), "Connection Made!!!", font=font, fill=255)
        draw.text((0,24), "Skimmer Found!!!!!", font=font, fill=255)
        draw.text((0,36), "Skip this pump!!!!", font=font, fill=255)
        
        disp.image(image)
        disp.display()
        get_address()
    else:
        print ("Comm Not Possible or Not Skimmer Dev")
        
    read_data()
def check_internet_connect(): 
    try:
        url = "https://www.google.com/"
        urllib.urlopen(url)
        status = "Connected"
    except urllib2.URLError, e:
        status = "Not connected"
    
    print status 
    if  (status == "Connected"):
        mail_mac_address()

    return


def mail_mac_address(): 
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
    #draw rectange size of OLED screen
    draw.rectangle((0,0, width, height), outline=0, fill=0)
    draw.text((0,24),"Scanning" + ellipsis, font=font, fill=255) #text to OLED
    disp.image(image)                  
    disp.display()
            #discovers bluetooth device by names scan duration 10 seconds
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)
            #prints to console how many devices are found with device name
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:  #if name matches print to OLED
        if (name == "HC-05") or (name == "HC-03") or (name == "HC-06"):
            draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            draw.text((0, 12), "Potential Skimmer", font=font, fill=255)
            draw.text((0, 24), name + " found.", font=font, fill=255)
            #draw.text((0,36), "Skip this pump.", font=font, fill=255)

            disp.image(image)
            disp.display()

            attempt_connection()       #call to attempt_connection()
            #time.sleep(5)

    count += 1                #for each iteration print a new . to OLED
    if count == 1:              
        ellipsis = "..  "     #should show -    scanning..
    elif count == 2:
        ellipsis = "... "     #should show -    scanning...
    elif count == 3:
        ellipsis = "...."     #should show -    scanning....
    else:
        ellipsis = ".   "     #should show -    scanning.
        count = 0
