#!/bin/bash
################################################################################
# This script is used to configure a Dataverse installation from a ConfigMap.
# It is used solely for changing Database settings!
################################################################################
IFS=$'\t'
# Fail on any error
set -euo pipefail
if [ "${CVM_SERVER_NAME}" ]; then
    echo "--------hello-------------";
    echo $1;
    echo "----------end of hello-----------";
    jso_text='';
    template='{"aci":"ACI","source-name":"CESSDA", "source-url":"https://cvm.dataverse.tk","vocabs":["VOC"],"keys": ["KV","KT","KU"]}';
    json_process="";
    json_element="";
    i=0;
    string="1;2";
    id="$( cut -d ';' -f 1 <<< "$string" )";
    echo $id;
    echo $string | cut -d';' -f1 # output is 1
    echo $string | cut -d';' -f2 # output is 2
    echo "=========";
    echo "$CVM_SERVER_URL";
    echo "_________";
    while read KEY VOC OTHERS; do
      if [[ "$json_process" == "" && "$KEY" == *-cv ]]; then
        json_element=${template//VOC/$VOC};
        json_element=${json_element//ACI/$KEY};
        json_process="create"
      elif [[ "$json_process" == "create" ]]; then
        case $KEY in
         *-vocabulary ) json_element=${json_element//KV/$KEY};;
         *-term ) json_element=${json_element//KT/$KEY};;
         *-url ) json_element=${json_element//KU/$KEY};
                json_process="finish";
                ((i=i+1));;
        esac
      fi
      if [[ "$json_process" == "finish" ]]; then
        json_process="";
        if [[ i -gt 1 ]]; then
            jso_text="$jso_text, $json_element";
        else
            jso_text="$jso_text $json_element";
        fi
      fi
    done < $1
    jso_text="[$jso_text]";
    echo $jso_text > $2;
fi