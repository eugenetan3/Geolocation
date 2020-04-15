import flask
import time
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import json


app = flask.Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/post-requests", methods=['GET', 'POST'])
def post_request(comments=[]):
    #if request.method == "GET":
    #    return render_template("post_requests.html", comments=comments)
    #data = request.get_json()
    #comments.append(data)
    #return redirect(url_for('post-requests')

    print(request.is_json)
    data = request.get_json()
    comments.append(data)
    print(comments)

    if request.method == "GET":
        return render_template("index.html", comments=comments)
    return 'Valid JSON request received!'
    #return jsonify(data)
    #return render_template('post_requests.html', post=data)



@app.route("/json-post-requests", methods=['GET','POST'])
def json_request():
    req_data = request.get_json(force=True)
    longitude = req_data['longitude']
    latitude = req_data['latitude']
    direction = req_data['direction']
    speed = req_data['speed']
    return '''
            Longitude: {}
            Latitude: {}
            Direction: {}
            Speed: {}'''.format(longitude, latitude, direction, speed)

if __name__ == '__main__':
    app.run(debug=True)
