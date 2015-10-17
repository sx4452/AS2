__author__ = 'ben'
# coding=UTF-8

import  math
import  time
from collections import defaultdict
from collections import Counter
from CONSTANT import ITEMSNUM
from CONSTANT import TRANSNUM
from CONSTANT import MINSUP
from CONSTANT import M
from CONSTANT import L
from CONSTANT import R
from CONSTANT import VAL

def tree():
    return defaultdict(tree, count = 0, isLeaf = False)      #simple tree in python!IMPORTANT!

def add(t, keys, id):
    for key in keys:
        if(cmp(key,'') != 0):                        #skip the None string
            t = t[key]
    leaft = t[id]
    leaft['isLeaf'] = True
    leaft[VAL] = leaft.get(VAL) + 1                   #count the support

def LexOrderSubset(originset):#from bottom to top: for each element in originset, put them one by one into current subset
    allset =[]
    for i in originset:
        ele = i
        curlength = len(allset)
        for j in range(0,curlength):
            if(cmp(ele, allset[j]) != 0):
                tmpele = allset[j] + ',' + ele
                allset.append(tmpele)
        allset.append(ele)
    return allset

def Apriori(HashTree):
    k = 0
    F = {}
    C = {}
    F[k] = {}
    for i in range(1, ITEMSNUM+1):                          #Init F[0]
        F[k][str(i)] = 0
    for i in F[k]:
        F[k][i] = SupportCount(HashTree, i.split(','))      #Count F[0]
    while len(F[k]) != 0:                                   #Boundary conditions: when current F is null
        C[k+1] = {}
        for i in F[k]:
            for j in F[k]:
                if(cmp(i,j) != 0):
                    tmpstr = ''
                    list1 = i.split(',')
                    list2 = j.split(',')
                    for m in list1:
                        for n in list2:
                            if(tmpstr.find(m) == -1):          #combine pairs of F[k] in C[k+1]
                                tmpstr = tmpstr + ',' + m
                            if(tmpstr.find(n) == -1):
                                tmpstr = tmpstr + ',' + n
                    dotcounter = Counter(tmpstr)
                    if dotcounter[','] ==  k+2:               #delete which length is not equal to current k
                        C[k+1][tmpstr[1:]] = 0
        Prune(C[k+1], F[k], k)
        for i in C[k+1].keys():
            strlist = i.split(',')
            C[k+1][i] = SupportCount(HashTree, strlist)
            if float(C[k+1][i])/float(TRANSNUM) < (MINSUP - 0.001):
                del C[k+1][i]
        F[k+1] = C[k+1]
        k = k + 1
    return F

def Prune(C, F, k):
    for tup in C.keys():
        tuplist = tup.split(',')
        curele = -1
        for i in tuplist:                     #take away element in C.keys one by one and check if they are in F
            if curele > int(i):               #delete those repeated in order
                del C[tup]
                break
            else:
                curele = int(i)
                pos = tup.index(i)
                if len(tup) > pos + len(i):
                    tmptup = tup[:pos] + tup[pos+len(i)+1:]
                else:
                    tmptup = tup[:-(len(i)+1)]
                if F.has_key(tmptup) == False:                #delete those subtup not meet the downward closure
                    del C[tup]
                    break

def SupportCount(HashTree, id):
    tmpHashTree = HashTree
    tmppos = ''
    for i in id:
        if(cmp(i, '') != 0):
            if(math.fmod(int(i), 3) == 0):
                tmpHashTree = tmpHashTree[L]
                tmppos = tmppos + i
            if(math.fmod(int(i), 3) == 1):
                tmpHashTree = tmpHashTree[M]
                tmppos = tmppos + i
            if(math.fmod(int(i), 3) == 2):
                tmpHashTree = tmpHashTree[R]
                tmppos = tmppos + i
    return tmpHashTree[tmppos][VAL]

def BuildHashTree(inputRead):
    HashTree = tree()
    for inputline in inputRead:
        if(len(inputline) > 23):                #skip the first line:1 2 3 4 5 6 7 8 9 10 11\n
            continue
        tmpID = ''
        for itemcnt in xrange(1, ITEMSNUM+1):       #itemcnt from 1 to ITEMSNUM
            if(inputline[2*(itemcnt-1)]  == '1'):
                if(math.fmod(itemcnt, 3) == 0):
                    tmpID = tmpID + ',' + str(itemcnt)
                if(math.fmod(itemcnt, 3) == 1):
                    tmpID = tmpID + ',' + str(itemcnt)
                if(math.fmod(itemcnt, 3) == 2):
                    tmpID = tmpID + ',' + str(itemcnt)
        IDlist = tmpID.split(',')[1:]
        subSet = LexOrderSubset(IDlist)                   #subSet:all the subset of IDlist in LexOrder
        for set in subSet:
            tmppos = ''
            tmpID = ''
            setlist = set.split(',')
            for i in setlist:                           # 0 in left 1 in middle 2 in right
                if(math.fmod(int(i), 3) == 0):
                    tmppos = tmppos + ',' + L
                if(math.fmod(int(i), 3) == 1):
                    tmppos = tmppos + ',' + M
                if(math.fmod(int(i), 3) == 2):
                    tmppos = tmppos + ',' + R
                tmpID = tmpID + i
            add(HashTree, tmppos.split(','), tmpID)
    return HashTree
