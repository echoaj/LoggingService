#!/usr/bin/env python
import json
import flask
import os
from flask import jsonify, render_template
from io import StringIO
import flask_cors

app = flask.Flask(__name__)
flask_cors.CORS(app, resources={r'/api/*': {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

PATH = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PATH, 'logs')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/logs')
def read_logs():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f.readlines():
                logs.append(json.loads(line))
    return jsonify(logs)


@app.route('/api/logger', methods=['GET', 'POST'])
def logger():
    result = flask.request.json
    buffer = StringIO()
    json.dump(result, buffer)
    buffer.write('\n')
    with open(LOG_FILE, 'a') as f:
        f.write(buffer.getvalue())
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
