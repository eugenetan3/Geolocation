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
and # location as the radius, generate a circle mark to indicat the density of the crowd.
And change circle color depend on the density of the population. Highest density is red,lowest density is yellow.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 5/19/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof
"""

import folium

# Settings
range_square = 0.0000001    # The radius of the cluster
factor = 1                  # size of red circle = factor * #population
start_zoom = 15             # initial zoom of viewpoint
max_population = 320        # The upper limit of population


def centroid(cluster_list: list) -> list:
    """
    Description: This function will calculate the  centroid of each cluster
        and the number of cluster member. Then store in centroid_list then return it.
        The longitude of centroid is the average longitude for each cluster.
        The same to latitude
    :param cluster_list: list of cluster. each cluster is a list of location tube.
        location tube in form of [longitude, latitude]
    :return: list of centroid for each cluster. each centroid in form of [longitude, latitude, # location]
    """
    centroid_list = []
    for a_cluster in cluster_list:
        longitude_sum = 0
        latitude_sum = 0
        num_of_loc = len(a_cluster)
        for a_loc in a_cluster:
            longitude_sum += a_loc[0]
            latitude_sum += a_loc[1]
        new_centroid = [longitude_sum / num_of_loc, latitude_sum / num_of_loc, num_of_loc]
        centroid_list.append(new_centroid)
    return centroid_list


def cluster_approximate(location_list: list, centroid_list: list, new_range_square: float) -> list:
    """
    Description: Reclustering by the new centroid to make the cluster more precise.
        For each centroid in the centroid_list, traverse the location_list
        and add the location that the distance between this centroid is in the sqrt(new_range_square)
        to the corresponding cluster of this centroid.
    :param location_list: list of location tube. Each location in form of (longitude, latitude)
    :param centroid_list: list of centroid. each centroid in form of [longitude, latitude, # location]
    :param new_range_square: Squared of the radius of the cluster.
        Use square to avoid calculating the square root in the calculation of distance.
    :return: list of centroid for each new cluster.
        each centroid in form of [longitude, latitude, # location]
    """
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
    """
    Description: Pop a location from the location_list called curr_loc, traverse the location_list,
        and pop the location that the distance between curr_loc is in sqrt(2 * range_square)
        and add it to curr_loc corresponding cluster.
        Then using cluster_approximate function to make the cluster more precise.
        In each approximation, narrow down the new_range_square taht input to function cluster_approximate
    :param location_list: list of location tube. Each location in form of (longitude, latitude)
    :return: list of centroid for each final cluster.
        each centroid in form of [longitude, latitude, # location]
    """
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


def mark(centroid_list: list) -> map:
    """
    Description: Using folium to generate interactive maps,
        and  mark each centroid on the map in the form of folium standard marker,
        then store the number of locations in the popup text of the markers.
        Take the latitude and longitude of each centroid as the center of the circle,
        and # location as the radius, generate a circle mark to indicate the density of the population.
        And change circle color depend on the density of the population.
        Highest density is red,lowest density is yellow.
    :param centroid_list: list of centroid for each final cluster.
        each centroid in form of [longitude, latitude, # location]
    :return: A marked folium map
    """
    m = folium.Map(location=[45.35327764580474, -122.85393959924241], zoom_start=start_zoom)
    for a_centroid in centroid_list:
        longitude = a_centroid[0]
        latitude = a_centroid[1]
        population = a_centroid[2]
        # color calculation
        color_factor = population / max_population
        if color_factor > 1:
            color_factor = 1
        green = 255-int(color_factor*255)
        if green > 16:
            color = f"#ff{hex(green)[2:]}00"
        else:
            color = f"#ff0{hex(green)[2:]}00"
        # marking
        folium.Circle(
            location=(longitude, latitude),
            radius=population * factor,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

        folium.Marker(
            location=(longitude, latitude),
            popup=f"population: {population}",    # information on the icon
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    return m


def main():
    """
    Description: Loading location data, call cluster function to cluster location data,
        then call mark function to mark cluster information on the folium map
    :return: Void
    """
    print("loading file...", end='')
    f = open("output.txt", 'r')
    location_list = []
    for line in f:
        inf = line.strip().split()
        loc = (float(inf[3]), float(inf[4]))
        location_list.append(loc)
    print("done")
    print("calculating cluster... ", end='')
    centroid_list = cluster(location_list)
    print("done")
    print("visualizing on map... ", end='')
    m = mark(centroid_list)
    m.save('map.html')
    print("done")
    f.close()
    return


if __name__ == "__main__":
    main()
