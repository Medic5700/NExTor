import json

#test variables to store
varInt = 16
varReal = 5.0
varString = "Test"
varBool = True
varList = [1,2,3,4,5]
varList2 = [[1,2,3,4,5],[6,7,8,9,0]]
varTuple = (1,2,3)
varDic = {1:'s',3:'4',2:'a'}
varDic2 = {1:5,3:6,2:7}

'''
# https://docs.python.org/3/library/pickle.html#comparison-with-json
12.1.1.2. Comparison with json

There are fundamental differences between the pickle protocols and JSON (JavaScript Object Notation):
•JSON is a text serialization format (it outputs unicode text, although most of the time it is then encoded to utf-8), while pickle is a binary serialization format;
•JSON is human-readable, while pickle is not;
•JSON is interoperable and widely used outside of the Python ecosystem, while pickle is Python-specific;
•JSON, by default, can only represent a subset of the Python built-in types, and no custom classes; pickle can represent an extremely large number of Python types (many of them automatically, by clever usage of Python’s introspection facilities; complex cases can be tackled by implementing specific object APIs).
'''

#Do not use pickel, so many security concerns.

'''test variable file structures, a prototype for actual data structures to use to represent needed data'''
#single file
fileName = "Test.tmp"
fileSize = 64*1024*1024
fileHash = 2**512
numberOfPieces = 128
pieceSize = 512*1024
pieceHashs = {}
for i in range(0,512):
    pieceHashs[i] = 2**512

#multifile
files = {"Path1.tmp":{"SIZE":64*1024*1024, "START":0, "END":64*1024*1024, "HASH": 2**512},
         "Path2.tmp":{"SIZE":64*1024*1024, "START":64*1024*1024, "END":2*64*1024*1024, "HASH": 2**512}
         }
pieceSize = 512*1024
numberOfPieces = 256
pieceHashs = []
for i in range(0,256):
    pieceHashs.append(2**512)
infoFile = {"FILES": files, "PIECESIZE": pieceSize, "NUMBEROFPIECES": numberOfPieces, "PIECEHASHS": pieceHashs}

#Note: all string dictionary keys that are used for the program are capitalized (file names excepted)
jsonFile = json.dumps(infoFile, sort_keys=True, indent=1) #Note: json is sorted, and indentation is used
print(jsonFile)
temp = json.loads(jsonFile)
print(temp)
