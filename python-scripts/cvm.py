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
    if keyword == 'cvmm':
        c = request.args.get("code")
        json_data = create_json_cvmm(c)
        response = Response(json_data, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    vocabulary = ''
    if request.args.get("voc"):
        vocabulary = request.args.get("voc")
    else:
        vocabulary = "AnalysisUnit"
        vocabulary = "TimeMethod"

    apienvurl = "v1/suggest/Vocabulary/%s/version/1.0/language/en/limit/10/query/%s" % (vocabulary, keyword)
    #apiurl = "%s/%s" % (os.environ["APIHOST"], apienvurl)
    apiurl = "%s/%s" % ("http://vocabularies.cessda.eu", apienvurl)
    data = json.loads(requests.get(apiurl, verify=False).text)
    data['vocab'] = vocabulary
    response = Response(json.dumps(data), mimetype='application/json')
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
            print(abc[3])

            if code is None:
                o_obj['url'] = {'type': 'uri', 'value': abc[3]}
                o_obj['code'] = {'type': 'literal', 'value': abc[2]}
                o_obj['prefLabel'] = {'type': 'literal', 'value': abc[2]}
                o_obj['languagePrefLabel'] = {'type': 'literal', 'value': abc[2]}
                o_obj['language'] = {'type': 'literal', 'value': 'en'}

                cv_json.append(o_obj)

            elif code in abc[3]:

                o_obj['url'] = {'type': 'uri', 'value': abc[3]}
                o_obj['code'] = {'type': 'literal', 'value': abc[2]}
                o_obj['prefLabel'] = {'type': 'literal', 'value': abc[2]}
                o_obj['languagePrefLabel'] = {'type': 'literal', 'value': abc[2]}
                o_obj['language'] = {'type': 'literal', 'value': 'en'}

                cv_json.append(o_obj)

        if line.startswith('#controlledVocabulary'):
            start_cvm = True

    cvmm_json_result['controlledVocabulary'] = cv_json
    json_data = json.dumps(cvmm_json_result)

    return json_data

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9266)
