#!/usr/local/bin/python3
# coding: utf-8

import sys, getopt
from bs4 import BeautifulSoup


def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"i:",["ifile="])
   except getopt.GetoptError:
      print('html2text.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('html2text.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print('Input file is %s' % (inputfile))
   original = open(inputfile, newline='')
   article = original.read()
   soup = BeautifulSoup(article, 'html.parser')

   # kill all script and style elements
   for script in soup(["script", "style"]):
       script.extract()    # rip it out

   # get text
   text = soup.get_text()
    
   # break into lines and remove leading and trailing space on each
   lines = (line.strip() for line in text.splitlines())
   # break multi-headlines into a line each
   chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
   # drop blank lines
   text = "JOJOSEP".join(chunk for chunk in chunks if chunk)

   print("%s" % (text.encode('utf-8')))
   original.close()

if __name__ == "__main__":
   main(sys.argv[1:])





