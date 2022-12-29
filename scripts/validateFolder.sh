#!/bin/bash

directory=/Users/pllaurado/nhs/repositories/xml-test-data/output

counter=0

for entry in "$search_path"${directory}/*
do


    python3 validate_xml.py file-path=$entry

    counter=$((counter+1))
    if (( $counter % 10 == 0 ))
    then
      sleep 1
    fi

done
