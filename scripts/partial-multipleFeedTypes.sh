#!/bin/bash
 
# Declare a string array with type
declare -a feedTypes=("AE" "APC" "OP" "SWC" "SI")
declare -r n_files=1

# Read the array values with space
for val in "${feedTypes[@]}"; do
	for i in $(seq 1 ${n_files}); do
		python3 partial_csv_data_generator.py feed-type=${val} csv-file=resources/csv-files/partial-plemi-nhsno-data.csv organisation=ORG01 &
	done
done

## Create zip file with all the xml files
# sleep 4
# compress -c output/*.xml > output/allFeedTypes_ORG01.zip