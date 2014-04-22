#!/usr/bin/python

import sys
import os
import re
import BeautifulSoup as bs
import urllib2
from lxml import etree

triggerTerms = ['net', 'IPV4', 'IPV6', 'NETFILTER', 'tcp', 'RTNETLINK',
                'bridge', 'wireless', 'PKT_SCHED']

GMANE_SEARCH = 'http://search.gmane.org/?query=%s'

class Entry():
  '''
  Represents an entry in a changelog file
  '''
  # xpath selector for first link in gmane search response
  self.gmane_xpath = '//*[@id="mform"]/dl[1]/dt/b/a'

  def __init__(self, entry_lines):
    self.add_entry(entry_lines)
  
  def add_entry(self, entry_lines):
    self.email = entry_lines[0]
    self.title = entry_lines[1]
    self.body  = entry_lines[2:]

  def get_address(self):
    try:
      query = GMANE_SEARCH % urllib2.quote(self.title)
      response = urllib2.urlopen(url)
      htmlparser = etree.HTMLParser()
      tree = etree.parse(response, htmlparser)
      elem = tree.xpath(xpathselector)
      link = elem[0].attrib['href']
      self.address = link
      return true
    except Exception as e:
      print 'Error getting address for patch %s: %s' % (self.title, e)
      return false

def line_is_start(line):
  '''
  determine starting line of changelog patch by finding email addr
  in std format
  '''
  return len(re.findall('<*@*.*>', line)) > 0

def parse_changelog_entries(lines):
  '''
  loop over changelog lines and parse into 
  list of changelog entries
  '''
  entries = []
  start = -1
 
  # Add entries
  for i in range(len(lines)):
    if line_is_start(lines[i]):
      if start > 0:
        entries.append(Entry(lines[start:i]))
      start = i
  
  return entries 

def main(changelog):
  lines = []
  
  with open(changelog, 'r') as fp:
    lines = fp.readlines()
  
  entries = parse_changelog_entries(lines)
  
  
