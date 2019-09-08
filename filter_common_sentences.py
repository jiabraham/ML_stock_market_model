#!/usr/local/bin/python3

import sys,getopt
import fileinput

sent_corpus = {}

THRESHOLD =  60
MIN_LENGTH = 6
MAX_LENGTH = 50

def filter_sentences():
  count_filtered = 0
  count_line_length = 0
  tot_lines = 0
  for line in sys.stdin:
      line = line.strip()
      tot_lines += 1
      filtered_line=''.join([i if ord(i) < 128 else ' ' for i in line])
      if filtered_line in sent_corpus:
          if sent_corpus[filtered_line] > THRESHOLD:
              count_filtered += 1
              continue
      line_tok_length = len(filtered_line.split())
      if line_tok_length > MAX_LENGTH or line_tok_length < MIN_LENGTH:
          count_line_length += 1
          continue
      print("%s" %(filtered_line))

  # print ("DONE: %d %d total %d" % (count_filtered, count_line_length, tot_lin\
es))
  return



def init_sentence_corpus(sentence_file):
  for line in fileinput.input(sentence_file):
      filtered_line=''.join([i if ord(i) < 128 else ' ' for i in line])
      arr = filtered_line.strip().split(' ')
      cnt = int(arr.pop(0))
      sent = " ".join(arr)
      sent_corpus[sent] = cnt
  return
  
def init_sentence_corpus(sentence_file):
  for line in fileinput.input(sentence_file):
      filtered_line=''.join([i if ord(i) < 128 else ' ' for i in line])
      arr = filtered_line.strip().split(' ')
      cnt = int(arr.pop(0))
      sent = " ".join(arr)
      sent_corpus[sent] = cnt
  return
  
def main(argv):
   corpusfile = ''
   try:
       opts, args = getopt.getopt(argv,"hc:",["corpus="])
   except getopt.GetoptError:
       print('filter_common_sentences.py -c <corpusfile>')
       print('Reads input from stdin')
       sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
          print('filter_common_sentences.py -c <corpusfile>')
          print('Reads input from stdin')
          sys.exit()
      elif opt in ("-c", "--corpus"):
          corpusfile = arg

   init_sentence_corpus(corpusfile)
   filter_sentences()
   return
   
if __name__ == "__main__":
    main(sys.argv[1:])

