#!/bin/bash

set -x

cd /Users/Jojo/stock_market_project/stock_market/data/
export PATH=/Users/Jojo/stock_market_project/stock_market/project/scripts:/usr/local/bin:$PATH


input="all_feats"
while read feats_to_process
do
    cd ${feats_to_process}

    cat new_articles_sent.filtered.tokenized.txt | check_vocabulary.py -v /Users/Jojo/stock_market_project/stock_market/data/features.0807.txt  | sort -u > new_articles_sent.features.txt
    
    cd /Users/Jojo/stock_market_project/stock_market/data/
    
done < ${input}



