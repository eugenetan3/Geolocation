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
    -installation requires the use of the Flask python package. Enter the following text into the terminal which you are using: $pip3   install Flask
        --if this pip installation fails try and use: $pip install Flask for Python 2.X
    -installation requires the use of the mysql-connector-python package. Enter the following text into the terminal which you are            using: $pip3 install mysql-connector-python. 
        --if this pip installation fails try and use: $pip install mysql-connector-python for Python 2.X
    -should either method of installation fail, double check the current installation of pip and try the installation process again
    
How to run the data output code:
    -To run the data outputting code, navigate inside the Geolocation Project Folder and enter the following into the terminal:                $python3 data_to_file.py
        --if this does not execute successfuly, try and enter the following: $python data_to_file.py
--------------------------------------------------------------------------------------------------------------------------------
!!!The below instruction is on if you would like to replicate the project yourself by building each component as your own!!!

How to host webserver:
To install and host the Flask server, you must first download the zip file containing Geolocation. Within the zip file contains two files: flask_app.py and index.html. To successfully create a host for the iOS device to interface with you must host the flask application.

A prerequisite to create the Flask server is that you must create an account on https://PythonAnywhere.com , during account creation simply fill out corresponding First and Last name fields as well as an email. The ‘Free’ account user should suffice for the scope of this project. 

Upon successful account creation the following steps are:
    1-When in the PythonAnywhere Dashboard navigate to ‘Web apps’ and click on “Add a new Web app” which should redirect you to a configuration page for the web app.
    2-The site is now hosting a default template provided by PythonAnywhere, navigate within the configuration page to the Code section, to the right of where it says ‘Source Code’ click on >Go to directory.
    3-Within that directory, click on the yellow button “Upload a file” and select the downloaded flask_app.py file.
    4-Next, on the left hand side click on “New Directory” and name the directory ‘templates’.
    5-Navigate to the newly created directory and add the ‘index.html’ file that was downloaded to it. 
    6-Now return to the configuration page by returning to the dashboard and selecting the web app listed under “Web App”
    7-Towards the top of the screen click: “Reload <username>.pythonanywhere.com”
    8-The site is now successfully hosted and you can navigate to that site on any device.
    9-To send POST requests to the device properly, within the downloaded Geolocation zip, within GeolocationSwift-Master, navigate into Geolocation directory and into viewcontroller.swift
    10-Within viewcontroller.swift, change line 104’s URL to ‘https://<username>.pythonanywhere.com/post_request’.
    11-Recompile the iOS app to reflect the change to POST destination.
    12-App is now successfully directing requests to this website.
    
How to create mysql database:
    -In order to create the MySQL database on ix-dev servers, you must have an account registered within the ix-dev servers, if you do not have an account you can create one at https://systems.cs.uoregon.edu/wiki/index.php.

Upon successful creation and approval of an ix-dev account, the following steps will create the MySQL database:
    1-To enter your ix-dev account, use your favorite ssh client and type: “$ ssh <username>@ix-dev.cs.uoregon.edu
    2-To install the initial tables, in terminal execute: “$ mysqlctl install”, it will prompt for a password, input a memorable password as this is the database password.
    3-Within the terminal, now type “$ vim .my.cnf”, within the file, uncomment ‘password’ and comment out the line: “default-storage-engine=myisam” as well as “skip-innodb”. Uncomment the line: “bind-address = 0.0.0.0.”
    4-The contents of the file should now look like this: 
    5-Now enter: “$mysql -p” and enter your password as prompted.
    6-Type: “$ CREATE DATABASE <database name>;”
    7-Navigate to the newly created database by typing “$use <databasename>;”
    8-Type: “$ CREATE TABLE <tablename> (user_id text, longitude text, latitude text, speed text, timestamp text, time_spent text);”
    9-The table has now been created, you can verify this by typing: “$ show tables;” then exit by typing “$ \q”
    10-Having exited the MySQL client, you can now type “$ mysqlctl start” it will begin running the server and list a port number the server is running on. You can type “$mysqlctl status” to see what the current status is.
    11-Now for the flask server to successfully enter items in the MySQL database, navigate to https://pythonanywhere.com and go to the source code directory mentioned above.
    12-When in the directory where flask_app.py exists, click on it and it will open a text editor.
    13-Within the text editor, within the function “post_request” replace the contents of username, password, database, and port number with the respective items that you just obtained above. Replace within line 44: locationdata2 with the name of your table. 
    14-Perform the Step 13 on data_to_file.py as well.
    15-Replace username with your username, password with the database password, database with the name of your database, and port number with the port number returned when the server began running. Upon successful replacement, save the file by clicking save in the top right.
    16-Return to the configuration page of your web app and click: “Reload <name>.pythonanywhere.com”
    17-The contents sent through the flask server will now be sent and entered into the MySQL database.
    18-Repeat steps 14 except within the data_to_file.py file within the directory it is downloaded by editing with a text editor.
    19-Be aware that if you shut the server down by using “$ mysqlctl stop” when you start again it may be listening on a different port number (which requires you to change the port).
--------------------------------------------------------------------------------------------------------------------------------

!!!This is the instruction on how to execute the code as it currently exists (with existing Flask Server and MySQL Database)!!!

The following are the steps to downloading aggregated data from the MySQL database to the local directory:
    0-The pip installation of mysql-connector-python has already been completed is a requisite, if it hasn't been installed yet refer to the pip installations above.
    1-Navigate to the directory where the downloaded Geolocation exists. Navigate to the directory containing file “date_to_file.py.” 
    2-To run the data output software, execute the command “python3 date_to_file.py”
    3-Ensure that a valid internet connection exists during execution of this command so the python software can connect to the remote database. 
    4-Upon executing successfully, within the same directory as the file “date_to_file.py” should exist output.csv and output.txt
    5-The two output files, output.txt exists as a tab delimited text file containing the raw aggregated data collected within the database. Output.csv is sorted by user and time representation of the data. Both files contain no data smoothing.

        
Software Dependencies:
     Python 3.X
     MySQL
     MySQL-connector-python
     Swift 5
     PythonAnywhere
     
Subdirectories:
    GeolocationSwift-master: XCode project archive, contains source code for the iOS application Geolocation-422 written in Swift 5
    Textfile: source code for data conversion from MySQL database to tab delimited output file.
