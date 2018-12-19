#!/usr/bin/env python3
import flask
from datetime import datetime as time


app = flask.Flask(__name__)


@app.route('/')
def index():
    return "acssce time:"+str(time.now())+'\n'

@app.route('/req', methods=['POST'])
def req():

    
    d = {
        "request_id": "mishima-afdce59f-00cc-48ee-bf44-7d7523e0af7",
        "url": "http://example.com/ad/image/123",
        "price" : 50
    }
    
    return flask.jsonify(d)


@app.route('/win', methods=['POST'])
def win():
    d = {
        "rewult":"ok"
        }

    return flask.jsonify(d)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

