'''
Description: This file manages the User Database module. It runs the Flask server and
database and reads and formats the data. It first writes the data into a tab delimited
text file, output.txt, and then sorts the data by user ID while maintaining relative
chronological order and writes that sorted data into a csv file, output.csv.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 4/18/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof
'''

import flask
import time
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import json
import mysql.connector

app = flask.Flask(__name__) #Alias Flask App

#Default webpage, is just a blank render template
@app.route("/")
def index():
    return render_template('index.html')



@app.route("/post-requests", methods=['GET', 'POST'])
def post_request(comments=[]):

    #Form MYSQL database connection to database hosted on ix
    mydb = mysql.connector.connect(host="ix-dev.cs.uoregon.edu", user="eugenet", passwd="password", database="my_db", port="3226")
    mycursor = mydb.cursor()

    #SQL command format to insert data 
    #add_data = ("INSERT INTO locationdata "
    #           "(id, data) "
    #           "VALUES (%s, %s)")

    #SQL command to insert data taken from app
    add_data = ("INSERT INTO locationdata2 "
               "(id, user_id, longitude, latitude, speed, timestamp, time_spent) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    #POST request to get JSON data that is posted to this url
    data = request.get_json()
    comments.append(data) #Add JSON data to local python list comments
    
    #debugging statement: comments.append(mydb.is_connected())
    
    #if data collected is not None (when page is refreshed it performs a GET), then assign JSON dictionary key values to variables
    if (data != None):
        userid = data['User ID']
        longitude = data['Longitude']
        latitude = data['Latitude']
        speed = data['Speed']
        date = data['Date']
        time_spent = data['Time Spent']

        #mysqldata = ('0', str(data))
        mysqldata = ('0', userid, longitude, latitude, speed, date, time_spent) #Form a tuple with JSON data


        mycursor.execute(add_data, mysqldata) #Execute the SQL command add_data with the tuple mysqldata
        mydb.commit() #Commit the data so it is saved

    if request.method == "GET":
        return render_template("index.html", comments=comments) #Render comments or valid entries
    ##

    ##
    return 'Valid JSON request received!'

if __name__ == '__main__':
    app.run(debug=True)
