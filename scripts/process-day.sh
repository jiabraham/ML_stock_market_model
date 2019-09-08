#!/bin/bash

set -x

cd /Users/Jojo/stock_market_project/stock_market/data/
export PATH=/Users/Jojo/stock_market_project/stock_market/project/scripts:/usr/local/bin:$PATH

for cdate in 2019-*
do

    cd $cdate
    for file in *_urls
    do
	dir=${file%_urls}
	cat $dir/new_articles_sent.txt.${cdate} | filter_common_sentences.py -c ../stock_corpus.sorted | perl -pe 's/\s*\- MarketWatch\s*/\n/;' | egrep -v "Published:.*ET" > $dir/new_articles_sent.filtered.txt
	cat $dir/new_articles_sent.filtered.txt | nltk_test.py > $dir/new_articles_sent.filtered.tokenized.txt
        cat $dir/new_articles_sent.filtered.tokenized.txt | add_decision.py -d decision > $dir/new_articles_sent.filtered.tokenized.dec.txt
    done
    cd ..
done




