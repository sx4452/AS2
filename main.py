__author__ = 'ben'
# coding=UTF-8

from collections import defaultdict
from collections import Counter
from itertools import combinations
import  math
import  string
import  time

ITEMSNUM = 11
TRANSNUM = 1000
DATAPATH = "assignment2-data.txt"
OUTPUTPATH = "result.txt"
MINSUP = 0.144
R = 'right'
L = 'left'
M = 'middle'
VAL = 'count'

def tree():
    return defaultdict(tree, count = 0, isLeaf = False)

def add(t, keys, id):
    for key in keys:
        if(cmp(key,'') != 0):                        #skip the None string
            t = t[key]
    leaft = t[id]
    leaft['isLeaf'] = True
    leaft[VAL] = leaft.get(VAL) + 1

def LexOrderSubset(originset):
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

def Aprioi(HashTree):
    k = 0
    F = {}
    C = {}
    F[k] = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0, '10':0, '11':0}
    for i in F[k]:
        F[k][i] = SupportCount(HashTree, i.split(','))
    while len(F[k]) != 0:
        C[k+1] = {}
        for i in F[k]:
            for j in F[k]:
                if(cmp(i,j) != 0):
                    tmpstr = ''
                    list1 = i.split(',')
                    list2 = j.split(',')
                    for m in list1:
                        for n in list2:
                            if(tmpstr.find(m) == -1):
                                tmpstr = tmpstr + ',' + m
                            if(tmpstr.find(n) == -1):
                                tmpstr = tmpstr + ',' + n
                    dotcounter = Counter(tmpstr)
                    if dotcounter[','] ==  k+2:
                        C[k+1][tmpstr[1:]] = 0
        #comb[k+1] = combinations(F[k], 2)
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
        for i in tuplist:
            if curele > int(i):
                del C[tup]
                break
            else:
                curele = int(i)
                if cmp(i, '10') != 0 and cmp(i, '11') !=0:
                    pos = tup.index(i)
                    if len(tup) > pos + 1:
                        tmptup = tup[:pos] + tup[pos+2:]
                    else:
                        tmptup = tup[:-2]
                    if F.has_key(tmptup) == False:
                        del C[tup]
                        break
                else:
                     pos = tup.index(i)
                     if len(tup) > pos + 2:
                        tmptup = tup[:pos] + tup[pos+3:]
                     else:
                        tmptup = tup[:-3]
                     if F.has_key(tmptup) == False:
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
                #tmpHashTree = tmpHashTree[tmppos]
            if(math.fmod(int(i), 3) == 1):
                tmpHashTree = tmpHashTree[M]
                tmppos = tmppos + i
                #tmpHashTree = tmpHashTree[tmppos]
            if(math.fmod(int(i), 3) == 2):
                tmpHashTree = tmpHashTree[R]
                tmppos = tmppos + i
                #tmpHashTree = tmpHashTree[tmppos]
    return tmpHashTree[tmppos][VAL]

def BuildHashTree(inputRead):
    HashTree = tree()
    for inputline in inputRead:
        if(len(inputline) > 23):                #skip the first line:1 2 3 4 5 6 7 8 9 10 11\n
            continue
        tmpID = ''
        for itemcnt in xrange(1, ITEMSNUM+1):
            if(inputline[2*(itemcnt-1)]  == '1'):
                if(math.fmod(itemcnt, 3) == 0):
                    tmpID = tmpID + ',' + str(itemcnt)
                if(math.fmod(itemcnt, 3) == 1):
                    tmpID = tmpID + ',' + str(itemcnt)
                if(math.fmod(itemcnt, 3) == 2):
                    tmpID = tmpID + ',' + str(itemcnt)
        IDlist = tmpID.split(',')[1:]
        subSet = LexOrderSubset(IDlist)
        for set in subSet:
            tmppos = ''
            tmpID = ''
            setlist = set.split(',')
            for i in setlist:
                if(math.fmod(int(i), 3) == 0):
                    tmppos = tmppos + ',' + L
                if(math.fmod(int(i), 3) == 1):
                    tmppos = tmppos + ',' + M
                if(math.fmod(int(i), 3) == 2):
                    tmppos = tmppos + ',' + R
                tmpID = tmpID + i
            add(HashTree, tmppos.split(','), tmpID)
    return HashTree

def InputData():
    inputFile = open(DATAPATH, 'r')
    inputRead = inputFile.readlines()
    inputFile.close()
    return inputRead

def OutputResult(result):
    outputFile = open(OUTPUTPATH, 'w+')
    '''
    tmp = {}
    for i in result:
        tmp[i] = {}
        if len(result[i]) != 0:
            for j in result[i]:
                jlist = j.split(',')
                tmpstr = ''
                for k in jlist:
                    tmpstr = tmpstr + k
                tmp[i][tmpstr] = result[i][j]
    '''
    resultPlus = {}
    for i in result:
        if len(result[i]) != 0:
            for j in result[i]:
                jlist = j.split(',')
                tmpstr = ''
                for k in jlist:
                    tmpstr = tmpstr + ' ' + k
                resultPlus[tmpstr[1:]] = result[i][j]
    '''
    outputTree = tree()
    itemlist = resultPlus.iteritems().split(' ')
    items = sorted(resultPlus[i].items(),key=lambda d:d[0])
    for key,value in items:
    '''
    for i in resultPlus:
        #print key, value # print key,dict[key]
        #outputFile.write(key + ' '+ str(float(value)/float(TRANSNUM)) + '\n\r')
        outputFile.write(i + ' '+ str(float(resultPlus[i])/float(TRANSNUM)) + '\n\r')
    outputFile.close()

def main():
    start = time.clock()
    inputRead = InputData()
    HashTree = BuildHashTree(inputRead)
    result = Aprioi(HashTree)
    OutputResult(result)
    end = time.clock()
    print 'runing time is '
    print end

if __name__ == "__main__":
    main()

