'''Code fragment to hash a file'''
#https://docs.python.org/3/library/hashlib.html#module-hashlib

import hashlib

filename = "LargeTestFile1.tmp"
f1 = open(filename,"br")

h = hashlib.sha3_512()

print("current file possition = " + str(f1.tell()))

temp = f1.read(512)
while len(temp) == 512:
    temp = f1.read(512)
    h.update(temp)

print("current file possition = " + str(f1.tell()))
    
if len(temp) > 0: #handles unevenly size file endings
    temp = temp + bytes(512 - len(temp))
    h.update(temp)
    
print("file hash is = " + (h.digest()).hex())

def hashFile(filename):
    """Takes filename, returns 64-byte array represnting SHA3_512 hash of file"""
    h = hashlib.sha3_512()
    f1 = open(filename,"br")
    temp = f1.read(512)
    while len(temp) == 512:
        temp = f1.read(512)
        h.update(temp)
    f1.close()
    if len(temp) > 0: #handles unevenly size file endings
        temp = temp + bytes(512 - len(temp))
        h.update(temp)
    return h.digest()

print(hashFile("LargeTestFile1.tmp").hex())
print(hashFile("LargeTestFile2.tmp").hex())
print(hashFile("LargeTestFile2.tmp").hex())
print(hashFile("SmallTestFile1.tmp").hex())
print(hashFile("SmallTestFile2.tmp").hex())
