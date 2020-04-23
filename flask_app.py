import flask
import time
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import json
##
import mysql.connector

app = flask.Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/post-requests", methods=['GET', 'POST'])
def post_request(comments=[]):
##

    mydb = mysql.connector.connect(host="ix-dev.cs.uoregon.edu", user="eugenet", passwd="password", database="my_db", port="3226")
    mycursor = mydb.cursor()

    #add_data = ("INSERT INTO locationdata "
    #           "(id, data) "
    #           "VALUES (%s, %s)")

    add_data = ("INSERT INTO locationdata2 "
               "(id, user_id, longitude, latitude, speed, timestamp, time_spent) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")


##
    data = request.get_json()
    comments.append(data)
    #comments.append(mydb.is_connected())
    if (data != None):
        userid = data['User ID']
        longitude = data['Longitude']
        latitude = data['Latitude']
        speed = data['Speed']
        date = data['Date']
        time_spent = data['Time Spent']

        #mysqldata = ('0', str(data))
        mysqldata = ('0', userid, longitude, latitude, speed, date, time_spent)


        mycursor.execute(add_data, mysqldata)
        mydb.commit()

    if request.method == "GET":
        return render_template("index.html", comments=comments)
    ##

    ##
    return 'Valid JSON request received!'




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
