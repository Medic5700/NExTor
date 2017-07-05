#assert triangle inequality
for i in range(0,16):
    for j in range(0,16):
        for k in range(0,16):
            if i > j or j > k: #assert test points are ordered
                continue
            #print("test1",i,j,k)
            if ((i^j) <= (i^k+k^j)):
                #print(True)
                pass
            else:
                print("test1",i,j,k)
                print(False)
                exit()
print("Test1 completed")

#assert triangle inequality
for i in range(0,16):
    for j in range(0,16):
        for k in range(0,16):
            if i > j or j > k: #assert test points are ordered
                continue
            #print("test2",i,j,k)
            if ((i^k) <= (i^k+k^j)):
                #print(True)
                pass
            else:
                print("test2",i,j,k)
                print(False)
                exit()
print("Test2 completed")

#a Kademlia node simulation over an 8-bit space (256 nodes)
print("Generating Kademlia test1 nodes")
import random
nodes = {}
bucketSize = 16
for i in range(0,256):
    buckets = []
    for j in range(0,8):
        bucket = []
        k = 0
        while (k < 1024*1) and (len(bucket) <= 2**j) and (len(bucket) < bucketSize): #note the bucket size limiter, 2**j. Limites bucket size to maximum possible nodes in that range.
            k += 1
            t = random.randint(0,256)
            if 2**j <= t^i < 2**(j+1):
                if not(t in bucket) and t != i:
                    bucket.append(t)
        buckets.append(bucket)
    nodes[i] = buckets
print("Kademlia test1 nodes generated")
#print(nodes)

print("Scanning nodes")
subOptimal = 0
for i in nodes:
    for j in range(0,8):
        if (not(len(nodes[i][j]) == min(2**j, bucketSize))):
            print("Node " + str(i))
            print("\t" + "Bucket " + str(j))
            print("\t" + "Expected size = " + str(min(2**j, bucketSize)))
            print("\t" + "Bucket size = " + str(len(nodes[i][j])))
            print("\t" + str(nodes[i]))
            print("\t" + str(nodes[i][j]))
            subOptimal += 1

print("Suboptimally filled node buckets = " + str(subOptimal))
print("Nodes scanned")

def pathFinder(start,end):
    """Takes a start node number and an end node number, returns list of nodes representing path between start and end nodes."""
    import math
    import random
    global nodes
    path = [start]
    currentNode = start
    i = 0
    while i < 8 and (currentNode ^ end != 0):
        print("i = " + str(i))
        print("\t" + "Node = " + str(currentNode))
        distance = currentNode ^ end
        distanceLog = math.floor(math.log2(distance)) #which bucket to look in
        print("\t" + "distance = " + str(distance))
        print("\t" + "log = " + str(distanceLog))
        tempBucket = nodes[currentNode][distanceLog]
        print("\t" + "Bucket = " + str(tempBucket))
        tempNode = tempBucket[random.randint(0, len(tempBucket) - 1)]
        print("\t" + "New node = " + str(tempNode))
        path.append(tempNode)
        currentNode = tempNode        
        i += 1
    return path

def pathFinder2(start,end):
    """Takes a start node number and an end node number, returns list of nodes representing path between start and end nodes. If no path possible, returns as much of possible path."""
    import math
    import random
    global nodes
    global bucketSize
    path = [start]
    currentNode = start
    i = 0
    while i < bucketSize and (currentNode ^ end != 0):
        print("i = " + str(i))
        print("\t" + "Node = " + str(currentNode))
        distance = currentNode ^ end
        distanceLog = math.floor(math.log2(distance)) #which bucket to look in
        print("\t" + "distance = " + str(distance))
        print("\t" + "log = " + str(distanceLog))
        tempBucket = nodes[currentNode][distanceLog]
        print("\t" + "Bucket = " + str(tempBucket))
        for j in range(distanceLog, bucketSize):
            if len(tempBucket) != 0:
                tempNode = tempBucket[random.randint(0, len(tempBucket) - 1)]
                break
            else:
                print("\t" + "Empty bucket, trying next bucket")
                tempBucket = nodes[currentNode][j]
                print("\t" + "Bucket = " + str(tempBucket))
        print("\t" + "New node = " + str(tempNode))
        path.append(tempNode)
        currentNode = tempNode
        i += 1
    return path

def pathFinder3(start, end):
    """Takes a start node number and an end node number, returns list of nodes representing path between start and end nodes. If no path possible, returns as much of possible path."""
    import random
    import math
    global nodes
    if (start ^ end == 0): #recursive terminator
        return []
    #select a node
    buckets = nodes[start]
    bucket = buckets[math.floor(math.log2(start ^ end))]
    if len(bucket) == 0:
        return []
    node = bucket[random.randint(0, len(bucket) - 1)]
    path = pathFinder3(node, end) #recursive call
    #unzip and rezip result into 1 dimensional array
    result = [node]
    for i in path:
        result.append(i)
    return result
    
print("finding path from 0 to 255")
for i in range(0,8):
    print("\t", pathFinder3(0, 255))
print("finding path from 254 to 0")
for i in range(0,8):
    print("\t", pathFinder3(254, 0))

#deletes node 255 for testing purposes
print("Removing element 255 from nodes")
for i in nodes:
    for j in range(0, len(nodes[i])):
        for k in range(len(nodes[i][j]) - 1, 0 - 1, -1): #backwards, to get around the 'you are iterating over what you are deleting' problem
            if nodes[i][j][k] == 255:
                print("Deleting element = ",i,j,k)
                if len(nodes[i][j]) == 1:
                    nodes[i][j] = []
                else:
                    del(nodes[i][j][k])

print("finding path from 0 to 255")
for i in range(0,8):
    print(pathFinder3(0, 255))
print("finding path from 254 to 0")
for i in range(0,8):
    print(pathFinder3(254, 0))
