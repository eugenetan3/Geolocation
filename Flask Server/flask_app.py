'''
Description: This is the hosted python flask web application which is the primary driver of 
the visualization module by reading from stored data within the database and then applied
to cluster and visualize it.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 5/18/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof
'''

import flask
import time
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import json

import folium
import mysql.connector


range_square = 0.0000001    # The radius of the cluster
factor = 1000                # size of red circle = factor * #population
start_zoom = 15             # initial zoom of viewpoint

def centroid(cluster_list: list) -> list:

    new_centroid_list = []
    for a_cluster in cluster_list:
        longitude_sum = 0
        latitude_sum = 0
        num_of_loc = len(a_cluster)
        for a_loc in a_cluster:
            longitude_sum += a_loc[0]
            latitude_sum += a_loc[1]
        new_centroid = [longitude_sum / num_of_loc, latitude_sum / num_of_loc, num_of_loc]
        new_centroid_list.append(new_centroid)
    return new_centroid_list


def cluster_approximate(location_list: list, centroid_list: list, new_range_square: float) -> list:
    new_cluster_list = []
    for curr_centroid in centroid_list:
        curr_cluster = []
        for i in range(0, len(location_list)):
            loc = location_list.pop(0)
            distance = (curr_centroid[0] - loc[0]) ** 2 + (curr_centroid[1] - loc[1]) ** 2
            if distance <= new_range_square:
                curr_cluster.append(loc)
            else:
                location_list.append(loc)
        new_cluster_list.append(curr_cluster)
    new_centroid_list = centroid(new_cluster_list)
    return new_centroid_list


def cluster(location_list: list) -> list:
    location_list_copy = location_list.copy()
    first_range_square = range_square * 4
    cluster_list = []
    while len(location_list_copy) > 0:
        curr_loc = location_list_copy.pop()
        curr_cluster = []
        for i in range(0, len(location_list_copy)):
            loc = location_list_copy.pop(0)
            distance = (curr_loc[0] - loc[0]) ** 2 + (curr_loc[1] - loc[1]) ** 2
            if distance <= first_range_square:
                curr_cluster.append(loc)
            else:
                location_list_copy.append(loc)
        curr_cluster.append(curr_loc)
        cluster_list.append(curr_cluster)

    centroid_list = centroid(cluster_list)
    # first approximate
    new_centroid_list = cluster_approximate(location_list.copy(), centroid_list, range_square * 2)
    # second approximate
    new_centroid_list = cluster_approximate(location_list.copy(), new_centroid_list, range_square * 1.5)
    # third approximate
    new_centroid_list = cluster_approximate(location_list.copy(), new_centroid_list, range_square * 1.1)
    # print("centroid_list:", new_centroid_list)
    return new_centroid_list

def find_largest_hotspot(centroid_list: list) -> int:
    largest_hotspot = 0
    for a_centroid in centroid_list:
        if a_centroid[2] > largest_hotspot:
            largest_hotspot = a_centroid[2]
    return largest_hotspot

def mark(centroid_list: list, largest_hotspot: int) -> map:
    m = folium.Map(location=[44.3188462041, -120.932963], zoom_start=7)
    for a_centroid in centroid_list:

        proportion = a_centroid[2]/largest_hotspot
        if proportion < .25:
            color = 'green'
        elif proportion < .5:
            color = 'yellow'
        elif proportion < .75:
            color = 'orange'
        else:
            color = 'red'

        folium.Circle(
            location=(a_centroid[0], a_centroid[1]),
            radius= proportion * factor,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

        folium.Marker(
            location=(a_centroid[0], a_centroid[1]),
            popup=f"population: {a_centroid[2]}",    # information on the icon
            icon=folium.Icon(color = color, icon='info-sign')
        ).add_to(m)
    return m

def make_map(user_time):

    mydb = mysql.connector.connect(host="eugenet.mysql.pythonanywhere-services.com", user="eugenet", passwd="Swimming1337", database="eugenet$default", port="3306")
    my_database = mydb.cursor()

    sql_statement = "SELECT * FROM locationdata2"
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    mydb.close()

    location_list = []
    for line in output:
        latitude = line[3]
        longitude = line[2]
        data_time = line[5][11:13]

        if data_time == user_time.split("-")[0]:
            location_list.append((float(latitude),float(longitude)))
    if len(location_list) == 0:
        m = folium.Map(location=[44.3188462041, -120.932963], zoom_start=7)
        m.save('./mysite/templates/map.html')

    centroid_list = cluster(location_list)
    largest_hotspot = find_largest_hotspot(centroid_list)
    m = mark(centroid_list,largest_hotspot)
    m.save('./mysite/templates/map.html')
    return

app = flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/switch", methods=['GET', 'POST'])
def index():
    user_time = str(request.form['site'])
    make_map(user_time)
    return render_template('map.html')



@app.route("/post-requests", methods=['GET', 'POST'])
def post_request(comments=[]):

    mydb = mysql.connector.connect(host="eugenet.mysql.pythonanywhere-services.com", user="eugenet", passwd="Swimming1337", database="eugenet$default", port="3306")
    mycursor = mydb.cursor()

    add_data = ("INSERT INTO locationdata2 "
               "(id, user_id, longitude, latitude, speed, timestamp, time_spent) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data = request.get_json()
    comments.append(data)

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

    return 'Valid JSON request received!'

@app.route("/", methods=['GET', 'POST'])
def menuselect():
    sites = ["00-01","01-02",'02-03','03-04','04-05','05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24']
    return render_template("switch.html", sites=sites)


if __name__ == '__main__':
    app.run(debug=True)




