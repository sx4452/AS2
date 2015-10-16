__author__ = 'ben'
# coding=UTF-8

from collections import defaultdict
from itertools import combinations
import  math
import  string
import  time

ITEMSNUM = 11
TRANSNUM = 1000
DATAPATH = "assignment2-data.txt"
MINSUP = 0.144
R = 'right'
L = 'left'
M = 'middle'
#ID = 'itemset'
VAL = 'count'

def tree():
    return defaultdict(tree, count = 0, isLeaf = False)

def add(t, keys, id):
    idcnt = 1
    pos = ''
    for key in keys:
        if(cmp(key,'') != 0):                        #skip the None string
            t = t[key]
            pos = pos + id[idcnt] + ','
            t = t[pos]
            t['isLeaf'] = True
            t[VAL] = t.get(VAL) + 1
            idcnt += 1

 #   t[ID] = id

#def dicts(t): return {k: dicts(t[k]) for k in t}

def Aprioi(HashTree):
    F = {}
    C = {}
    comb = {}
    F[0] = ['0','1','2','3','4','5','6','7','8','9']
    for k in xrange(0, ITEMSNUM):
        comb[k+1] = combinations(F[k], 2)
        C[k+1] = {}
        cnt = 0
        for i in comb[k+1]:
            C[k+1][cnt] = i[0]+i[1]
            cnt += 1
#        print list(F[k+1])
        
        '''
        for i in F[k+1]:
            if(i is not in F[k])
                del i
            else:
                SupportCount(HashTree)

        F[k+1] = C[k+1]
    print 'doing Aprioi...'
    '''


def SupportCount(HashTree, id):
    tmpHashTree = HashTree
    for i in id:
        if(math.fmod(i, 3) == 0):
            tmppos = tmppos + ',' + L
            tmpHashTree = tmpHashTree[L]
        if(math.fmod(i, 3) == 1):
            tmppos = tmppos + ',' + M
            tmpHashTree = tmpHashTree[M]
        if(math.fmod(i, 3) == 2):
            tmppos = tmppos + ',' + R
            tmpHashTree = tmpHashTree[R]
    sup = tmpHashTree[VAL]
    return sup

'''
def BuildHashTree(transcnt, itemcnt, data, str):
        if(itemcnt >= 11):
            HashTree = tree()
            add(HashTree, str.split(','))
            return HashTree
        else:
            if(data[transcnt][itemcnt] == '1'):
                if(math.fmod(itemcnt, 3) == 0):
                    return BuildHashTree(transcnt, itemcnt+1, data, str + ',' + L)
                if(math.fmod(itemcnt, 3) == 1):
                    return BuildHashTree(transcnt, itemcnt+1, data, str + ',' + M)
                if(math.fmod(itemcnt, 3) == 2):
                    return BuildHashTree(transcnt, itemcnt+1, data, str + ',' + R)
            else:
                return BuildHashTree(transcnt, itemcnt+1, data, str)
'''

def InputData():
    inputFile = open(DATAPATH, 'r')
    inputRead = inputFile.readlines()
    return inputRead

def BuildHashTree(inputRead):
    HashTree = tree()
    transcnt = 0
    for inputline in inputRead:
        if(len(inputline) > 24):                #skip the first line:1 2 3 4 5 6 7 8 9 10 11
            continue
        tmppos = ''
        tmpID = ''
        for itemcnt in xrange(0, ITEMSNUM):
            if(inputline[2*itemcnt]  == '1'):
                if(math.fmod(itemcnt, 3) == 0):
                    tmppos = tmppos + ',' + L
                    tmpID = tmpID + ',' + str(itemcnt)
                if(math.fmod(itemcnt, 3) == 1):
                    tmppos = tmppos + ',' + M
                    tmpID = tmpID + ',' + str(itemcnt)
                if(math.fmod(itemcnt, 3) == 2):
                    tmppos = tmppos + ',' + R
                    tmpID = tmpID + ',' + str(itemcnt)
        add(HashTree, tmppos.split(','), tmpID.split(','))
            #DATA[transcnt][itemcnt] = inputline[2*itemcnt]            #data from transcnt = 1, the 0 line is item
        transcnt += 1

    return HashTree
    '''
    for i in range(0,ITEMSNUM):
        for j in range(0,TRANSNUM):
            print DATA[i][j]
    '''

def main():
    start = time.clock()
    inputRead = InputData()
    HashTree = BuildHashTree(inputRead)
#   Aprioi(HashTree)

#   SupportCount(data)
    end = time.clock()
    print 'runing time is '
    print end

if __name__ == "__main__":
    main()

