#Author: Ben Fulker
#Last Edited: 11/30/2018
#This software is an adaptation from Tyler Winegarner raspi_skimcan.py 
#Retrived from github on 9/30/2018: 
#  https://github.com/photoresistor/raspi_skimscan/blob/master/raspi_skimscan.py
#desc: scans for local bluetooth devices with names matching the description 
#   of those used in cas pump credit card skimmers. When a potential skimmer 
#   with the specified HC-03, HC-05, or HC-06 is found the Bluetooth MAC address
#   is captured. Then the software attempts to connect to potential skimmer 
#   devices using the Bluetooth RFCOMM protocol. If a connection is made the 
#   character "P" is sent to the potential skimmer. If the potential skimmer 
#   returns the character "M" then it is likely a skimmer. The MAC address is 
#   then stored on the devices local text file database. The software then
#   check if the device is currently connected to its home Wi-Fi network and if
#   it is connected it will email the captured MAC address to a specified
#   email address.
#       This software is directly derived from the research done by Nathan 
#       Seidle as documented in this article: 
#                       https://learn.sparkfun.com/tutorials/gas-pump-skimmers
# 


import smtplib       #email lib in email_ip_address()
from email.MIMEMultipart import MIMEMultipart #for email
from email.MIMEText import MIMEText           #for email
import sys           #sys
import os            #os
import random
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
#note the following are only used with SPI
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

macAddress = "What What"    #initalize vars

BT_RET_CHARACTER = "M"      #set Constants
BT_SEND_CHARACTER = "P"
bluetooth_return_value = ""  #initialize var



############################used for testing only###############################
#import random

#def attempt_connection(macAddress):
#    for x in range(1):    #select one random number
#        value = random.randint(0,3) #limit the range of the int to be 0 and 3
        
#        if(value == 0):             #if value of random.randint is 0
#            print( "Not A Skimmer")     #print to console not a skimmer
#           print ("Pump is OK!!")      #print to console not a skimmer
#            print_oled("", ("No Connection"), "", False)
#            return
#        else:                       #if number is 1,2, or 3
#            print( "Skimmer Found!!!")      #print to console
#            print ("Skip This Pump!!")      #print to console
            
#            print_oled("Connection Made!!!", ("Skimmer Found!!!!!"), 
#                                                   "Skip this pump!!!!", False) 
#            save_address(macAddress)   #call to save_address() macAddress param
################################################################################ 

######################### was used for testing##################################    
#def get_address():  #randomized get_address() to used to simulate BT_MAC
#    for x in range(1):    #get 1 val randomized between 0 and 9
#        v = random.randint(0,9)  
#                            #set semi random bluetooth MAC address
#        macAddress = ("B"+str(v)+":"+ str(v)+str(v)+":I"+str(v)+
#                            ":S"+str(v)+":"+str(v)+"3:U"+str(v))
#        print "macAddress is " + macAddress  #print to console for testing
#        check_internet_connect(macAddress)  #call check_internet_connect 
################################################################################ 

#The save_address method opens the SkimmerDeviceAddresses.txt file and appends
#to the file the found Devices MAC address along with the current time according 
#of the raspberry pi zero w
def save_address(macAddress):
    import datetime                 #import date and time
    now = datetime.datetime.now()   #assign datetime.now to now
    file_name = "SkimmerDeviceAddresses.txt"    #file name
    file = open(file_name, "a")             #open file and append
    file.write("\nMAC = " + macAddress + "-" + 
                str(now.month)+"/"+str(now.day)+"/"+str(now.year) +
                "-" + str(now.hour)+":"+str(now.minute))   #write sting to file
    file.close()                    #close file
    check_internet_connect(macAddress)

# This method attempts to connect to the the potential skimmer device and send
#the character "P" to it using bluetooth RFCOMM protocol
def attempt_connection1(macAddress):
    
    port = 1                                              #set port to 1  
                                                         
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )    #set socket to RFCOMM
    sock.connect(("", port))               #connect sock to port and MAC address
    sock.send(BT_SEND_CHARACTER)           # sends character to other device

    sock.close()                           #closes the socket
    
    server(macAddress)                     #call to server method

#server method recieves and data sent back over from other device over the 
#RFCOMM protocol if the character "M" is sent back it is most likely a skimmer
#device
def server(macAddress): 
    try:
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
            
            print_oled("Connection Made!!!", ("Skimmer Found!!!!!"), 
                                                    "Skip this pump!!!!", False)
            
            save_address(macAddress)
        else:
            print ("Comm Not Possible or Not Skimmer Dev")

        
    except:
        print "exception bluetooth sever error"
        sys.stderr.write("server bluetooth error")
        sys.exit(1)
        return
  
#The check_internet_connect method try's to check if there is Wi-Fi connection 
#to a specified URL to verify that it is connect to the internet 
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

#The mail_mac_address method connects to an smtp server with the users specified
#email user_name and password. It then sends an email to the that same account 
#with the found skimmer device Bluetooth MAC address using a multippart format. 
def mail_mac_address(macAddress): 
    
###############user to update with there email information######################
    user_name = 'skimscanfgcu'                        #email user name for login
    password = 'Skimscan1!'                           #email password for login
    email_address = "skimscanfgcu@gmail.com"          #full string email address
    smtp_server = 'smtp.gmail.com'                    #smtp server for google
    smtp_port = 587                                   #smtp port for google
################################################################################
    
    server = smtplib.SMTP(smtp_server,smtp_port)#set server google smtp port=587
                                    
    server.ehlo()                               #Connect to Server
    server.starttls()
    
    server.login(user_name, password)  #Login to Server with my cr
                                                
    fromaddr = email_address                    #set message Header
    toaddr = email_address                      #set message Header
    msg = MIMEMultipart()                       #set message Header multipart
    msg['From'] = fromaddr                      #set message Header from addr
    msg['To'] = toaddr                          #set message Header to address
    msg['Subject'] = "Todays RaspberryPI CSS Device MAC address" #set Subject

    body = "MAC = " + macAddress           #attach body of email to MIME message
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()                      #convert object msg to a string

    server.sendmail(fromaddr, toaddr, text)     #send email message
    print(body)                                 #print body to console

#The print_oled method takes three variables line_one, line_two, line_three, and
#no_sleep. Line one two and three are the three seperate lines used on the OLED
#The no_sleep variable is a boolean that allows it to sleep and keep output on 
#the display and to slow the system
def print_oled(line_one, line_two, line_three, no_sleep):
    draw.rectangle((0, 0, width, height), outline=0, fill = 0)
    draw.text((0, 12), line_one, font=font, fill=255)
    draw.text((0, 24), line_two, font=font, fill=255)
    draw.text((0,36), line_three, font=font, fill=255)
            
    disp.image(image)
    disp.display()
    if no_sleep == False:
        time.sleep(5)
    return

while (True):     
    #draw rectange size of OLED screen
    print_oled("", ("Scanning" + ellipsis), "", True)
            #discovers bluetooth device by names scan duration 10 seconds
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)
            #prints to console how many devices are found with device name
    print("found %d devices" % len(nearby_devices))
            #addr captures bluetooth device MAC address
    for addr, name in nearby_devices:  #if name matches print to OLED
        if (name == "HC-05") or (name == "HC-03") or (name == "HC-06"):
           
            print_oled("Potential Skimmer", (name + " found."), addr, False)
            
            macAddress = addr               #assign Bluetooth addr to macAddress
            #print ("Main: macAddress = " + macAddress)        #print to console
            attempt_connection1(macAddress)       #call to attempt_connection()
                                                 #with macAddress as parameter
        else:
            print_oled("", ("Device Not Found"), "", False)
            
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
