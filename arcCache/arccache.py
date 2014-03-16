#!/usr/bin/env python
import sys
import time

# Authors:
# Robert Jellinek, Samer Al-Kiswany, Siva Ramasubramanian

class CacheItem():
  def __init__(self, addr):
    self.age = time.time()
    self.addr = addr

class LRU():
  def __init__(self, maxSize):
    self.items = []
    self.size = maxSize
    self.name = 'LRU cache'
    self.hits = 0

  def get(self, addr): 
    # see if item is in cache; if it is,
    # get the value and update its position in the cache
    index = self.search(addr)

    if index != -1:
      self.hits += 1
      del self.items[index]
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

class ArcCache():
  def __init__(self, cacheSize):
    self.t1 = LRU(0)
    self.t2 = LRU(0)
    self.b1 = LRU(0)
    self.b2 = LRU(0)
    self.size = 0    # p in the paper
    self.cache_size = cacheSize # c  in the paper
    self.hits = 0
    self.name = 'ArcCache'

  def get(self, addr):
    item = CacheItem(addr)
    # search t2 and t1 (remember: search() updates item, pulls
    # it to top of t2)
    t2_index = self.t2.search(addr)

    # it's in t2, update it an put it at top of t2
    if t2_index != -1:
      del self.t2.items[t2_index]
      self.t2.items.insert(0, item) 
      self.hits = self.hits + 1
      return

    # check if it's in t1. If so, take it from t1 and 
    # put it in t2
    t1_index = self.t1.search(addr)
    if t1_index != -1:
      del self.t1.items[t1_index]
      self.t2.items.insert(0, item)  
      self.hits = self.hits + 1
      self.size -= 1
      return

    # if it's in b1, delete from b1 and add to t2
    b1_index = self.b1.search(addr)
    if b1_index != -1:
      segma1 = self.computeSegma1()
      newSize = min(self.size + segma1, self.cache_size)
      del self.b1.items[b1_index]
      self.t2.items.insert(0, item)
      replace(item, newSize)
      self.hits += 1
      return

    # if it's in b2, delete from b2 and add to t2
    b2_index = self.b2.search(addr)
    if b2_index != -1:
      segma2 = self.computeSegma2()
      newSize = max(self.size - segma2, 0)
      del self.b2.items[b2_index]
      self.t2.items.insert(0, item)      
      replace(item, newSize)
      self.hits += 1
      return

    if (len(self.t1.items) + len(self.b1.items)) == self.cache_size:
      if len(self.t1.items) < self.cache_size:
        if self.b1.items:
          self.b1.items.pop()
        self.replace(item, self.size)
      else:
        self.t1.items.pop()
        self.size = self.size - 1
    else:
      if (len(self.t1.items) + len(self.b1.items) + len(self.t2.items) + len(self.b2.items)) >= self.cache_size:
        if self.b2.items:
          self.b2.items.pop()
        self.replace(item, self.size)
          
    # Else, if it's not in any cache, add it to t1
    self.t1.items.insert(0, item)
    self.size = self.size + 1

  def replace(self, item, newSize):
    b2_index = self.b2.search(item.addr)
    if (len(self.t1.items) > 0 and len(self.t1.items) > newSize) or (b2_index != -1 and len(self.t1.items) == newSize):
      self.t1.items.pop()
      self.b1.items.insert(0, item)
    else:
      self.t2.items.pop()
      self.b2.items.insert(0, item)      
    
  def computeSegma1(self):
    if len(self.b1.items) >= len(self.b2.items):
      return 1
    else:
      return len(self.b2.items)/len(self.b1.items)
    
  def computeSegma2(self):
    if len(self.b2.items) >= len(self.b1.items):
      return 1
    else:
      return len(self.b1.items)/len(self.b2.items)  

def loadCache(fname, cache):
  f = open(fname, 'r')
  numReqs = 0
  for line in f.readlines():
    cache.get(line.split('\n')[0])
    numReqs += 1
  f.close()
  return numReqs

def usage():
  print 'Usage: python arccache.py [trace file] [cache size]'

if __name__ == '__main__':
  usage()
  
  print '\nRun with trace files example-lru.txt and example-arc.txt to ' \
    'see traces that perform better under LRU and ARC respectively.\n\n'+'*'*80 +'\n\n'
  
  fname = sys.argv[1]
  csize = int(sys.argv[2])
  
  cache = ArcCache(csize)
  numReqs = loadCache(fname, cache)
  print 'Loaded %d unique entries into %s' % (numReqs, cache.name)
  print 'Reloading same entries into %s:' % cache.name
  numReqs = 2 * loadCache(fname, cache)
  print 'Hits: %d\tMisses: %d\n' % (cache.hits, numReqs - cache.hits)

  cache = LRU(csize)
  numReqs = loadCache(fname, cache)
  print 'Loaded %d unique entries into %s' % (numReqs, cache.name)
  print 'Reloading same entries into %s:' % cache.name
  numReqs = 2 * loadCache(fname, cache)
  print 'Hits: %d\tMisses: %d\n' % (cache.hits, numReqs - cache.hits)
  
