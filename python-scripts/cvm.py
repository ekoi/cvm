from flask import Flask, request, Response
import requests
import os
import json
import urllib3, io

app = Flask(__name__)

http = urllib3.PoolManager()

@app.route("/v1")
def cv():
    #apiurl = "%s/%s" % (os.environ["APIHOST"], "v1/Vocabulary")
    apiurl = "http://vocabularies.cessda.eu/v1/Vocabulary"
    response = Response(requests.get(apiurl), mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/getcv")
def getcv():
    d = ["TopicClassification", "TimeMethod", "AnalysisUnit"]
    voc = {}
    voc['vocab'] = d
    response = Response(json.dumps(voc), mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/cvlist")
def cvlist():
    #apiurl = "%s/%s" % (os.environ["APIHOST"], "v1/Vocabulary")
    apiurl = "https://vocabularies.cessda.eu/v1/vocabulary"
    #return (requests.get(apiurl).text)
    data = json.loads(requests.get(apiurl).text)
    response = Response(json.dumps(data), mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    items = []
    for voc in data['DDI']:
        items.append(voc)
    return Response(json.dumps(items), mimetype='application/json')

@app.route("/", methods=['GET', 'POST'])
def cvmanager():
    keyword = request.args.get("q")
    c = request.args.get("code")
    if keyword == 'cvmm-dataverse':
        json_data = create_json_cvm_dataverse(c)
        response = Response(json_data, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    elif keyword == 'cvmm-git':
        json_data = create_json_cvmm(c)
        response = Response(json_data, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    elif keyword == 'CESSDA':
        vocabulary = ''
        if request.args.get("voc"):
            vocabulary = request.args.get("voc")
        else:
            vocabulary = "AnalysisUnit"
            vocabulary = "TimeMethod"

        apienvurl = "v1/suggest/Vocabulary/%s/version/1.0/language/en/limit/10/query/%s" % (vocabulary,c)
        #apiurl = "%s/%s" % (os.environ["APIHOST"], apienvurl)
        apiurl = "%s/%s" % ("http://vocabularies.cessda.eu", apienvurl)
        data = json.loads(requests.get(apiurl, verify=False).text)
        data['vocab'] = vocabulary
        response = Response(json.dumps(data), mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    default_json = {}
    response = Response(default_json, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def create_json_cvmm(code):
    r = http.request('GET', "https://raw.githubusercontent.com/ekoi/speeltuin/master/resources/CMM_Custom_MetadataBlock.tsv")
    d = r.data.decode('utf-8')
    s = io.StringIO(d)

    cvmm_json_result = {}
    cv_json = []
    start_cvm = False

    for line in s:
        if start_cvm:
            # print(line)
            abc = line.split('\t')
            o_obj = {}
            # print(abc[3])

            if code is None:
                cv_json.append(create_cmm_element(abc[3],abc[2],abc[2],abc[2]))

            elif code in abc[3]:
                cv_json.append(create_cmm_element(abc[3],abc[2],abc[2],abc[2]))


        if line.startswith('#controlledVocabulary'):
            start_cvm = True

    cvmm_json_result['listOfCodes'] = cv_json
    json_data = json.dumps(cvmm_json_result)

    return json_data

def create_json_cvm_dataverse(code):
    r = http.request('GET', "https://raw.githubusercontent.com/ekoi/speeltuin/master/resources/CMM_Custom_MetadataBlock.tsv")
    d = r.data.decode('utf-8')
    s = io.StringIO(d)

    cvmm_json_result = {}
    cv_json = []
    start_datasetfield = False

    for line in s:
        if line.startswith('#controlledVocabulary'):
            start_datasetfield = False
        if start_datasetfield:
            # print(line)
            abc = line.split('\t')
            o_obj = {}

            if code is None:
                cv_json.append(create_cmm_element(abc[16],abc[2],abc[2],abc[2]))

            elif code in abc[16]:
                cv_json.append(create_cmm_element(abc[16],abc[2],abc[2],abc[2]))

        if line.startswith('#datasetField'):
            start_datasetfield = True

    cvmm_json_result['listOfCodes'] = cv_json
    json_data = json.dumps(cvmm_json_result)

    return json_data

def create_cmm_element(u, c, pl, lpl):
    o_obj = {}
    o_obj['url'] = {'type': 'uri', 'value': u}
    o_obj['code'] = {'type': 'literal', 'value': c}
    o_obj['prefLabel'] = {'type': 'literal', 'value': pl}
    o_obj['languagePrefLabel'] = {'type': 'literal', 'value': lpl}
    o_obj['language'] = {'type': 'literal', 'value': 'en'}
    return o_obj

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9266)
