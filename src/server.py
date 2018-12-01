#This class is used as a server and client for RFCOMM Bluetooth connection and
#string data transfer. The def server() method recieves data sent from our CSS
#device. Then it acts as the client and sends a return character to the CSS
#device

                                                            #import libraries
import bluetooth
import sys
import os
                                #set constants for send and recieve characters
BT_SEND_CHARACTER = "M"
BT_REC_CHARACTER = "P"

def server():
    
    try:                                   #set socket to RFCOMM
        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

        port = 1                            #set port to 1
        server_sock.bind(("",port))    #bind socket to port and string address
        server_sock.listen(1)           #set socket to listen(1)
                        #set client socket to same as server socket
        client_sock,address = server_sock.accept()      
        print "Accepted connection from CSS device ",address

        data = client_sock.recv(1024)       #received data from sender/client
        print "received [%s]" % data        #print received data
        
        client_sock.close()                 #close client socket
        server_sock.close()                 #close server socket
        if(data == BT_REC_CHARACTER):       #if sent data matches call client()
            client(address)

    except:                                 #error handling
        print "server bluetooth error"
        sys.stderr.write("server bluetooth error")
        sys.exit(1)
        return
            
def client(address):

#    bd_addr = address
    bd_addr = "B8:27:EB:8B:1D:38"

    port = 1                                #set port = 1
                                            #set socket to RFCOMM
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))    #connect socket to port and other device address

    sock.send(BT_SEND_CHARACTER)            #send return char to server method
                                            #on the CSS device
    sock.close()                            #close socket

#while(True):
#    server()
server()