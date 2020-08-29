#!/bin/bash
url="$1/api/admin/settings/:CVMConf";
echo "Retrieving setting from $url"
dvnCvmConfSetting=$(curl -Ls $url)
# echo $dvnCvmConfSetting
cvmConfStatus=$(echo $dvnCvmConfSetting| jq '. | select(.status == "OK")')
# echo $cvmConfStatus
if [[ "$cvmConfStatus" == "" ]]; then
    echo "$url NOT FOUND."
    #do something here, eq upload a new one.
    exit
else
    echo "Status is OK"
fi
#Get the element value of data.message
dvnCvmConf=$(echo $dvnCvmConfSetting | jq '.data.message')
# echo $dvnCvmConf
#Remove all \n and \"
dvnCvmConfClean=`echo $dvnCvmConf | sed 's/[\][n]//g' | sed 's/\\\//g' | sed 's:^.\(.*\).$:\1:'`
# echo $dvnCvmConfClean

#TODO: validate $dvnCvmConfClean

#Create a pretty-print json file
# echo $dvnCvmConfClean | jq . > cvm-setting.json

#Get all aci's key
acis=$(echo $dvnCvmConfClean | jq '.[].aci')
# echo $acis

echo "Retrieving json from $2"
# inputJson=""
if [[ "$2" =~ ^http* ]]; then
    inputJsonFromUrl=$(curl -Ls $2)
    #TODO: Validate $inputJsonFromUrl
    aciFromUrl=$(echo $inputJsonFromUrl | jq '.[].aci')
#     echo $aciFromUrl

    #TODO: Refactoring using function to prevent repeating code
    echo "Checking for any duplicate"
    for i in $acis
    do
        for j in $aciFromUrl
        do
           if [[ $i == $j ]]; then
               echo "ERROR Duplicate aci found: $j"
               exit
           fi
        done
    # echo $i;
    done
    echo "No duplicate found. Write the json from $2 to cvm-setting-from-url.json"
    echo $inputJsonFromUrl > cvm-setting-from-url.json
    echo "Write the combined json to cvm-setting-combined.json"
    jq -s '[.[][]]' cvm-setting.json cvm-setting-from-url.json > cvm-setting-combined.json
else
    inputJsonFromFile=$(echo $(<$2))
    #TODO: Validate $json from file
    aciFromFile=$(echo $inputJsonFromFile | jq '.[].aci')
#     echo $aciFromFile

    #TODO: Refactoring using function to prevent repeating code
    echo "Checking for any duplicate"
    for i in $acis
        do
            for j in $aciFromFile
            do
               if [[ $i == $j ]]; then
                   echo "ERROR Duplicate aci found: $j"
                   exit
               fi
            done
        # echo $i;
        done
    echo "No duplicate found."
    echo "Write the combined json to cvm-setting-combined.json"
    jq -s '[.[][]]' cvm-setting.json $2 > cvm-setting-combined.json
fi

if jq -e . >/dev/null 2>&1 < cvm-setting-combined.json; then
    echo "Parsed JSON successfully"
    echo "Uploading cvm-setting-combined.json"
    #Push to the server
    uploadedResult=$(curl -H "Content-Type: application/json" -X PUT --data-binary @cvm-setting-combined.json "$1/api/admin/settings/:CVMConf")
    echo $uploadedResult | jq .
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

