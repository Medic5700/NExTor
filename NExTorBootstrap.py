"""
A Bootstrap server for the NExTor network
"""

import socket
import time
import json
import os
import Cryptodome
import random
from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import DSS

ProtocalVersion = "0000"
ProgramName = "Python3 Bootstrap Server"
ProgramVersion = "v0.0"

#get/generate config file
if not (os.path.exists("config.json")):
    options = {
        'hostIP':"127.0.0.1",
        'hostPort':5555,
        'privateKeyHex':("".ljust(138*2, "0"))
        }
    file = open("config.json",'w')
    file.write(json.dumps(options, sort_keys=True, indent=1))
    file.close()
    
file = open("config.json",'r')
options = json.loads(file.read())
file.close()

#load Globals
HostIP = options["hostIP"]
HostPort = options["hostPort"]
PrivateKey = ECC.import_key(bytes(bytearray.fromhex(options["privateKeyHex"])))
Nodes = {}

del(options)

PublicKeyHex = ((PrivateKey.public_key().export_key(format='DER', compress=True)).hex()).ljust(128, "0") #TODO this is shortcut, have actual machinery to swap out encryption implimentations
message = PublicKeyHex + ":" + str(ProtocalVersion) + ":" + "bootstrap" + ":" + str(ProgramName) + ":" + str(ProgramVersion) + ":"
message = message.ljust(192, ' ')
h1 = SHA256.new(message.encode(encoding='utf-8'))
signer = DSS.new(PrivateKey, 'fips-186-3')
signature = signer.sign(h1)
Handshake = message.encode(encoding='utf-8') + signature

print(Handshake)
print(len(Handshake))
print(Handshake.hex())

print(PublicKeyHex)

#start listening
socket1 = socket.socket()
socket1.bind((HostIP, HostPort))
socket1.settimeout(1)

socket1.listen(512)
print("server Listening")

while (True):
    try: #this loop with socket1.accept() allows use ctrl-c program interupt to work
        clientConnection, clientAddress = socket1.accept()
    except:
        time.sleep(0.01)
        continue
    
    clientHandshake = clientConnection.recv(256) #will wait until new data is received
    print("clienthandshake : " + clientHandshake.hex())
    
    if not clientHandshake:
        continue #if the connection terminates, no data is received, and breaks from the loop
     
    print("Debug: address: " + str(clientAddress))
    
    message = str(clientHandshake[0:192].decode("utf-8"))
    print("Debug: message: " + str(message))
    signature = clientHandshake[192:]
    print("signiture : " + signature.hex())
    
    raw = message.split(":")
    clientPublicKey = raw[0]
    version = raw[1]
    clientFunction = raw[2]
    clientName = raw[3]
    clientVersion = raw[4]

    if ProtocalVersion != version:
        print("Client Protocal Version Fail")
        continue
    
    #verify if handshake is signed properly, else continue
    test = bytes(bytearray.fromhex(clientPublicKey))
    print("key : " + test.hex())
    received_key = ECC.import_key(test)
    print("BinMessage : " + message.ljust(256, " ").encode('utf-8').hex())
    h2 = SHA256.new(message.ljust(256, " ").encode('utf-8'))
    verifier = DSS.new(received_key, 'fips-186-3')
    print("signiture : " + signature.hex())
    try:
        verifier.verify(h2, signature)
    except ValueError:
        print("Client Signature Fail")
        continue
    
    clientConnection.send(Handshake)
    
    #all communication should be encrypted beyond this point

    try:
        #need to figure out way to properly handle IPv6
        clientAddressHex = socket.inet_pton(socket.AF_INET, clientAddress[0]).hex() + hex(clientAddress[1])[2:].rjust(4, "0")
        # clientAddressHex = socket.inet_pton(socket.AF_INET6, clientAddress[0]).hex() + hex(clientAddress[1])[2:].rjust(18, "0")
    except:
        print("adress translation fail")
        continue

    Nodes[clientPublicKey] = (clientAddressHex, int(time.time()))
    #TODO make routine to clean out old addresses
    
    bootstrapList = {"Client":clientAddressHex, "Peers":[] }
    for i in range(32): #can fit about... 100-ish IPv6 addresses in 4KB
        keys = sorted(Nodes.keys())
        random.randint(0, len(keys) - 1)
        bootstrapList["Peers"].append(Nodes[keys[random.randint(0, len(keys) - 1)]][0])
    temp = json.dumps(bootstrapList, sort_keys=True).ljust(4096, " ")
    
    clientConnection.send(temp.encode("utf-8"))
    clientConnection.shutdown(socket.SHUT_RDWR) #close doesn't 'close' the connection immediatly
    clientConnection.close()


