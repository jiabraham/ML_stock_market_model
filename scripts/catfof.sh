#!/bin/bash

while read line
do
    echo -n $line": "
    cat $line
done < "${1:-/dev/stdin}"

