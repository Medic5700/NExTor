'''This is just a prototype for handling the files?'''

class Debug:
    """Class for logging and debuging"""
    
    def __init__(self, debugMode, file = "Debug.log"):
        self.__filename = file
        self.showDebug = debugMode #Bool
        
    def __save(self, text):
        """Saves text to file as a log entry"""
        logfile = open(self.__filename, 'a')
        try:
            logfile.write(text)
        except:
            self.err("Error Occured in Error Logging Function: Attempting to report previous error")
            for i in text:
                try:
                    logfile.write(i)
                except:
                    logfile.write("[ERROR]")
        logfile.close()

    def log(self, text):
        """Takes string, pushes to stdout AND saves it to the log file
        
        For general logging, and non-fatal errors
        """
        temp = "[" + time.asctime() + "] Log: " + text
        print(temp)
        self.__save(temp + "\n")
    
    def err(self, text):
        """Takes string, pushes to stdout and saves it to the log file
        
        Mainly meant for non-recoverable errors that should cause the program to terminate"""
        temp = "[" + time.asctime() + "] ERR: " + text
        print(temp)
        self.__save(temp + "\n")        
    
    def debug(self, *args):
        """takes n number of strings, pushes to stdout and log file
        
        only writes input to stdout/log file when self.showDebug is True (debugMode was set to true when initialized)"""
        if (self.showDebug):
            temp = "Debug:"
            for i in args:
                temp += "\t" + str(i) + "\n"
            print(temp, end="") #fixes issue where log and sceen output newlines don't match
            self.__save(temp)
stderr = Debug(True)

import os

#get data about multiple files in torrent
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

torrentRoot = "./TestThors/tmp1"
if not os.path.exists(torrentRoot):
    print("filepath does not exist")
    exit()
fileList = None
if os.path.isfile(torrentRoot):
    fileList = [torrentRoot]
elif os.path.isdir(torrentRoot):
    fileList = walk(torrentRoot)

torrentSize = 0
for i in fileList:
    torrentSize += os.path.getsize(i)
    
def pieceSizeCalc(torrentSize):
    """Takes a (int)size, returns a (int) peicessize"""
    '''Every time the torrentSize x4, the piece size x2'''
    # min block size 256*1024
    import math
    pieceSize = 2**(18 + math.floor(max(math.log2(torrentSize) - 26, 0) // 2))
    return pieceSize

torrentPieceSize = pieceSizeCalc(torrentSize)

#Hash file
def hashFile(filepath):
    """Takes a file path, returns a byte array (64 bytes) representing the sha3_512 hash of the file"""
    import hashlib
    h = hashlib.sha3_512()
    f1 = open(filepath, 'br')
    #parses data 64MB at a time, to avoid loading the entirety of a file into memory
    data = f1.read(64*1024*1024)
    while len(data) == 64*1024*1024:
        h.update(data)
        data = f1.read(64*1024*1024)
    f1.close()
    if len(data) > 0:
        h.update(data)
    return h.digest()

class TorFile:
    def __init__(self, filePath, fileSize):
        self.filePath = filePath
        self.fileSize = fileSize
        self.start = None
        self.fileHash = None
        self.ID = None
        
    def __repr__(self):
        return "(" + self.filePath + ", " + str(self.fileSize) + ", " + str(self.start) + ")"

def fileOrganizer(pathList):
    import os
    import math
    #sort files by size
    fileList = []
    for i in pathList:
        if os.path.getsize(i) == 0:
            continue
        if os.path.isdir(i) == True:
            continue
        fileList.append(TorFile(i, os.path.getsize(i)))
    
    torrentSize = 0
    for i in fileList:
        torrentSize += i.fileSize
        
    pieceSize = pieceSizeCalc(torrentSize)
    
    torrentFullSize = 0
    for i in fileList:
        torrentFullSize += pieceSize * math.ceil(i.fileSize/pieceSize)
    
    #sort the files into large, medium, and small sizeed files
    # http://www.wolframalpha.com/input/?i=Plot%5Bx%2F(ceil(x%2F(256*1024))*1024*256),+%7Bx,+0,2*1024*1024%7D%5D
    largeFiles = []
    mediumFiles = []
    smallFiles = []
    for i in fileList:
        if i.fileSize > 4 * pieceSize:
            largeFiles.append(i)
        elif i.fileSize < pieceSize // 16:
            smallFiles.append(i)
        else:
            mediumFiles.append(i)

    #sorts list into acending order, makes it more efficent to 'pop' from the list
    largeFiles = sorted(largeFiles, key=lambda TorFile: TorFile.fileSize)
    mediumFiles = sorted(mediumFiles, key=lambda TorFile: TorFile.fileSize)
    smallFiles = sorted(smallFiles, key=lambda TorFile: TorFile.fileSize)
    
    startList = {}

    bookmark = 0 #used for showing next free byte
    piecemark = 0 #used for showing next free chunk
    
    # files are aligned to blocks (IE: files do not share blocks with other files)
    while len(largeFiles) != 0:
        #print("\t", "large", "estimated end", largeFiles[-1].fileSize - 1 + bookmark, "bookmark", bookmark, "piecemark", piecemark)
        temp = largeFiles.pop()
        startList[bookmark] = temp
        temp.start = bookmark
        piecemark = math.ceil((bookmark + temp.fileSize)/pieceSize) * pieceSize
        bookmark = piecemark
        
    # files are partially aligned to blocks, but any leftover space is filled with other files
    while len(mediumFiles) != 0:
        stuffing = True
        limiter = bookmark + math.ceil(mediumFiles[-1].fileSize/pieceSize) * pieceSize
        #print("Bookmark", bookmark, "limiter", limiter)
        
        while len(mediumFiles) != 0:
            #print("\t", "medium-medium", "estimated end", mediumFiles[-1].fileSize - 1 + bookmark, "limiter", limiter, "bookmark", bookmark, "piecemark", piecemark)
            if mediumFiles[-1].fileSize - 1 + bookmark > limiter:
                #print("\t\t", "breaking 1")
                break
            temp = mediumFiles.pop()
            startList[bookmark] = temp
            temp.start = bookmark
            piecemark = math.ceil((bookmark + temp.fileSize - 1)/pieceSize) * pieceSize
            bookmark = bookmark + temp.fileSize
        
        while (len(smallFiles) != 0):
            #print("\t", "medium-small", "estimated end", smallFiles[-1].fileSize - 1 + bookmark, "limiter", limiter, "bookmark", bookmark, "piecemark", piecemark)
            if smallFiles[-1].fileSize -1 + bookmark > limiter:
                #print("\t\t", "breaking 1")
                break            
            temp = smallFiles.pop()
            startList[bookmark] = temp
            temp.start = bookmark
            piecemark = math.ceil((bookmark + temp.fileSize - 1)/pieceSize) * pieceSize
            bookmark = bookmark + temp.fileSize
        
        bookmark = piecemark
        
    #throws all the small files together, with no chunk alignments
    while (len(smallFiles) != 0):
        #print("\t", "small", "estimated end", smallFiles[-1].fileSize - 1 + bookmark, "bookmark", bookmark, "piecemark", piecemark)
        temp = smallFiles.pop()
        startList[bookmark] = temp
        temp.start = bookmark
        piecemark = math.ceil((bookmark + temp.fileSize - 1)/pieceSize) * pieceSize
        bookmark = bookmark + temp.fileSize    
    
    return startList

torrentFiles = fileOrganizer(fileList)

#debug output
pieceSize = pieceSizeCalc(torrentSize)
for i in sorted(torrentFiles.keys()):
    debugTemp = []
    start = torrentFiles[i].start
    while start < torrentFiles[i].start + torrentFiles[i].fileSize - 1:
        debugTemp.append(start/pieceSize)
        start += pieceSize
    stderr.debug(torrentFiles[i], debugTemp)
        
#hash files larger then 256*1024
for i in sorted(torrentFiles.keys()):
    if torrentFiles[i].fileSize >= 256*1024:
        torrentFiles[i].fileHash = hashFile(torrentFiles[i].filePath)

class TorrentSerializedObject:
    import os
    """This creates a file like object that can be read() from for the entirety of the torrent, automatically zero filling gaps, and concatinating the files"""
    def __init__ (self, fileDictionary, peiceSize):
        self.buffer = bytes(0)
        self.bufferSize = peiceSize #set to the minumum chunk size possible for any torrent
        self.position = 0
        self.blockPosition = 0
        self.fileList = fileDictionary #a dictionary of files indexed by start position
        #self.currentFile = self.fileList[0]
        
        self.loadBuffer(0)
    
    def loadBuffer (self, position):
        #find the positions of the files
        temp = sorted(self.fileList.keys(), reverse=True)
        fileStart = None
        for i in temp:
            if position >= i:
                fileStart = i
                break
        stderr.debug("loadBuffer", "fileStart = " + str(fileStart))
        #fileStart is always <= position
        fileOffset = position - fileStart
        
        #handle condition where file ends before start of block
        
    
    def read (self, size):
        fileStart = self.currentFile.start
        
temp = TorrentSerializedObject(torrentFiles)
#generate data-structure for metadata file
'''
import math
import hashlib

filehash = int.from_bytes(filehash, byteorder='big')
files = {}
for i in fileList:
    files[i] = {"SIZE":filesize, "START":0, "END":filesize, "HASH": filehash}
    
numberOfPieces = math.ceil(filesize/torrentPieceSize)
pieceHashs = []
for i in range(0, numberOfPieces):
    h = hashlib.sha3_512()
    f1 = open(filepath, 'br')
    h.update(f1.read(torrentPieceSize))
    pieceHashs.append(int.from_bytes(h.digest(), byteorder='big'))
    del(h)

#fill in all data for data structure
infoFile = {"FILES": files, "PIECESIZE": torrentPieceSize, "NUMBEROFPIECES": numberOfPieces, "PIECEHASHS": pieceHashs}

#export to json
import json
jsonFile = json.dumps(infoFile, sort_keys=True, indent=1)
f1 = open(hex(filehash)[2:] + str(".json"), "w")
f1.write(jsonFile)
f1.close()

#reimport from json

#verify file against json metadata
'''
