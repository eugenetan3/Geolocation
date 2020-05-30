"""
Description: This python file will read the output of Time Interval Data Retriever,
Loading the longitude and latitude into location_list.
Clustering location data by giving the maximum radius of clusters.
Calculate the  centroid and the number of location for each clusters,
and store in centroid_list. Each centroid in the format of [longitude, latitude, # location]
Using folium to generate interactive maps,
and  mark each centroid on the map in the form of folium standard marker,
then store the number of locations in the popup text of the markers.
Take the latitude and longitude of each centroid as the center of the circle,
and # location as the radius, generate a circle mark to indicate
the density of the crowd.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 5/19/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof
"""

import folium
import mysql.connector
import sshtunnel
import csv


# Settings
range_square = 0.0000001    # The radius of the cluster
factor = 50                 # size of red circle = factor * #population
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
    m = folium.Map(location=[45.35327764580474, -122.85393959924241], zoom_start=start_zoom)
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


def main():
    print("Interacting with database...", end='')      

    # check if there is any connection error
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    #connect to the mysql database
    with sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'),
        ssh_username = 'eugenet',
        ssh_password = 'Group3422',
        remote_bind_address=('eugenet.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        connection = mysql.connector.connect(
            host='127.0.0.1', user='eugenet',
            password='Swimming1337', database='eugenet$comments',
            port = tunnel.local_bind_port
        )
        my_database = connection.cursor()
        #sql format to receive all data from desired table
        sql_statement = "SELECT * FROM comments"
        my_database.execute(sql_statement)
        #put the data into a list of strings
        output = my_database.fetchall()
        #close the connection
        connection.close()
        
    location_list = []
    for line in output:
        point = eval(line[1])
        longitude = point['Longitude']
        latitude = point['Latitude']
        location_list.append((float(latitude),float(longitude)))
        
    print("done")
    print("calculating cluster... ", end='')
    centroid_list = cluster(location_list)
    largest_hotspot = find_largest_hotspot(centroid_list)
    print("done")
    print("visualizing on map... ", end='')
    m = mark(centroid_list,largest_hotspot)
    m.save('map.html')
    print("done")
    return


if __name__ == "__main__":
    main()
