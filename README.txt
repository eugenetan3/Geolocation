# Geolocation
--------------------------------------------------------------------------------------------------------------------------------

Project Description: Our system utilizes geospatial data to collect data on users' movements during the COVID-19 pandemic. It allows user locations to be reported accurately to a hosted web server which then delivers the user's data into a secure MySQL Database. Storage within the database allows for manipulation of user data and examination of an user geospatial information.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 4/18/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof
--------------------------------------------------------------------------------------------------------------------------------
REQUIRED:
How to install python packages:
    -installation requires use of mysqlclient to perform the underlying mysql connection.
        -Installation command: pip3 install mysql
            -Should this pip installation fail, try and use installation command: pip install mysql
                -Should either (or both) methods of installation fail, try and perform command: pip3 install mysqlclient
    -installation requires use of mysql-connector-python to perform the connection to the system database.
        -Installation command: pip3 install mysql-connector-python
            -Should this pip installation fail, try and use installation command: pip install mysql-connector-python
                -Should either (or both) methods of installation fail check the current installation of pip and try again!
    -installation requires use of folium to perform the visualization of the map interface.
        -Installation command: pip3 install folium
        -Should this pip installation fail, try and use installation command: pip install folium
        -Should either methods of installation fail check the current installation of pip and try again!

    
How to run the data output code:
    -To be able to see the data visualization of the collected geospatial data, you must host the flask_app.py code onto https://pythonanywhere.com as a new web application. 
        
--------------------------------------------------------------------------------------------------------------------------------
        
Software Dependencies:
     Python 3.7
     MySQL
     MySQL-connector-python
     Swift 5 (Project 1)
     PythonAnywhere
     
Subdirectories:
    GeolocationSwift-master: XCode project archive, contains source code for the iOS application Geolocation-422 written in Swift 5
    Textfile: source code for data conversion from MySQL database to tab delimited output file.
