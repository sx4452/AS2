__author__ = 'ben'

def power_set(s):
    n = len(s)
    test_marks = [ 1<<i for i in range(0, n) ]
    for k in range(0, 2**n):
        l = []
        for idx, item in enumerate(test_marks):
            if k&item:
                l.append(s[idx])
        yield set(l)
#A simple test
def __test__():
    s = [1,2,3,4]
    for e in power_set(s):
        print e
__test__()

