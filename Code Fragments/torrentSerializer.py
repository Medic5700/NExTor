import os
import math

#test setup
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

torrentRoot = "./"
if not os.path.exists(torrentRoot):
    print("filepath does not exist")
    exit()
fileList = None
if os.path.isfile(torrentRoot):
    fileList = [torrentRoot]
elif os.path.isdir(torrentRoot):
    fileList = walk(torrentRoot)
    

def hashFile(path):
    """Takes a file path, returns a byte array (64 bytes) representing the sha3_512 hash of the file"""
    import hashlib
    blockSize = 64*1024*1024
    
    h = hashlib.sha3_512()
    f1 = open(filepath, 'br')
    #parses data 1MB at a time, to avoid loading the entirety of a file into memory
    data = f1.read(blockSize)
    while len(data) == blockSize:
        h.update(data)
        data = f1.read(blockSize)
    f1.close()
    if len(data) > 0:
        h.update(data)
    return h.digest()

class TorFile:
    import os
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileSize = os.path.getsize(filePath)
        self.start = None
        self.end = None
        self.fileHash = None
        self.ID = None
        
    def __repr__(self):
        return "(" + self.filePath + ", " + str(self.fileSize) + ", " + str(self.start) + ", " + str(self.end) + ")"

def pieceSizeCalc(torrentSize):
    """Takes a (int)size, returns a (int) peicessize"""
    '''Every time the torrentSize x4, the piece size x2'''
    # min block size 256*1024
    import math
    pieceSize = 2**(18 + math.floor(max(math.log2(torrentSize) - 26, 0) // 2))
    return pieceSize

def fileOrganizer(pathList):
    #sort files by size
    temp = []
    for i in pathList:
        temp.append(TorFile(i))
    
    #sortedFileList = sorted(temp, key=lambda TorFile: TorFile.fileSize, reverse=True)
    sortedFileList = sorted(temp, key=lambda TorFile: TorFile.fileSize)
    
    torrentSize = 0
    for i in sortedFileList:
        torrentSize += i.fileSize
        
    #just a test
    pieceSize = pieceSizeCalc(torrentSize)
    for i in sortedFileList:
        i.pieces = math.ceil(i.fileSize/pieceSize)
        i.sizeInTorrent = pieceSize * i.pieces
    
    #just a test
    torrentFullSize = 0
    for i in sortedFileList:
        torrentFullSize += i.sizeInTorrent
    print("TorrentSize = " + str(torrentSize))
    print("FullTorrentSize = " + str(torrentFullSize))
    
    '''
    for i in sortedFileList:
        i.ratio = i.fileSize / (math.ceil(i.fileSize/pieceSize) * pieceSize)
        print(i.ratio, i.fileSize, i.filePath)
    '''
    #sort the files
    # http://www.wolframalpha.com/input/?i=Plot%5Bx%2F(ceil(x%2F(256*1024))*1024*256),+%7Bx,+0,2*1024*1024%7D%5D
    largeFiles = []
    mediumFiles = []
    smallFiles = []
    for i in sortedFileList:
        if i.fileSize > 4 * pieceSize:
            largeFiles.append(i)
        elif i.fileSize < pieceSize // 16:
            smallFiles.append(i)
        else:
            mediumFiles.append(i)

    largeFiles = sorted(largeFiles, key=lambda TorFile: TorFile.fileSize)
    mediumFiles = sorted(mediumFiles, key=lambda TorFile: TorFile.fileSize)
    smallFiles = sorted(smallFiles, key=lambda TorFile: TorFile.fileSize)
    
    print(largeFiles)
    print(mediumFiles)
    print(smallFiles)
    
    startList = {}
    endList = {}

    bookmark1 = 0 #used for showing next free byte
    piecemark = 0 #used for showing next free chunk
    
    # files are aligned to blocks (IE: files do not share blocks with other files)
    while len(largeFiles) != 0:
        print("\t", "large", "estimated end", largeFiles[-1].fileSize - 1 + bookmark1, "bookmark", bookmark1, "piecemark", piecemark)
        temp = largeFiles.pop()
        startList[bookmark1] = temp
        temp.start = bookmark1
        temp.end = bookmark1 + temp.fileSize - 1
        endList[bookmark1 + temp.fileSize - 1] = temp
        piecemark = math.ceil((bookmark1 + temp.fileSize)/pieceSize) * pieceSize
        bookmark1 = piecemark
        
    # files are partially aligned to blocks, but any leftover space is filled with other files
    while len(mediumFiles) != 0:
        stuffing = True
        limiter = bookmark1 + math.ceil(mediumFiles[-1].fileSize/pieceSize) * pieceSize
        print("Bookmark", bookmark1, "limiter", limiter)
        
        while len(mediumFiles) != 0:
            print("\t", "medium-medium", "estimated end", mediumFiles[-1].fileSize - 1 + bookmark1, "limiter", limiter, "bookmark", bookmark1, "piecemark", piecemark)
            if mediumFiles[-1].fileSize - 1 + bookmark1 > limiter:
                print("\t\t", "breaking 1")
                #stuffing = False
                break
            temp = mediumFiles.pop()
            startList[bookmark1] = temp
            temp.start = bookmark1
            temp.end = bookmark1 + temp.fileSize - 1  
            endList[bookmark1 + temp.fileSize - 1] = temp
            piecemark = math.ceil((bookmark1 + temp.fileSize - 1)/pieceSize) * pieceSize
            bookmark1 = bookmark1 + temp.fileSize
        
        while (len(smallFiles) != 0): #and (stuffing == True):
            print("\t", "medium-small", "estimated end", smallFiles[-1].fileSize - 1 + bookmark1, "limiter", limiter, "bookmark", bookmark1, "piecemark", piecemark)
            if smallFiles[-1].fileSize -1 + bookmark1 > limiter:
                print("\t\t", "breaking 1")
                #stuffing = False
                break            
            temp = smallFiles.pop()
            startList[bookmark1] = temp
            temp.start = bookmark1
            temp.end = bookmark1 + temp.fileSize - 1  
            endList[bookmark1 + temp.fileSize - 1] = temp
            piecemark = math.ceil((bookmark1 + temp.fileSize - 1)/pieceSize) * pieceSize
            bookmark1 = bookmark1 + temp.fileSize
        
        bookmark1 = piecemark
        
    while (len(smallFiles) != 0):
        print("\t", "small", "estimated end", smallFiles[-1].fileSize - 1 + bookmark1, "bookmark", bookmark1, "piecemark", piecemark)
        temp = smallFiles.pop()
        startList[bookmark1] = temp
        temp.start = bookmark1
        temp.end = bookmark1 + temp.fileSize - 1  
        endList[bookmark1 + temp.fileSize - 1] = temp
        piecemark = math.ceil((bookmark1 + temp.fileSize - 1)/pieceSize) * pieceSize
        bookmark1 = bookmark1 + temp.fileSize    
    
    '''
    print("startList")
    for i in sorted(startList.keys()):
        print(i, startList[i])
    print("endList")
    for i in sorted(endList.keys()):
        print(i, endList[i])
    '''
    for i in sorted(startList.keys()):
        print(startList[i])
        start = startList[i].start
        while start < startList[i].end:
            print("\t", start/pieceSize)
            start += pieceSize
        
    return startList
    
temp = fileOrganizer(fileList)
