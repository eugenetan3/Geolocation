'''
Description: This is the hosted python flask web application which is the primary driver of 
the visualization module by reading from stored data within the database and then applied
to cluster and visualize it.

Source for clustering algorithm:
Bradley N. Miller and David L. Ranum. 2013. Python Programming In Context (2nd. ed.). Jones and Bartlett Publishers, Inc., USA.(ch.7)

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
    """
    Description: This function will calculate the centroid of each cluster
        and the number of points in each cluster. Then it returns centroids in centroid_list.
        The longitude of centroid is the average longitude for each cluster.
        The same is true for the latitudes.
    :param cluster_list: list of clusters. Each cluster is a list of location pairs.
        location pairs are of the form [longitude, latitude]
    :return: a list of the centroid for each cluster. each centroid in form of [longitude, latitude, # location]
    """

    new_centroid_list = []  
    for a_cluster in cluster_list:  # iterate through list of clusters
        longitude_sum = 0 
        latitude_sum = 0
        num_of_loc = len(a_cluster)
        for a_loc in a_cluster: # iterate through locations in clusters
            # sum the locations
            longitude_sum += a_loc[0]   
            latitude_sum += a_loc[1]
        # average the locations, create the centroid
        new_centroid = [longitude_sum / num_of_loc, latitude_sum / num_of_loc, num_of_loc]
        new_centroid_list.append(new_centroid)
    return new_centroid_list


def cluster_approximate(location_list: list, centroid_list: list, new_range_square: float) -> list:
    """
    Description: Reclustering by the new centroid to make the cluster more precise.
        For each centroid in the centroid_list, traverse the location_list
        and if the location is within the defined new range,
        add that location to the cluster associated with that centroid

    :param location_list: list of location pairs. Each location is of form (longitude, latitude)
    :param centroid_list: list of centroids. each centroid is of form [longitude, latitude, # location]
    :param new_range_square: the desired radius of each cluster squared.
        Use square to avoid calculating the square root in the calculation of distance.
    :return: list of centroid for each new cluster.
        each centroid in form of [longitude, latitude, # location]
    """
    new_cluster_list = []
    for curr_centroid in centroid_list: # iterate over each centroid
        curr_cluster = []
        for i in range(0, len(location_list)):  # iterate over all data points
            loc = location_list.pop(0)  # take the next location out of the list
            # find the distance from this point to the centroid
            distance = (curr_centroid[0] - loc[0]) ** 2 + (curr_centroid[1] - loc[1]) ** 2
            if distance <= new_range_square:    # if the point is within the desired distance
                curr_cluster.append(loc)    # add it to the associated cluster
            else:
                location_list.append(loc)   # otherwise put it back into the list
        new_cluster_list.append(curr_cluster)   
    new_centroid_list = centroid(new_cluster_list)
    return new_centroid_list


def cluster(location_list: list) -> list:
    """
    Description: Pop a location from the location_list called curr_loc, traverse the location_list,
        and pop all locations that are within the initially defined distance (4 * range_square)
        to a cluster associated with the popped location. Repeat this until the list of locations
        is empty.
        Then, use the cluster_approximate function to make the cluster more and more precise.
        In each approximation, narrow down the new_range_square that input to function cluster_approximate
    :param location_list: list of location pairs. Each location in form of (longitude, latitude)
    :return: list of centroid for each final cluster.
        each centroid in form of [longitude, latitude, # location]
    """
    location_list_copy = location_list.copy()
    first_range_square = range_square * 4   # the initial desired radius for each cluster
    cluster_list = []
    while len(location_list_copy) > 0:  # continue until the list of locations is empty
        curr_loc = location_list_copy.pop() # pop the first location in the list
        curr_cluster = []   
        for i in range(0, len(location_list_copy)): # traverse through all other locations left
            loc = location_list_copy.pop(0) # remove the next location temporarily
            # find the distance between the temporary location and the original
            distance = (curr_loc[0] - loc[0]) ** 2 + (curr_loc[1] - loc[1]) ** 2
            if distance <= first_range_square:  # if the temporary location is close enough
                curr_cluster.append(loc)    # add it to the associated cluster
            else:
                location_list_copy.append(loc)  # otherwise, put it back in the location list
        curr_cluster.append(curr_loc)
        cluster_list.append(curr_cluster)

    centroid_list = centroid(cluster_list)
    # first approximate
    new_centroid_list = cluster_approximate(location_list.copy(), centroid_list, range_square * 2)
    # second approximate
    new_centroid_list = cluster_approximate(location_list.copy(), new_centroid_list, range_square * 1.5)
    # third approximate
    new_centroid_list = cluster_approximate(location_list.copy(), new_centroid_list, range_square * 1.1)
    return new_centroid_list

def find_largest_hotspot(centroid_list: list) -> int:
    """
    Description: Find the size of the cluster with the most data points

    :param centroid_list: list of centroid for each final cluster.
        each centroid in form of [longitude, latitude, # location]
    :return: an integer which is the length of the longest cluster
    """
    largest_hotspot = 0     # set the current largest size
    for a_centroid in centroid_list:    # iterate through each centroid
        if a_centroid[2] > largest_hotspot: # if [# location] > the current largest size
            largest_hotspot = a_centroid[2] # change the largest size to the size of this centroid
    return largest_hotspot

def mark(centroid_list: list, largest_hotspot: int) -> map:
    """
    Description: Using folium to generate interactive maps,
        and  mark each centroid on the map in the form of folium standard marker,
        then store the number of locations in the popup text of the markers.
        Take the latitude and longitude of each centroid as the center of the circle,
        and # location as the radius, generate a circle mark to indicate the density of the population.
        And change circle color depend on the density of the population.
        Highest density is red,lowest density is green.
    :param centroid_list: list of centroid for each final cluster.
        each centroid in form of [longitude, latitude, # location]
    :param largest_hotspot: the size of the cluster with the most data points
    :return: A marked folium map
    """
    m = folium.Map(location=[44.3188462041, -120.932963], zoom_start=7)
    # create a Folium map centered on Eugene
    for a_centroid in centroid_list:    # iterate through each centroid
        # find the ratio of this centroid's cluster's size to the largest cluster
        proportion = a_centroid[2]/largest_hotspot
        # assign a color according to this proportion
        if proportion < .25:
            color = 'green'
        elif proportion < .5:
            color = 'yellow'
        elif proportion < .75:
            color = 'orange'
        else:
            color = 'red'
        # create a circle around this cluster to represent the hotspot's danger size
        folium.Circle(
            location=(a_centroid[0], a_centroid[1]),
            radius= proportion * factor,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

        # create a marker at the cluster's centroid that displays its actual size when touched
        folium.Marker(
            location=(a_centroid[0], a_centroid[1]),
            popup=f"population: {a_centroid[2]}",    # information on the icon
            icon=folium.Icon(color = color, icon='info-sign')
        ).add_to(m)
    return m

def make_map(user_time):
    """
    Description: Loading location data, call cluster function to cluster location data,
        then call mark function to mark cluster information on the folium map
    :return: Void
    """
    # connect to the MySQL database on PythonAnywhere
    mydb = mysql.connector.connect(host="eugenet.mysql.pythonanywhere-services.com", user="eugenet", passwd="Swimming1337", database="eugenet$default", port="3306")
    my_database = mydb.cursor()

    # take all data from the desired table
    sql_statement = "SELECT * FROM locationdata2"
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    mydb.close()

    location_list = []
    for line in output: # iterate over the data
        latitude = line[3]  
        longitude = line[2]
        data_time = line[5][11:13]

        # check if the time the data was collected matches the desired time interval
        if data_time == user_time.split("-")[0]:
            # if so, add it to the list of locations to be clustered and plotted
            location_list.append((float(latitude),float(longitude)))
            
    # if there are no locations (no time interval is input or the database in that time
    # interval is empty, just display an empty map
    if len(location_list) == 0:
        m = folium.Map(location=[44.3188462041, -120.932963], zoom_start=7)
        m.save('./mysite/templates/map.html')

    # run the clustering algorithm
    centroid_list = cluster(location_list)
    # find the largest cluster
    largest_hotspot = find_largest_hotspot(centroid_list)
    # mark the map
    m = mark(centroid_list,largest_hotspot)
    m.save('./mysite/templates/map.html')
    return

app = flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/switch", methods=['GET', 'POST'])
def index():
    # find the desired time interval via WebApp
    user_time = str(request.form['site'])
    # make the map for the desired time interval
    make_map(user_time)
    return render_template('map.html')



@app.route("/post-requests", methods=['GET', 'POST'])
def post_request(comments=[]):
    # connect to MySQL database on PythonAnywhere
    mydb = mysql.connector.connect(host="eugenet.mysql.pythonanywhere-services.com", user="eugenet", passwd="Swimming1337", database="eugenet$default", port="3306")
    mycursor = mydb.cursor()

    # format for inserting data into desired table
    add_data = ("INSERT INTO locationdata2 "
               "(id, user_id, longitude, latitude, speed, timestamp, time_spent) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    # make a request to get the JSON data
    data = request.get_json()
    comments.append(data)

    if (data != None):
        userid = data['User ID']
        longitude = data['Longitude']
        latitude = data['Latitude']
        speed = data['Speed']
        date = data['Date']
        time_spent = data['Time Spent']
        mysqldata = ('0', userid, longitude, latitude, speed, date, time_spent)
        # insert the formatted data into the MySQL database
        mycursor.execute(add_data, mysqldata)
        mydb.commit()

    if request.method == "GET":
        return render_template("index.html", comments=comments)

    return 'Valid JSON request received!'

@app.route("/", methods=['GET', 'POST'])
def menuselect():
    # format for inputting time interval by user
    sites = ["00-01","01-02",'02-03','03-04','04-05','05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-24']
    return render_template("switch.html", sites=sites)


if __name__ == '__main__':
    app.run(debug=True)




