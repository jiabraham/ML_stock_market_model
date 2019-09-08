#!/usr/local/bin/python3

import sys
import nltk
import fileinput

from nltk.tokenize import sent_tokenize, word_tokenize

for line in fileinput.input():
    filtered_line=''.join([i if ord(i) < 128 else ' ' for i in line])
    tokens = word_tokenize(filtered_line)
    bigrams = list(nltk.bigrams(tokens))
    for token in tokens:
        print("%s" % (token))
    for bigram in bigrams:
        print("%s" % ('_'.join(bigram)))




