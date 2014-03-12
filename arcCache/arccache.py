#!/usr/bin/env python
import sys
import time

## print FINAL hits misses

# Input: read a stream of numbers

class CacheItem():
  def __init__(self, addr):
    self.age = time.time()
    self.addr = addr
    #self.data = data

class ArcCache():
  def __init__(self, maxSize):
    self.t1 = Cache(maxSize)
    self.t2 = Cache(maxSize)
    self.b1 = Cache(maxSize)
    self.b2 = Cache(maxSize)

  def add(self, item):
    # search t2 (remember: search() updates item, pulls
    # it to top of t2)
    i = self.t2.search(item.addr)

    # it's in t2, update it an put it at top of t2
    if i != -1:
      val = self.t2.items[i]
      val.age = time.time()
      del(self.t2.items[i])
      self.t2.items.add(val)
      return

    # check if it's in t1. If so, take it from t1 and 
    # put it in t2
    i = self.t1.search(item.addr)
    if i != -1:
      # evict from t1
      val = self.t1.items[i]
      val.age = time.time()
      del(self.t1.items[i])
      self.t2.add(val)
      return

    # if it's in b1, delete from b1 and add to t2
    i = self.b1.search(item.addr)
    if i != -1:
      # evict from b1
      val = self.b1.items[i]
      val.age = time.time()
      del(self.b1.items[i])
      self.t2.add(val)
      return


    # if it's in b2, delete from b2 and add to t2
    i = self.b2.search(item.addr)
    if i != -1:
      # evict from b2
      val = self.b2.items[i]
      val.age = time.time()
      del(self.b2.items[i])
      self.t2.add(val)
      return

    # Else, if it's not in any cache, add it to t1
    self.t1.add(item)


      

class Cache():
  def __init__(self, maxSize):
    self.items = [] #Queue.PriorityQueue(maxSize)
    self.maxSize = maxSize

  def add(self, item): 
    time.sleep(.1)

    # see if item is in cache; if it is,
    # get the value and update its position in the cache
    i = self.search(item.addr)

    # item was not in cache
    if i == -1:
      # if it's full and we're inserting, we need to evict first
      if len(self.items) >= self.maxSize:
        self.items.pop()
      item.age = time.time()
      self.items.insert(0, item)
    else:
      val = self.items[i]
      val.age = time.time()
      del(self.items[i])
      self.items.insert(0, val)
      
  
  def search(self, addr):
    '''
    return index of item in cache list
    '''
    for i in range(len(self.items)):
      if self.items[i].addr == addr:
        return i
        #val = self.items[i]
        #val.age = time.time()
        #del(self.items[i])
        #self.items.insert(0, val)
        #return val
    return -1

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

