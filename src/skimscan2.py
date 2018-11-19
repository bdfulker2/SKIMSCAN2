# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
#from gattlib import*
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
#from bluetooth.ble import DiscoveryService

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

def attempt_connection(macAddress):
    for x in range(1):    #select one random number
        value = random.randint(0,3) #limit the range of the int to be 0 and 3
        
        if(value == 0):             #if value of random.randint is 0
            print( "Not A Skimmer")     #print to console not a skimmer
            print ("Pump is OK!!")      #print to console not a skimmer
            draw.rectangle((0, 0, width, height), outline=0, fill = 0)#set OLED
            #draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            draw.text((0,24), "No Connection", font=font, fill=255)#text-4-OLED
            time.sleep(5)       #sleep so text stays on OLED
            return
        else:                       #if number is 1,2, or 3
            print( "Skimmer Found!!!")      #print to console
            print ("Skip This Pump!!")      #print to console
            draw.rectangle((0, 0, width, height), outline=0, fill = 0)#set OLED
                #print text to OLED 12=line 1, 24 = line 2, 36 line 3 of OLED
            draw.text((0,12), "Connection Made!!!", font=font, fill=255)
            draw.text((0,24), "Skimmer Found!!!!!", font=font, fill=255)
            draw.text((0,36), "Skip this pump!!!!", font=font, fill=255)

            disp.image(image)
            disp.display()          #display to OLED
            time.sleep(5)           #sleep so text stays on screen for 5 secs   
            save_address(macAddress)
 
def save_address(macAddress):
    import datetime                 #import date and time
    now = datetime.datetime.now()   #assign datetime.now to now
    file_name = "SkimmerDeviceAddresses"    #file name
    file = open(file_name, "a")             #open file and append
    write("MAC = " + macAddress + "-" + now.month+"/"+now.day+"/"+now.year +
                "-" + now.hour+":"+now.min)         #write sting to file
    file.close()                    #close file
    check_internet_connect(macAddress)
    
#def get_address():  #randomized get_address() to used to simulate BT_MAC
#    for x in range(1):    #get 1 val randomized between 0 and 9
#        v = random.randint(0,9)  
#                            #set semi random bluetooth MAC address
#        macAddress = ("B"+str(v)+":"+ str(v)+str(v)+":I"+str(v)+
#                            ":S"+str(v)+":"+str(v)+"3:U"+str(v))
#        print "macAddress is " + macAddress  #print to console for testing
#        check_internet_connect(macAddress)  #call check_internet_connect 
 
#def get_address2():
#    service = DiscoveryService()    #set servie to Discovery serve

 #   devices = service.discover(2)   #discover upto 2 devices store in devices

#    for address, name in devices.items():   
#        print("name: {}, address: {}".format(name, address)) #print format
#        if (name == "HC-05") or (name == "HC-03") or (name == "HC-06"):
#            macAddress = address        #set address to macAddress
#            print "in get_address2() the macAddress = " + macAddress #output
#           
#            check_internet_connect(macAddress) #call to check_internet_connect
#        else:                   #if device name doesnt match
#            print "Address not recovered"      #print address not recovered
            
#    return                                     #return to scanning
    
def attempt_connection1(macAddress):
    #uuid = "eba2b472-e69c-11e8-847c-3b2a22f8eff6"
    bd_addr = "B8:27:EB:8B:1D:38"
    
    port = 1
    
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))
    sock.send(BT_SEND_CHARACTER)
    
    sock.close()
    
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_sock.bind((macAddress,port))
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
        time.sleep(5)
        get_address()
    else:
        print ("Comm Not Possible or Not Skimmer Dev")
        
    read_data()
    
def check_internet_connect(macAddress):   #method to check internet connection
    try:
        url = "https://www.google.com/"     #using google.com as url to test
        urllib.urlopen(url)                 #uses urllib to open a url
        status = "Connected"                #assign status = connected
    except urllib2.URLError, e:             #exception URLError
        status = "Not connected"            #if url error status = not connected
    
    print status                            #print status to console
    if  (status == "Connected"):            #if status is still connected
        mail_mac_address(macAddress)        #call to mail_mac_address
                                            #with parameter of macAddress
    return


def mail_mac_address(macAddress): 
    
    server = smtplib.SMTP('smtp.gmail.com',587) #set server google smtp port=587
                                    
    server.ehlo()                               #Connect to Server
    server.starttls()
    
    
    server.login('skimscanfgcu', 'Skimscan1!')  #Login to Server with my cr
                                                
    fromaddr = "skimscanfgcu@gmail.com"         #set message Header
    toaddr = "skimscanfgcu@gmail.com"           #set message Header
    msg = MIMEMultipart()                       #set message Header multipart
    msg['From'] = fromaddr                      #set message Header from addr
    msg['To'] = toaddr                          #set message Header to address
    msg['Subject'] = "Todays RaspberryPI CSS Device MAC address" #set Subject

    body = "MAC = " + macAddress           #attach body of email to MIME message
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()                      #convert object msg to a string

    server.sendmail(fromaddr, toaddr, text)     #send email message
    print(body)                                 #print body to console


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
            #addr captures bluetooth device MAC address
    for addr, name in nearby_devices:  #if name matches print to OLED
        if (name == "HC-05") or (name == "HC-03") or (name == "HC-06"):
            draw.rectangle((0, 0, width, height), outline=0, fill = 0)
            draw.text((0, 12), "Potential Skimmer", font=font, fill=255)
            draw.text((0, 24), name + " found.", font=font, fill=255)
            draw.text((0,36), addr, font=font, fill=255)
            
            macAddress = addr               #assign Bluetooth addr to macAddress
            print ("Main: macAddress = " + macAddress)         #print to console
            
            disp.image(image)
            disp.display()

            attempt_connection(macAddress)       #call to attempt_connection()
            #time.sleep(5)                       #with macAddress as parameter
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
