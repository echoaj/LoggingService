#!/usr/bin/env python
import json
import flask
import os
from flask import jsonify, render_template, url_for
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


@app.route('/api/logs/pretty')
def read_logs_pretty():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f.readlines():
                logs.append(json.loads(line))
    return render_template("pretty_logs.html", logs=logs)


@app.route('/api/logs/clear')
def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write('{"Welcome To": "Logger Service"}\n')
    return flask.redirect(url_for('read_logs'))


@app.route('/api/logs/pretty/clear')
def clear_pretty_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write('{"Welcome To": "Logger Service"}\n')
    return flask.redirect(url_for('read_logs_pretty'))


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
