#!/bin/bash
url="$1/api/admin/settings/:CVMConf";
dvnCvmConfSetting=$(curl -Ls $url)
# echo $dvnCvmConfSetting
cvmConfStatus=$(echo $dvnCvmConfSetting| jq '. | select(.status == "OK")')
# echo $cvmConfStatus
if [[ "$cvmConfStatus" == "" ]]; then
    echo "$url NOT FOUND."
    #do something here, eq upload a new one.
    exit
fi
#Get the element value of data.message
dvnCvmConf=$(echo $dvnCvmConfSetting | jq '.data.message')
# echo $dvnCvmConf
#Remove all \n and \"
dvnCvmConfClean=`echo $dvnCvmConf | sed 's/[\][n]//g' | sed 's/\\\//g' | sed 's:^.\(.*\).$:\1:'`
# echo $dvnCvmConfClean

#TODO: validate $dvnCvmConfClean

#Create a pretty-print json file
echo $dvnCvmConfClean | jq . > cvm-setting.json

# inputJson=""
if [[ "$2" =~ ^http* ]]; then
    inputJsonFromUrl=$(curl -Ls $2)
    exit
    #TODO: Validate $inputJsonFromUrl
    echo $inputJsonFromUrl > cvm-setting-from-url.json
    jq -s '[.[][]]' cvm-setting.json cvm-setting-from-url.json > cvm-setting-combined.json
else
#     inputJson=$(echo $(<$2))
    #TODO: Validate $json from file
    jq -s '[.[][]]' cvm-setting.json $2 > cvm-setting-combined.json
fi

if jq -e . >/dev/null 2>&1 < cvm-setting-combined.json; then
    echo "Parsed JSON successfully"
else
    echo "Failed to parse JSON"
fi


# cvmConf=`echo $dvnCvmConf | sed 's/[\][n]//g' | sed 's/\\\//g' | sed 's:^.\(.*\).$:\1:'`
# json1=$(for row in $(echo "${cvmConf}" | jq -r '.[] | @base64'); do _jq() { echo ${row} | base64 --decode;   }; echo $(_jq); echo -n ",";done)
# if jq -e . >/dev/null 2>&1 <<<"$json1"; then
#     echo "Parsed JSON successfully"
# else
#     echo "Failed to parse JSON"
# fi

