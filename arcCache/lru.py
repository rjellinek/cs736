#!/usr/bin/env python
import sys
import time

# Input: read a stream of numbers

class CacheItem():
  def __init__(self, addr):
    self.age = time.time()
    self.addr = addr

class Cache():
  def __init__(self, maxSize):
    self.items = []
    self.size = maxSize

  def get(self, addr): 
    # see if item is in cache; if it is,
    index = self.search(addr)

    # is in the cache
    if index != -1:
      # put the item at the top of the list
      del self.items[index]
    # cache is full, pop something
    else:
      if len(self.items) >= self.size:
        self.items.pop()
        
    item = CacheItem(addr)
    self.items.insert(0, item) 

  
  def search(self, addr):
    '''
    update timestamp and put item at top of list.
    return the val.
    '''
    for i in range(len(self.items)):
      if self.items[i].addr == addr:
        return i
    return -1

  def printCache(self):
    output = ''
    for i in range(len(self.items)):
      output += '%s\t%s\n' % (self.items[i].addr, self.items[i].age)
    
    print output

def loadCache(fname, cache, timesToLoad=1):
  f = open(fname, 'r')
  for line in f.readlines():
    # print 'Adding:\t%s\t%s' %(item.addr, item.age)
    cache.get(line.split('\n')[0])
  f.close()
  return cache
 
def runTest(cache, fname):
  print 'Running test on cache with maxSize=%d' % cache.maxSize
  

if __name__ == '__main__':
  fname = sys.argv[1]
  csize = int(sys.argv[2])
  cache = Cache(csize)
  cache = loadCache(fname, cache)
  #print 'Cache: '
  cache.printCache()

  lst = ['11', '22', '33', '44']
  for item in lst:
    print 'Adding %s:' % item
    cache.get(item)
    print 'Cache:' 
    cache.printCache()

