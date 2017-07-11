'''Code fragment to deal with file mangement'''
import os

#standard file read
file = open("LargeTestFile1.tmp", "br")
file.read()
file.seek(0, 0) #seek to start of stream
temp = file.read(512)
while len(temp) != 0:
    temp = file.read(512)
file.close()

#get file stats
print(os.path.getsize("LargeTestFile1.tmp"))
print(os.path.isfile("LargeTestFile1.tmp"))
print(os.path.isfile("ecc"))
print(os.path.isdir("LargeTestFile1.tmp"))
print(os.path.isfile("ecc"))
print(os.path.islink("LargeTestFile1.tmp"))
print(os.path.ismount("LargeTestFile1.tmp"))

#check path exists
print(os.path.exists("LargeTestFile1.tmp"))
print(os.path.exists("ecc"))
print(os.path.exists("dsfsdfsfsfsdfsdfsfdff"))

#list files in directory
print(os.listdir('.'))

def walk(path='.'):
    """Takes a path, and recursivly transverses file tree, returns list of filepaths (files only)(empty directories not listed)"""
    output = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):
            output.append(os.path.join(path, i))
        if os.path.isdir(os.path.join(path, i)):
            temp = walk(os.path.join(path, i)) #recursive call
            for j in temp:
                output.append(os.path.join(j))
    return output

temp = walk()
for i in temp:
    print(i)
