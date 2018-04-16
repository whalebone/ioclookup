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
    hits = post("http://{}:{}/iocs/_search".format(environ["ELASTICSEARCH_HOST"], environ["ELASTICSEARCH_PORT"]), data=str(data_post)).json()
    if environ["DEBUG"]:
        with open("hits.txt", "w") as file:
            file.write(str(hits))


    ioc_data_dict = {}
    for ioc in hits["hits"]["hits"]:
        if "accuracy" in ioc["_source"]:
            acc_data = ioc["_source"]["accuracy"]
            if type(acc_data) is dict:
                accuracy = 0
                for key in acc_data:
                    accuracy += acc_data[key]
                if accuracy in ioc_data_dict:
                    date_writed = dt.strptime(ioc_data_dict[accuracy]["_source"]["time"]["observation"][:10], "%Y-%m-%d")
                    date_actual = dt.strptime(ioc["_source"]["time"]["observation"][:10], "%Y-%m-%d")
                    if ((date_writed - date_actual).total_seconds()) > 0:
                        continue
                ioc_data_dict[accuracy] = ioc
    if not len(ioc_data_dict):
        data = {}
    else:
        data = ioc_data_dict[max(ioc_data_dict)]



    response = app.response_class(response=dumps(data), status=200, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

