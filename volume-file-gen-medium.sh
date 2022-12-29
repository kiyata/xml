declare -a mediumOrgs=("RFF" "R1H" "RDD" "RC1" "RQ3" "RXL" "RMC" "RAE" "RXH" "RXQ" "RWY" "RGT" "RQM" "RFS" "RLN" "RJR" "RXP" "RJ6" "RN7" "RP5" "RBD" "RWH" "RJN" "RVV" "RXR")

for org in "${mediumOrgs[@]}"
do
   echo "Generating data for $org"
   python activity-xml-generator.py random CSOP "${org}" --overr-config vp/config-medium.json --activities  79455  --month M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12
done