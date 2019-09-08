#!/usr/local/bin/python3
# coding: utf-8

import fileinput
import getopt
import sys

def read_vocabulary(filename):
    vocabulary = {}
    vocinput = fileinput.input(filename)
    for index, line in enumerate(vocinput, start=1):
        line = line.strip()
        vocabulary[line] = index
    vocinput.close()
    return vocabulary  

def read_features(filename, vocabulary):
    event = []
    features_input = fileinput.input(filename)
    for line in features_input:
        line = line.strip()
        if line in vocabulary:
            event.append(line)
        else:
            event.append("unk")
    features_input.close()
    return event


def main(argv):
   inputfile = ''
   vocabfile = ''
   try:
       opts, args = getopt.getopt(argv,"hv:",["vocabulary="])
   except getopt.GetoptError:
      print('check_vocabulary.py -v <vocabfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('check_vocabulary.py -v <vocabfile>')
         sys.exit()
      if opt == '-v':
          vocabfile = arg

   vocabulary = read_vocabulary(vocabfile)
   for line in sys.stdin:
       line = line.strip()
       if line in vocabulary:
           print(line)


if __name__ == "__main__":
   main(sys.argv[1:])






