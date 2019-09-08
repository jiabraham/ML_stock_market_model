#!/bin/bash

while read line
do
    echo -n $line": "
    cat $line | wc -l
done < "${1:-/dev/stdin}"

