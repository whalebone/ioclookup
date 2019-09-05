from flask import Flask, request
from json import dumps
from requests import post
from os import environ
from datetime import datetime as dt
app = Flask(__name__)


@app.route('/')
def elasticsearch_ioc():
    domain = request.args.get('domain', '')
    if not domain:
        return app.response_class(status=404, mimetype='application/json')
    data_post = {
              "query": {
                "match": {
                  "source.fqdn": domain
                }
              }
            }
    hits = post("http://{}:{}/{}/_search".format(environ["ELASTICSEARCH_HOST"], environ["ELASTICSEARCH_PORT"], environ["ELASTICSEARCH_INDEX"]), data=dumps(data_post)).json()
    for ioc in hits["hits"]["hits"]:
        try:
            del ioc["_source"]["raw"]
        except KeyError:
            pass
    if environ["DEBUG"]:
        with open("hits.txt", "w") as file:
            file.write(str(hits))
    ioc_data = [ioc["_source"] for ioc in hits["hits"]["hits"]]
    response = app.response_class(response=dumps(ioc_data), status=200, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

