from flask import Flask, request, Response
import requests
import os
import json

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8091)
