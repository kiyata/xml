#declare -a largeOrgs=("OR1" "OR2" "RBS" "RTK" "RF4")
declare -a largeOrgs=("RTK" "RF4")
for org in "${largeOrgs[@]}"
do
   echo "Generating data for $org"
   python activity-xml-generator.py random CSOP "${org}" --overr-config vp/config-large.json --activities  87664 --month M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12
done