'''Creates the test files/directories used for testing
Note: emphisis is on readability, not performance here
'''
import os

#Single file, small file size, even, simple name
print("Creating: Single file, small file size, even, simple name")
f1 = open("0001.tmp", "bw")
for i in range(0, 4*1024):
    f1.write(bytes([i % 256]))
f1.close()

#Single file, small file size, odd, simple name
print("Creating: Single file, small file size, odd, simple name")
f1 = open("0002.tmp", "bw")
for i in range(0, 4*1024 + 10):
    f1.write(bytes([i % 256]))
f1.close()

#Single file, medium file size, even, simple name
print("Creating: Single file, medium file size, even, simple name")
f1 = open("0003.tmp", "bw")
for i in range(0, 512*1024):
    f1.write(bytes([i % 256]))
f1.close()

#Single file, medium file size, even, simple name
print("Creating: Single file, medium file size, even, simple name")
f1 = open("0004.tmp", "bw")
for i in range(0, 64*1024*1024):
    f1.write(bytes([i % 256]))
f1.close()

#Multiple files, medium file size, even, simple name
print("Creating: Multiple files, medium file size, even, simple name")
if not os.path.exists("tmp1"):
    os.makedirs("tmp1")
f1 = open("tmp1/0001.tmp", "bw")
for i in range(0, 64*1024*1024):
    f1.write(bytes([i % 256]))
f1.close()
f1 = open("tmp1/0002.tmp", "bw")
for i in range(0, 64*1024*1024):
    f1.write(bytes([i % 256]))
f1.close()

#Multiple files, various file size, odd, simple name
print("Creating: Multiple files, various file size, odd, simple name")
if not os.path.exists("tmp2"):
    os.makedirs("tmp2")
for i in range(0, 4):
    f1 = open("tmp2/" + str(i).zfill(4) + ".tmp", "bw")
    for j in range(0, 64*1024*1024):
        f1.write(bytes([j % 256]))
    f1.close()
for i in range(0, 16):
    f1 = open("tmp2/" + str(i + 4).zfill(4) + ".tmp", "bw")
    for j in range(0, 64*1024):
        f1.write(bytes([j % 256]))
    f1.close()
for i in range(0, 64):
    f1 = open("tmp2/" + str(i + 4 + 16).zfill(4) + ".tmp", "bw")
    for j in range(0, 1024):
        f1.write(bytes([j % 256]))
    f1.close()
    
#Multiple files, various file size, odd, simple name
print("Creating: Multiple files, small file size, odd, simple name")
root = "tmp3/"
if not os.path.exists(root):
    os.makedirs(root)
for i in range(0, 1024):
    f1 = open(root + str(i).zfill(4) + ".tmp", "bw")
    for j in range(0, 16*1024):
        f1.write(bytes([j % 256]))
    f1.close()

#Multiple files, various file size, odd, simple name
print("Creating: Multiple files, small file size, odd, simple name")
root = "tmp4/"
if not os.path.exists(root):
    os.makedirs(root)
for i in range(0, 1024):
    f1 = open(root + str(i).zfill(4) + ".tmp", "bw")
    for j in range(0, 21*1024):
        f1.write(bytes([j % 256]))
    f1.close()
    
    f1 = open(root + str(i).zfill(4) + "b.tmp", "bw")
    for j in range(0, 1024 + 10):
        f1.write(bytes([j % 256]))
    f1.close()
