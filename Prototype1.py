'''This is just a prototype for handling the files?'''
import os

#Get basic data about file
filepath = "./TestThors/0004.tmp"
if not os.path.exists(filepath):
    print("filepath does not exist")
    exit()
if not os.path.isfile(filepath):
    print("filepath is not a file")
    exit()
filetype = "FILE"
filesize = os.path.getsize(filepath)

#Hash file
import hashlib

h = hashlib.sha3_512()
f1 = open(filepath, 'br')
temp = f1.read(512)
while len(temp) == 512:
    h.update(temp)
    temp = f1.read(512)
if len(temp) > 0:
    temp = temp + bytes(512 - len(temp))
    h.update(temp)
f1.close()
filehash = int.from_bytes(h.digest(), byteorder='big')
del(h)

#generate data-structure for metadata file
import math

def bytes_int(input):
    pass

pieceSize = 512*1024
files = {filepath:{"SIZE":filesize, "START":0, "END":filesize, "HASH": filehash}}
numberOfPieces = math.ceil(filesize/pieceSize)
pieceHashs = []
for i in range(0, numberOfPieces):
    h = hashlib.sha3_512()
    f1 = open(filepath, 'br')
    h.update(f1.read(pieceSize))
    pieceHashs.append(int.from_bytes(h.digest(), byteorder='big'))
    del(h)

#fill in all data for data structure
infoFile = {"FILES": files, "PIECESIZE": pieceSize, "NUMBEROFPIECES": numberOfPieces, "PIECEHASHS": pieceHashs}

#export to json
import json
jsonFile = json.dumps(infoFile, sort_keys=True, indent=1)
f1 = open(hex(filehash)[2:] + str(".json"), "w")
f1.write(jsonFile)
f1.close()

#reimport from json

#verify file against json metadata
