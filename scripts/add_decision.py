#!/usr/local/bin/python3

import sys,getopt
import fileinput

def add_decision(decision):
  for line in sys.stdin:
      line = line.strip()
      print("%s %s" % (decision, line))
  return

def init_decision(decision_file):
  for line in fileinput.input(decision_file):
      decision = line.strip()
  return decision


def main(argv):
   decisionfile = ''
   try:
       opts, args = getopt.getopt(argv,"hd:",["decision="])
   except getopt.GetoptError:
       print('add_decision.py -d <decisionfile>')
       print('Reads input from stdin')
       sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
          print('add_decision.py -d <decisionfile>')
          print('Reads input from stdin')
          sys.exit()
      elif opt in ("-d", "--decision"):
          decisionfile = arg

   decision = init_decision(decisionfile)
   add_decision(decision)
   return

if __name__ == "__main__":
    main(sys.argv[1:])



