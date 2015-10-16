__author__ = 'ben'
# coding=UTF-8
import  time

ITEMSNUM = 11
TRANSNUM = 1000
DATAPATH = "assignment2-data.txt"
MINSUP = 0.144

def InputData():
    inputFile = open(DATAPATH, 'r')
    inputRead = inputFile.readlines()
    return inputRead

def main():
    start = time.clock()
    inputRead = InputData()
    data = {}
    transcnt = 0
    cnt = 0
    result = {}
    for inputline in inputRead:
        if(len(inputline) > 24):                #skip the first line:1 2 3 4 5 6 7 8 9 10 11
            continue
        data[transcnt] = {}
        for itemcnt in xrange(0, ITEMSNUM):
            if(inputline[2*itemcnt]  == '1'):
                data[transcnt][itemcnt] = 1
            else:
                data[transcnt][itemcnt] = 0
        transcnt += 1

    for j in xrange(0,ITEMSNUM):
        result[j] = {}
        for k in xrange(0,ITEMSNUM):
                if j < k:
                    result[j][k] = 0


    for i in xrange(0,TRANSNUM):
        for j in xrange(0,ITEMSNUM):
            for k in xrange(0,ITEMSNUM):
                if j < k:
                    if(data[i][j] == 1 and data[i][k] == 1):
                        result[j][k] += 1

    for j in xrange(0,ITEMSNUM):
            for k in xrange(0,ITEMSNUM):
                if j < k:
                    print str(j)+str(k)+' '+str(result[j][k])

    end = time.clock()
    print 'runing time is '
    print end

if __name__ == "__main__":
    main()


