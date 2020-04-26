# Geolocation
--------------------------------------------------------------------------------------------------------------------------------

Project Description: Our system utilizes geospatial data to collect data on users' movements during the COVID-19 pandemic. It allows user locations to be reported accurately to a hosted web server which then delivers the user's data into a secure MySQL Database. Storage within the database allows for manipulation of user data and examination of an user geospatial information.

Authors: Eugene Tan, Ellie Yun, Jackson Klagge, Gaoyuan Chen, Matthew Struble

Created: 4/18/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof


How to host webserver:
    -take python file flask_app.py and index.html and navigate to PythonAnywhere.com and create an account
    -after you create the account, navigate to the dashboard and open the 'Web App' section.
    -navigate to the web app page and go to > source code > go directory and upload flask_app.py
    -create a new subdirectory in that directory called 'Templates' and upload index.html into that folder.
    -go back to your webapp page and click: 'reload <page name>'
    -page is now hosted on pythonanywhere and data can be sent through hosted server

How to install:
    -installation requires the use of the Flask python package. Enter the following text into the terminal which you are using: $pip3   install Flask
        --if this pip installation fails try and use: $pip install Flask for Python 2.X
    -installation requires the use of the mysql-connector-python package. Enter the following text into the terminal which you are            using: $pip3 install mysql-connector-python. 
        --if this pip installation fails try and use: $pip install mysql-connector-python for Python 2.X
    -should either method of installation fail, double check the current installation of pip and try the installation process again
    
How to run the data output code:
    -To run the data outputting code, navigate inside the Geolocation Project Folder and enter the following into the terminal:                $python3 data_to_file.py
        --if this does not execute successfuly, try and enter the following: $python data_to_file.py
        
Software Dependencies:
     Python 3.X
     MySQL
     MySQL-connector-python
     Swift 5
     PythonAnywhere
     
Subdirectories:
    GeolocationSwift-master: XCode project archive, contains source code for the iOS application Geolocation-422 written in Swift 5
    Textfile: source code for data conversion from MySQL database to tab delimited output file.
