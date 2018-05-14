import socket
import time
import json
import os
import Cryptodome
from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import DSS

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
    
    key = ECC.generate(curve='P-256')
    publicKey = key.public_key().export_key(format='DER', compress=True).hex()
    print("publicKey :" + str(key.public_key().export_key(format='DER', compress=True)))
    protocallVersion = "0000"
    
    version = 'v0.0'
    clientName = "DummyClient"
    message = publicKey + ":" + protocallVersion + ":" + "bisclient" + ":" + clientName + ":" + version + ":"
    message = message.ljust(192, ' ')
    
    h1 = SHA256.new(message.ljust(256, " ").encode('utf-8'))
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h1)
    handshake = message.encode('utf-8') + signature
    
    print("Sending data: " + str(handshake.hex()))
    socket1.send(handshake)

    data = socket1.recv(256)
    print("\tRecived data: " + str(data.hex()))    
    
    #all communication should be encrypted beyond this point    
    
    data = socket1.recv(4096).decode('utf-8')
    print("\tRecived data: " + str(data))        
    
    socket1.close()
    
print("Running TCP dummy Client")
for i in range(64):
    DummyClient()
    time.sleep(0)
