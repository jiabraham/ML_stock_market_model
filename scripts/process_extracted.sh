#!/bin/bash

set -x

cd /Users/Jojo/stock_market_project/stock_market/data/
export PATH=/Users/Jojo/stock_market_project/stock_market/project/scripts:/usr/local/bin:$PATH


input="dirs_to_process"
while read dir_to_process
do
    cd ${dir_to_process}

    last_dir=`cat /Users/Jojo/stock_market_project/stock_market/data/latest`

    last_price=`cat /Users/Jojo/stock_market_project/stock_market/data/$last_dir/extracted_price`

    current_price=`cat extracted_price`

    delta=`echo "${current_price} - ${last_price}" | perl -pe 's/,//g;' | bc -l`

    echo "Delta = "${delta}

    change="-"
    if (( $(echo "$delta > 0" | bc -l) ));  then change="+"; fi

    echo ${delta} > delta
    echo ${change} > decision

    echo ${dir_to_process} > /Users/Jojo/stock_market_project/stock_market/data/latest
    
    cd ..
done < ${input}




