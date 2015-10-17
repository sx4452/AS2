__author__ = 'ben'
# coding=UTF-8

import  math
import  time
from collections import defaultdict
from collections import Counter
from APRIORI import tree
from APRIORI import BuildHashTree
from APRIORI import Apriori
from CONSTANT import ITEMSNUM
from CONSTANT import TRANSNUM
from CONSTANT import MINSUP
from CONSTANT import M
from CONSTANT import L
from CONSTANT import R
from CONSTANT import VAL
from CONSTANT import DATAPATH
from CONSTANT import OUTPUTPATH

def InputData():
    inputFile = open(DATAPATH, 'r')
    inputRead = inputFile.readlines()
    inputFile.close()
    return inputRead

def DFSoutput(curNode, tmppos, resultPlus, outputFile):        #DFS the tree and output
    lasti = ''
    for i in curNode:
        if isinstance(i, int):
            if cmp(lasti, '') != 0:
                tmppos = tmppos[:-(len(str(lasti))+1)]
            tmppos = tmppos + ' ' + str(i)
            lasti = i                                           #lasti: for the same depth, use it to delete the formal position
            outputFile.write(tmppos[1:] + ' '+ str(float(resultPlus[tmppos[1:]])/float(TRANSNUM)) + '\n')
            curNode[i][VAL] = 1
            DFSoutput(curNode[i], tmppos, resultPlus, outputFile)

def OutputResultLexOrder(result):
    outputFile = open(OUTPUTPATH, 'w+')
    resultPlus = {}
    for i in result:
        if len(result[i]) != 0:
            for j in result[i]:
                jlist = j.split(',')
                tmpstr = ''
                for k in jlist:
                    tmpstr = tmpstr + ' ' + k
                resultPlus[tmpstr[1:]] = result[i][j]                  #combine the result into resultPlus to become one dict
    resultList = resultPlus.keys()
    for i in xrange(0, len(resultList)):
        resultList[i] = resultList[i].split(' ')
        for j in xrange(0,len(resultList[i])):
            resultList[i][j] = int(resultList[i][j])                  #turn resultPlux into a list
    resultTree = tree()
    curNode = resultTree
    for sublist in resultList:
        curNode = resultTree
        for ele in sublist:
            curNode = curNode[ele]                                    #build a output tree
    DFSoutput(resultTree, '', resultPlus, outputFile)
    outputFile.close()

def OutputResultSimple(result):
    outputFile = open(OUTPUTPATH, 'w+')
    for i in result:
        if len(result[i]) != 0:
            for j in result[i]:
                outputFile.write(j+' '+ str(float(result[i][j])/float(TRANSNUM)) + '\n\r')
    outputFile.close()

def main():
    start = time.clock()
    inputRead = InputData()
    HashTree = BuildHashTree(inputRead)
    result = Apriori(HashTree)
    OutputResultLexOrder(result)                     #output result in LexOrder by DFS implementation
    #OutputResultSimple(result)                      #output result with the constructions in result simply
    end = time.clock()
    print 'runing time is '
    print end

if __name__ == "__main__":
    main()

