temp = []
for i in range(0,256):
    temp.append(i)
pattern = bytes(temp)

f1 = open("LargeTestFile.tmp","bw")
print("Creating large test file")
for i in range(0,1*4*1024*64):
    f1.write(pattern)
f1.close()
print("Created large test file")
