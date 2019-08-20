#!/usr/local/bin/python3

from __future__ import absolute_import, division, print_function, unicode_literals

import fileinput
import getopt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import tensorflow as tf
from   tensorflow import keras
from   tensorflow import feature_column
from   tensorflow.keras import layers
from   sklearn.model_selection import train_test_split
from tensorflow import contrib


tfe = contrib.eager

print(tf.__version__)

MAX_REC_LENGTH=1918
EMBEDDING_DIMENSION=16

def read_vocabulary(filename):
    vocabulary = {}
    vocinput = fileinput.input(filename)
    for index, line in enumerate(vocinput, start=1):
        line = line.strip()
        vocabulary[line] = index
    vocinput.close()
    return vocabulary  

def read_features(filename, vocabulary):
    event = np.full(MAX_REC_LENGTH, 0)
    features_input = fileinput.input(filename)
    for ind, line in enumerate(features_input):
        line = line.strip()
        if line in vocabulary and ind < MAX_REC_LENGTH:
            event[ind] = vocabulary[line]
    features_input.close()
    return event

def read_decision(filename):
    dec_input = fileinput.input(filename)
    dec = ""
    for line in dec_input:
        dec = line.strip()
    dec_input.close()
    return dec

def read_corpus(filename, vocabulary):
    # We assume that the decision file is 2 directories above the feature file
    corpus = []
    decisions = []
    corpusinput = fileinput.FileInput(filename)
    for line in corpusinput:
        line = line.strip()
        (hist, fut) = line.split(' ')
        arr = hist.split('-')
        date = "%s-%s-%s" % (arr[0], arr[1], arr[2])
        decision_file = "%s/decision" % (fut)
        features_file = "%s/%s/new_articles_sent.features.txt" % (hist, date)
        event = read_features(features_file, vocabulary)
        corpus.append(event)
        decision = read_decision(decision_file)
        if decision == '+':
            decisions.append([1])
        else:
            decisions.append([0])
    corpus = pd.DataFrame.from_records(corpus, columns=["features"]*1918)
    decisions = pd.DataFrame.from_records(decisions, columns=["decisions"])
    print(corpus.describe())
    print(decisions.describe())
    return corpus, decisions


def get_compiled_model(vocabulary_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocabulary_size, EMBEDDING_DIMENSION),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model


def main(argv):
   corpus = ''
   try:
       opts, args = getopt.getopt(argv,"hc:v:",["corpus=", "vocabulary="])

   except getopt.GetoptError:
       print('stock_market_model.py -c corpus_file -v vocabulary')
       sys.exit(2)

   corpusfile = ""
   vocabfile = ""
   for opt, arg in opts:
      if opt == '-h':
          print('stock_market_model.py -c <corpus_file> -v <vocabulary>')
          sys.exit()
      elif opt in ("-c", "--corpus"):
          corpusfile = arg
      elif opt in ("-v", "--vocabulary"):
          vocabfile = arg

   if not vocabfile:
       print ("Must specify a vocabulary file!!");
       return -1

   pd.set_option('display.max_columns', 30);
   pd.set_option('display.max_rows', 10);
   vocabulary = read_vocabulary(vocabfile)
   (corpus, decisions) = read_corpus(corpusfile, vocabulary)
   dataset = corpus.merge(decisions, left_index=True, right_index=True)
   print(dataset.head(5))

   target = dataset.pop("decisions")
   tfdataset = tf.data.Dataset.from_tensor_slices((dataset.values, target.values))

   dataset_len = len(dataset)
   train_size = int(0.7 * dataset_len)
   val_size = int(0.15 * dataset_len)
   test_size = int(0.15 * dataset_len)

   #Run this 10000 times and see what the averages come out to be 
   total_accuracy = {}
   total_loss = {}
   # keep results for plotting
   test_loss_results = []
   test_accuracy_results = []
   
   for test_number in range (0, 1):

       full_dataset = tfdataset.shuffle(dataset_len)
       train_dataset = full_dataset.take(train_size)
       test_dataset = full_dataset.skip(train_size)
       val_dataset = test_dataset.skip(val_size)
       test_dataset = test_dataset.take(test_size)


       num_epochs = 100
       model = get_compiled_model(len(vocabulary)+1)   
       model.summary()

       history = model.fit(train_dataset, epochs=num_epochs)
   
       print('\n# Evaluate on test data')
       results = model.evaluate(test_dataset)

       print('test loss, test acc:', results)
       test_accuracy_results.append(results[1])
       test_loss_results.append(results[0])
       
       total_accuracy[test_number] = results[1]
       total_loss[test_number] = results[0]

   # average_accuracy = float(total_accuracy)
   # average_loss = float(total_loss)
   for test_number in range(0, 1):
       print(total_accuracy[test_number])

   for test_number in range(0, 1):
       print(total_loss[test_number])
   
   plt.plot(history.history['acc'])
   plt.plot(history.history['loss'])
   plt.plot(test_accuracy_results,'bo')
   plt.plot(test_loss_results,'r+')
   
   plt.title('model accuracy')
   plt.ylabel('accuracy')
   plt.xlabel('epoch')
   plt.legend(['acc', 'loss', 'test-acc', 'test-loss'], loc='upper right')
   plt.show()

   
   return

if __name__ == "__main__":
    main(sys.argv[1:])
