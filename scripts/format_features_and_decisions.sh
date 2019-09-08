#!/bin/bash

set -x

cd /Users/Jojo/stock_market_project/stock_market/data/
export PATH=/Users/Jojo/stock_market_project/stock_market/project/scripts:/usr/local/bin:$\
PATH


input="features"
while read features
do

    fgrep -w -f ../../features.0807.txt new_articles_sent.filtered.tokenized.txt | sort -u\
											> new_articles_sent.features.txt
    #store the feat(words)

    cd /Users/Jojo/stock_market_project/stock_market/data/ #date/
    #get the positive or negative signal from date directory

    #concat and put into final format for npz
    #one_hot() ?

done < ${input}
