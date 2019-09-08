#!/bin/bash

set -x

todaysdate=`date "+%Y-%m-%d-%H-%M"`

cd /Users/Jojo/stock_market_project/stock_market/data/
mkdir ${todaysdate}
cd ${todaysdate}

export PATH=/Users/Jojo/stock_market_project/stock_market/project/scripts:/usr/local/bin:$PATH

rm latest-news*

wget https://www.marketwatch.com/latest-news

grep href latest-news | grep 2019 | grep newsviewer | perl -pe 's#^.*?href="##; s/".*$//; s/\?.*$//;' | awk '{ print $1, $1; }' | perl -pe 's/^.*?2019/2019/;' | grep '^2019' > new_stories_to_be_downloaded.txt

cat new_stories_to_be_downloaded.txt  | awk '{ file=$1"_urls"; print $2 >> file; }'

for file in *_urls
do
  dir=${file%_urls}
  mkdir $dir
  wget -i $file -O $dir/new_articles.txt
  echo "Done... "$dir
  html2text.py -i $dir/new_articles.txt | perl -pe 's/JOJOSEP/\n/g;' > $dir/new_articles_sent.txt.${todaysdate}
  cat $dir/new_articles_sent.txt.${todaysdate} | filter_common_sentences.py -c ../stock_corpus.sorted | perl -pe 's/\s*\- MarketWatch\s*/\n/;' | egrep -v "Published:.*ET" > $dir/new_articles_sent.filtered.txt
  cat $dir/new_articles_sent.filtered.txt | nltk_test.py > $dir/new_articles_sent.filtered.tokenized.txt
done


last_dir=`cat /Users/Jojo/stock_market_project/stock_market/data/latest`

last_price=`cat /Users/Jojo/stock_market_project/stock_market/data/$last_dir/extracted_price`

get_price.py | perl -pe 's/^.*?"//; s/".*$//;' >  extracted_price

current_price=`cat extracted_price`

delta=`echo "${current_price} - ${last_price}" | perl -pe 's/,//g;' | bc -l`

echo "Delta = "${delta}

change="-"
if (( $(echo "$delta > 0" | bc -l) ));  then change="+"; fi

echo ${delta} > /Users/Jojo/stock_market_project/stock_market/data/${todaysdate}/delta
echo ${change} > /Users/Jojo/stock_market_project/stock_market/data/${todaysdate}/decision

for file in *_urls
do
    dir=${file%_urls}
    cat $dir/new_articles_sent.filtered.tokenized.txt | add_decision.py -d decision > $dir/new_articles_sent.filtered.tokenized.dec.txt
    fgrep -w -f /Users/Jojo/stock_market_project/stock_market/data/features.0807.txt $dir/new_articles_sent.filtered.tokenized.txt | sort -u > $dir/new_articles_sent.features.txt
done



echo ${todaysdate} > /Users/Jojo/stock_market_project/stock_market/data/latest

echo "DataCollect_"${change}"_"${delta} | mail -s "contents" jia253@nyu.edu
