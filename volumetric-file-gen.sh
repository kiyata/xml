helpFunction()
{
   echo ""
   echo "Usage: volumetric-file-gen.sh -f OP -c 79 -a 1500 -t large.txt -m M01,M05"
   echo -e "\t-f Feed type, e.g. OP, CSAPC"
   echo -e "\t-c Cost count by activity"
   echo -e "\t-a Number of activities"
   echo -e "\t-t File containing list of trusts"
   echo -e "\t-m Months for which files should be generated. M01-m12 is default if not provided"
}

while getopts "f:c:a:t:m:" opt
do
   case "$opt" in
      f ) feedType="$OPTARG" ;;
      c ) costCount="$OPTARG" ;;
      a ) activityCount="$OPTARG" ;;
      t ) trustFile="$OPTARG" ;;
      m ) months="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [[ -z "$feedType" ]] || [[ -z "$costCount" ]] || [[ -z "$activityCount" ]] || [[ -z "$trustFile" ]]
then
   echo "Some or all required parameters are missing";
   helpFunction
else

if [ -z "$months" ]
then
   months = "M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12"
fi
# Begin script in case all parameters are correct
echo "Feed type     : ${feedType}"
echo "Cost/activity : ${$costCount}"
echo "Activity count: ${$activityCount}"
echo "Trust file    : ${trustFile}"
echo "Months        : ${months}"

# create json config file
cp template.json config.json
sed -i "s/COST/$cost/g" config.json

#trusts=`cat ${trustFile}`
#for trust in $trusts; do
#  echo "Generating data for ${trust}"
#  python ../activity-xml-generator.py random "${feedType}" "${trust}" --overr-config config.json --activities "${activities}" --month "${months}"
#done


#readme
#./volume-file-gen.sh CSOP 76 1000 large-trusts.txt 3
#large: 1,051,964, cost 76
#medium: 953,460, cost 49
#months: M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12
fi