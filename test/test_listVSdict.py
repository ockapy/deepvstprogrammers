# test list vs dict
from timeit import default_timer as timer
import array
import numpy as np

class TestListVSDict:
    def __init__(self,size=155):
        self.list = [0]*size
        self.dict = {}
        self.array = array.array('i',[0]*size)
        self.npArray = np.zeros(size,dtype=np.int32)

    def setList(self,i,x):
        self.list[i] = x
    
    def setDict(self,i,x):
        self.dict[i] = x

    def setArray(self,i,x):
        self.array[i] = x

    def setNpArray(self,i,x):
        self.npArray[i] = x


size = 155
repeat = 100000
testListVSDict = TestListVSDict(size)

start = timer()
for rep in range(repeat):
    for i in range(size):
        testListVSDict.setNpArray(i,i)
end = timer()
print("NP Array ",end - start)

start = timer()
for rep in range(repeat):
    for i in range(size):
        testListVSDict.setList(i,i)
end = timer()
print("List ",end - start)


start = timer()
for rep in range(repeat):
    for i in range(size):
        testListVSDict.setDict(i,i)
end = timer()
print("Dict ",end - start)

start = timer()
for rep in range(repeat):
    for i in range(size):
        testListVSDict.setArray(i,i)
end = timer()
print("Array ",end - start)


