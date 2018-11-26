# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


import bluetooth

def server():
    
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
        if(data == 'P'):
            client()

    except:
        print "server bluetooth error"
        return
            
def client():
    try:
        bd_addr = "B8:27:EB:8B:1D:38"

        port = 1

        sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((bd_addr, port))

        sock.send("M")

        sock.close()
    except:
        print "client bluetooth error"
        return
        
while(true):
    server()