#!/bin/bash

#python3 random_data_generator.py feed-type=EC organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#python3 random_data_generator.py feed-type=APC organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#python3 random_data_generator.py feed-type=OP organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#python3 random_data_generator.py feed-type=SI organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#python3 random_data_generator.py feed-type=SWC organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#python3 random_data_generator.py feed-type=MHCC organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#python3 random_data_generator.py feed-type=MHPS organisation=ORG01 n-activities=10 config-file=resources/configs/config.json
#
#
#declare -a allFeedTypes=("EC" "APC" "OP" "SWC" "SI" "MHCC" "MHPS" "IAPT" )
#declare -a organisations=("ORG01" "ORG02" "ORG99")
#declare -a months=("M01" "M02" "M03" "M04" "M05" "M06" "M07" "M08" "M09" "M10" "M11" "M12")
#declare -r n_activities=100
#
## Read the array values with space
#for month in "${months[@]}"; do
#	 for org in "${organisations[@]}"; do
#	   	 for feed in "${allFeedTypes[@]}"; do
#          python3 random_data_generator.py feed-type=${feed} n-activities=${n_activities} organisation=${org} month=${month} config-file=resources/configs/config.json &
#       done
#   done
#   sleep 1
#done

#
## Declare a string array with type
#declare -a allFeedTypes=("APC")
#declare -a organisations=("ORG01")
#declare -a months=("M09" "M10" "M11" "M12")
#declare -r n_activities=2000
#
## Read the array values with space
#for month in "${months[@]}"; do
#	 for org in "${organisations[@]}"; do
#	   	 for feed in "${allFeedTypes[@]}"; do
#          python3 random_data_generator.py feed-type=${feed} n-activities=${n_activities} organisation=${org} month=${month} config-file=resources/configs/config.json &
#       done
#   done
#   sleep 1
#done
#

#
#declare -a allFeedTypes=("EC" "APC" "OP" "SWC" "SI" "MHCC" "MHPS" "IAPT" )
#declare -a organisations=("ORG01")
#declare -a months=("M01" "M02")
#declare -r n_activities=5
#
## Read the array values with space
#for month in "${months[@]}"; do
#	 for org in "${organisations[@]}"; do
#	   	 for feed in "${allFeedTypes[@]}"; do
#          python3 random_data_generator.py feed-type=${feed} n-activities=${n_activities} organisation=${org} month=${month} config-file=resources/configs/config.json &
#       done
#   done
#   sleep 1
#done
#
#


declare -a allFeedTypes=("AMB" )
declare -a organisations=("RRU" "RX6" "RYA" "RYC" "RYF")
declare -a months=("M01" "M02" "M03" "M04" "M05" "M06" "M07" "M08" "M09" "M10" "M11" "M12")
#declare -a months=("M01")
declare -r n_activities=1

# Read the array values with space
for month in "${months[@]}"; do
	 for org in "${organisations[@]}"; do
	    for feed in "${allFeedTypes[@]}"; do
       python3 xml-gen.py random ${feed} ${org} --activities ${n_activities}  --month ${month} --overr-config resources/samples/config-file.json &
      done
   done
   sleep 1
done


