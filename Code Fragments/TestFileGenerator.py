temp = []
for i in range(0,256):
    temp.append(i)
pattern = bytes(temp)

f1 = open("LargeTestFile1.tmp","bw")
print("Creating LargeTestFile1.tmp")
for i in range(0,1*4*1024*64):
    f1.write(pattern)
f1.close()
print("Created LargeTestFile1.tmp")

f1 = open("LargeTestFile2.tmp","bw")
print("Creating LargeTestFile2.tmp")
for i in range(0,1*4*1024*64+1):
    f1.write(pattern)
f1.close()
print("Created LargeTestFile2.tmp")

f1 = open("SmallTestFile1.tmp","bw")
print("Creating SmallTestFile1.tmp")
for i in range(0,4):
    f1.write(pattern)
f1.close()
print("Created SmallTestFile1.tmp")

f1 = open("SmallTestFile2.tmp","bw")
print("Creating SmallTestFile2.tmp")
for i in range(0,1):
    f1.write(pattern)
f1.close()
print("Created SmallTestFile2.tmp")
