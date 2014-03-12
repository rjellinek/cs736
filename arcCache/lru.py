#!/usr/bin/env python
import sys
import time

# Input: read a stream of numbers

class CacheItem():
  def __init__(self, addr):
    self.age = time.time()
    self.addr = addr
    #self.data = data

class Cache():
  def __init__(self, maxSize):
    self.items = [] #Queue.PriorityQueue(maxSize)
    self.maxSize = maxSize

  def add(self, item): 
    time.sleep(.1)

    # see if item is in cache; if it is,
    # get the value and update its position in the cache
    val = self.search(item.addr)

    # item was not in cache
    if val is None:
      # if it's full and we're inserting, we need to evict first
      if len(self.items) >= self.maxSize:
        self.items.pop()
      item.age = time.time()
      self.items.insert(0, item)
  
  def search(self, addr):
    '''
    update timestamp and put item at top of list.
    return the val.
    '''
    for i in range(len(self.items)):
      if self.items[i].addr == addr:
        val = self.items[i]
        val.age = time.time()
        del(self.items[i])
        self.items.insert(0, val)
        return val
    return None

  def printCache(self):
    output = ''
    for i in range(len(self.items)):
      output += '%s\t%s\n' % (self.items[i].addr, self.items[i].age)
    
    print output

def loadCache(fname, cache):
  f = open(fname, 'r')
  for line in f.readlines():
    item = CacheItem(line.split('\n')[0])
    print 'Adding:\t%s\t%s' %(item.addr, item.age)
    cache.add(item)
  f.close()
  return cache

if __name__ == '__main__':
  fname = sys.argv[1]
  csize = sys.argv[2]
  cache = Cache(csize)
  cache = loadCache(fname, cache)
  print 'Cache: '
  cache.printCache()

  # test:
  lst = ['1234', '4312']
  for item in lst:
    print 'Adding %s:' % item
    cache.add(CacheItem(item))
    print 'Cache:' 
    cache.printCache()

