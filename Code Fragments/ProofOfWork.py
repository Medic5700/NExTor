"""an idea for a proof of work function, to minimize DOS attacks"""
import random

def primeList(limit):
    #temp is maximum number that a prime will be searched to
    assert limit >=2
    temp = [2]
    for i in range(2,limit):
        isPrime = True
        for j in temp:
            if i%j==0:
                isPrime = False
                break
        if isPrime == True:
            temp.append(i)
    return temp

pList = pList = primeList(100000)

def fac(temp):
    if temp == 1:
        return [1]
    i = 2
    while (i<=temp):
        if (temp%i) == 0:
            return [i] + fac(temp//i)
        i = i+1
        
def fac2(num):
    if num == 1:
        return [1]
    for i in pList:
        if num%i==0:
            return [i] + fac2(temp//i)

def factor(temp):
    temp = fac(temp)
    del(temp[len(temp)-1])
    temp.sort()
    return temp

def make(length):
    acc = 1
    temp = []
    for i in range(length):
        temp.append(pList[random.randint(0,len(pList)-1)])
        acc = acc * temp[-1]
    temp.sort()
    return acc,temp

def test(x):
    temp = make(x)
    print(temp[0])
    print(len(str(temp[0])))
    print(temp[1])
    print(factor(temp[0]))
