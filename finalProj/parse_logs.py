#!/usr/bin/python

import sys
import os
import re
from bs4 import BeautifulSoup
import urllib2
from lxml import etree

triggerTerms = ['net', 'IPV4', 'IPV6', 'NETFILTER', 'tcp', 'RTNETLINK',
                'bridge', 'wireless', 'PKT_SCHED', 'SCTP', 'PPPOE', 'DECNET',
                'NETLINK', 'IPX', 'ECONET', 'netdrvr', 'PKTGEN', 'network',
                'IPSEC','Ethernet', 'AF_PACKET', 'vlan', 'wan', 'lan', 'router',
                'net_sched', 'af_unix', 'ipvs']

GMANE_SEARCH = 'http://search.gmane.org/?query=%s'

class Entry():
  '''
  Represents an entry in a changelog file
  '''
  # xpath selector for first link in gmane search response
  gmane_xpath = '//*[@id="mform"]/dl[1]/dt/b/a'

  def __init__(self, entry_lines):
    self.add_entry(entry_lines)
 
  def __str__(self):
    #return ('%s\n\t<a href="%s">%s</a>\n\t%s\n\t%s\n\n') % (self.email,
    #  self.address, self.title, self.target_files, self.body)
    
    target = ','.join(self.stats['files'])
    return ('=HYPERLINK("%s","%s")\t%s' + ' \t'*8 + ('%s\t'*3)+ '%s\n') % (self.address,
      self.title, 
      target, 
      self.stats['files_changed'], 
      self.stats['insertions'],
      self.stats['deletions'], 
      self.body)

  def add_entry(self, entry_lines):
    self.email = entry_lines[0].strip()
    self.title = entry_lines[1].strip()
    self.body  = ' '.join(entry_lines[2:])
    self.body = re.sub('\s+', ' ', self.body)
    self.address = ''
    if not self.get_address():
      return False
    self.target_page = self.get_comment_page()
    self.get_stats(self.target_page)
    return True

  def get_address(self):
    if not hasattr(self, 'email'):
      print 'Error, have not created Entry yet!'
      return False
    
    url = GMANE_SEARCH % urllib2.quote(self.title)
    tries = 0
    while tries < 3:
      try:
        response = urllib2.urlopen(url)
        break
      except:
        tries += 1
    if tries == 3:
      print 'Failed to fetch address for %s' % self.title
      return False
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    elem = tree.xpath(self.gmane_xpath)
    try:
      link = elem[0].attrib['href']
    except:
      return False
    self.address = link
    return True

  def get_comment_page(self):
    '''
    returns comment page (from self.address) 
    in text format
    '''
    #TODO: error checking and retries!
    # If self.address isn't here, retry self.get_address
    url = self.address
    response = urllib2.urlopen(url)
    html = response.read()
    bs = BeautifulSoup(html)
    return bs.text
  
  def get_stats(self, comment_page):
    '''
    Takes comment page in text format, saves file edited.
    self.stats is saved in form of 
    '''
    self.stats = {}
    
    try:
      self.stats['files_changed'] = re.findall('(\d+) files changed', comment_page)[0]
    except:
      self.stats['files_changed'] = '0'
    try:
      self.stats['insertions'] = re.findall('(\d+) insertions?\(\+\)', comment_page)[0]
    except:
      self.stats['insertions'] = '0'
    try:
      self.stats['deletions'] = re.findall('(\d+) deletions?\(-\)', comment_page)[0]
    except:
      self.stats['deletions'] = '0'
    try:
      self.stats['files'] = re.findall('--- a(\S+)\s', comment_page)
    except:
      self.stats['files'] = ' '
  
def line_is_start(line):
  '''
  determine starting line of changelog patch by finding email addr
  in std format
  '''
  return len(re.findall('^<\S+@\S+\.\S+>', line)) > 0

def should_add(title):
  '''
  Return true if any of our trigger terms is in the title
  '''
  for term in triggerTerms:
    if term.lower() in title.lower():
      return True
  return False

def parse_changelog_entries(output_file, lines):
  '''
  loop over changelog lines and parse into 
  list of changelog entries
  '''
  entries = []
  start = -1
 
  # Add entries
  for i in range(len(lines)):
    #print 'line %d: %s' % (i, lines[i])
    if line_is_start(lines[i]):
      #print 'line is start line, start=%d' % i
      if start > 0:
        print 'Considering entry with title: %s' % lines[start+1]
        if should_add(lines[start+1]):
          print 'Adding it now: '
          entry = Entry(lines[start:i])
          entries.append(entry)
          output_file.write(str(entry))
          print entry
        else:
          print 'Did not add'
        
        print '*'*80

        ##TODO: delete after debug
        #if len(entries) == 4:
        #  return entries
      start = i
  
  return entries 

def main(changelog):
  lines = []
  
  with open(changelog, 'r') as fp:
    lines = fp.readlines()
 
  with open('%s.output' % changelog, 'w') as output_file:
    entries = parse_changelog_entries(output_file, lines)

if __name__ == '__main__':
  main(sys.argv[1])
