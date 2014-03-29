#!/usr/bin/env python

##
## Rob Jellinek and Siva Ramasubramanian
## 

import sys

# maps thread_id -> [locks]
locks_held = {}

# map variable -> set(locks held)
C = {}

# dict of {var:set of threads using it}
# if |thread_set| > 1, var is initialized 
initialized = {}

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
      if '#' in line:
        continue
      thread_id, var, op = line.split(',')
      if var not in C:
        C[var] = set()

      if var not in initialized:
        initialized[var] = set()
      
      # populate locks_held table at the same time. 
      # this is important for threads that initially 
      # access vars without locks, before they're initialized.
      if thread_id not in locks_held:
        locks_held[thread_id] = set() 
    
    # for each v (addr), initialize C(v) (C[addr]) to the set of all locks
    for line in trace:
      if '#' in line:
        continue
      thread_id, lock_addr, op = line.split(',')
      if 'l' in op: # not differentiating r/w locks here
        for addr in C:
          C[addr].add(lock_addr) # represents a lock on the var corresponding
                                    # to the operations's address

def process_entry(entry):
  '''
  //lock trace format: addrRL, addrWL
  '''
  if '#' in entry:
    return

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
    initialized[addr].add(thread_id)
    
  elif 'u' in op:
    if thread_id not in locks_held:
      print "Trying to release unheld locks"
    else:
      locks_held[thread_id].remove(addr)

  elif 'r' in op or 'w' in op:
    if len(initialized[addr]) > 1:
      print 'updating intersection because %s is initialized!' % addr
      C[addr].intersection_update(locks_held[thread_id])
    initialized[addr].add(thread_id)
    
    print 'rw initialized[%s]: ' % addr
    print initialized[addr]

    # if the intersection's empty and the var's been initialized, it's a problem
    if not len(C[addr]) and len(initialized[addr]) > 1:
      print 'ERROR! C[%s] is empty, lock not protecting shared resource!' % addr
      print 'intiialized[%s]' % addr
      print initialized[addr]
      sys.exit()

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
      print '\n'
      print '*'*60
      print line
      print_Cs()
      print '\n\n\n'
      process_entry(line)

if __name__ == '__main__':
  if not len(sys.argv) == 2:
    print 'Usage: eraser.py [filename]'

  run(sys.argv[1])
  print 'Success!'
