#!/usr/bin/env python

# maps thread_id -> [(addr,op)...]
threads = {}

# maps thread_id -> [locks]
# 1: 
locks_held = {}

# map address -> set(locks held)
lockset = {}

def add_operation(s):
  '''
  lock trace format: addrRL, addrWL
  '''
  thread_id, addr, op = s.split(',')
  
  entry = str(thread_id+":"+addr+":"+op)
  
  if op == 'l':
    if thread_id not in locks_held:
      locks_held[thread_id] = set(entry) 
    else:
      locks_held[thread_id].add(entry)
    
    if addr not in lockset:
      lockset[addr] = set(entry)
    else:
      lockset[addr] = lockset[addr].intersection(locks_held[thread_id])
      if not len(lockset[addr]):
        print "Lockset empty for address " + addr
  
  elif op=='u':
    if thread_id not in locks_held:
      print "Trying to release unheld locks"
    else:
      locks_held[thread_id].remove(entry)
    
    if addr not in lockset:
      print "No locks on address"
    else:
      lockset[addr].remove(entry)


def read_trace(trace):
  '''
  trace format:
  thread_id:int,addr:int,operation:{'r','w','l','u'}
  '''
  for line in trace:
    
  
