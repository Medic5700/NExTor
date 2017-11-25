'''a bootstrap server, returns a short list of nodes that are alive'''

import socket
import time
import random

def BootstrapServer():
    """
    """
    nodes = {}
    
    host = "127.0.0.1" #loopback adress
    port = 5555
    publicKey = hex(random.randint(0, 256**64 - 1))[2:]
    socket1 = socket.socket()
    socket1.bind((host, port))
    socket1.settimeout(1)
    
    socket1.listen(512)
    
    print("server Listening")
    
    while (True):
        try:
            connection, address = socket1.accept()
        except:
            time.sleep(1)
            continue
        
        peerHandshake = connection.recv(256).decode("utf-8") #will wait until new data is received
        
        if not peerHandshake:
            continue #if the connection terminates, no data is received, and breaks from the loop
         
        print("Debug: Recived: " + str(peerHandshake))
        print("Debug: address: " + str(address))
        
        processed = peerHandshake.split(":")
        clientPublicKey = processed[0]
        version = processed[1]
        clientName = processed[2]
        
        handshake = publicKey + ":" + "v0.0" + ":" + "bootstrap" + ":"
        handshake = handshake.ljust(256, '_')
        
        connection.send(handshake.encode("utf-8"))
        
        '''the next step would be to wait to receve a handshake encrypted and signed by the peer, to verify connection,
        then this would respond with their original handshake encrypted and signed by server, to verify connection to them
        '''
        connection.recv(256).decode("utf-8")
        connection.send(handshake.encode("utf-8"))
        #assume connection and peer are verified at this point
        #all communication should be encrypted beyond this point
        
        nodes[clientPublicKey] = (clientPublicKey, version, clientName, str(address), int(time.time()))
        
        bootstrapIP = ""
        for i in range(64):
            keys = sorted(nodes.keys())
            random.randint(0, len(keys) - 1)
            bootstrapIP += nodes[keys[random.randint(0, len(keys) - 1)]][3] + ":"
        bootstrapIP = "BootstrapIP:" + bootstrapIP
        bootstrapIP = bootstrapIP.ljust(2048, "_")
        
        connection.send(bootstrapIP.encode("utf-8"))
        
        connection.shutdown(socket.SHUT_RDWR) #close doesn't 'close' the connection immediatly
        connection.close()
    
def DummyClient():
    """Starts a TCP client
    Connects to server
    Pings some data off of the server
    """
    host = "127.0.0.1" #loopback adress
    port = 5555
    
    socket1 = socket.socket()
    socket1.settimeout(1)
    socket1.connect((host, port))
    
    publicKey = hex(random.randint(0, 256**64 - 1))[2:]
    publicKey = publicKey.upper().rjust(128, "0")
    version = 'v0.0'
    clientName = "DummyClient"
    handshake = publicKey + ":" + version + ":" + clientName + ":"
    handshake = handshake.ljust(256, '_')
    
    print("Sending data: " + str(handshake))
    socket1.send(handshake.encode('utf-8'))
    
    data = socket1.recv(256).decode('utf-8')
    print("\tRecived data: " + str(data))    
    
    '''the next step would be to wait to receve a handshake encrypted and signed by the peer, to verify connection,
    then this would respond with their original handshake encrypted and signed by server, to verify connection to them
    '''
    socket1.send(handshake.encode("utf-8"))
    socket1.recv(256).decode("utf-8")
    #assume connection and peer are verified at this point
    #all communication should be encrypted beyond this point    
    
    data = socket1.recv(2048).decode('utf-8')
    print("\tRecived data: " + str(data))        
    
    socket1.close()
    
ClientServer = input("Is it a server? (T/F):").lower()

if ClientServer == 'f':
    print("Running TCP dummy Client")
    for i in range(64):
        DummyClient()
        time.sleep(0)
else:
    print("Running TCP Server")
    BootstrapServer()
