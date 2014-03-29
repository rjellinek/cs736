#!/usr/bin/env python

import sys

# maps thread_id -> [(addr,op)...]
threads = {}

# maps thread_id -> [locks]
# 1: 
locks_held = {}

# map address -> set(locks held)
C = {}

def populate_C(filename):
  '''
  initialize C(addr) (which is C(v)) to set of all 
  locks
  '''
  with open(filename,'r') as fp:
    trace = fp.readlines()
    
    # populate all addresses (all variables)
    # i.e. create C(v) for each v
    for line in trace:
      thread_id, addr, op = line.split(',')
      if addr not in C:
        C[addr] = set()
    

    # for each v (addr), initialize C(v) (C[addr]) to the set of all locks
    for line in trace:
      thread_id, lock_addr, op = line.split(',')
      if 'l' in op: # not differentiating r/w locks here
        for addr in C:
          C[addr].add(lock_addr) # represents a lock on the var corresponding
                                    # to the operations's address
    print 'C: '
    print C

def process_entry(entry):
  '''
  //lock trace format: addrRL, addrWL
  '''
  thread_id, addr, op = entry.split(',')
  
  if 'l' in op:
    if thread_id not in locks_held:
      locks_held[thread_id] = set() 

    # check that no other thread is holding this lock
    for t in locks_held:
      if t != thread_id and addr in locks_held[t]:
        print 'Error, thread %s is holding the lock while thread %s is ' \
          'requesting it' % (t, thread_id)
        sys.exit()

    locks_held[thread_id].add(addr)
    
  elif 'u' in op:
    if thread_id not in locks_held:
      print "Trying to release unheld locks"
    else:
      locks_held[thread_id].remove(addr)

  elif 'r' in op or 'w' in op:
    C[addr].intersection_update(locks_held[thread_id])
    print 'C[%s] = ' % addr
    print C[addr]
    if not len(C[addr]):
      print 'ERROR! C[%s] is empty, lock not protecting shared resource!' % addr
      sys.exit()
  print 'locks_held'
  print locks_held

def print_Cs():
  for addr in C:
    print 'C(%s): ' % addr
    print C[addr]

def run(filename):
  '''
  trace format:
  thread_id:int,addr:int,operation:{'r','w','l','u'}
  '''
  populate_C(filename)
  with open(filename,'r') as fp:
    trace = fp.readlines()
    for line in trace:
      print_Cs()
      print '\n\n\n'
      process_entry(line)

if __name__ == '__main__':
  if not len(sys.argv) == 2:
    print 'Usage: eraser.py [filename]'

  run(sys.argv[1])
  print 'Success!'
