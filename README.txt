# Geolocation Visualization
--------------------------------------------------------------------------------------------------------------------------------

Project Description: Our system utilizes geospatial data to collect data on users' movements during the COVID-19 pandemic. It allows user locations to be reported accurately to a hosted web server which then delivers the user's data into a secure MySQL Database. Storage within the database allows for manipulation of user data and examination of an user geospatial information. This Geospatial Data is then visualized in the form of a map for user consumption via web browser.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 5/18/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof
--------------------------------------------------------------------------------------------------------------------------------
REQUIRED:

Installation of these python packages must occur on https://pythonanywhere.com , a prerequisite is that you must have an account to be able to install.

1. Upon successful account creation navigate to the top “Consoles”:

2. Within the new page there is a prompt of “Start a new console:” select Other: ‘Bash’. This will open a bash terminal for you to perform installation commands. Within this bash console perform the following commands to install the packages.

Installation requires the use of the MySQL python package, to install this package enter the following into the terminal of your choosing with ‘pip installer’ installed on: pip3.7 install MySQL
Should this pip installation fail, try and use: pip3.7 install --user MySQL

Installation requires the use of the MySQL-connector-python package, to install this package enter the following into the terminal of your choosing with ‘pip installer’ installed on: pip3.7 install mysql-connector-python
Should this pip installation fail, try and use: pip3.7 install --user mysql-connector-python

Installation requires the use of the Folium python package, to install this package enter the following into the terminal of your choosing with ‘pip installer’ installed on: pip3.7 install folium
Should this pip installation fail, try and use: pip3.7 install --user folium

Should either method of the above installations fail, double check the current installation of pip and try the installation process again

How to run the data output code:
    -To be able to see the data visualization of the collected geospatial data, you must host the flask_app.py code onto https://pythonanywhere.com as a new web application. 
        
HOW TO HOST THE FLASK SERVER
The system requires specific package installations such as Folium and MySQL. Since pythonanywhere operates with its own versions, you must install these Python packages using their bash terminal. If you have already completed this, continue, otherwise refer to the instructions above. Installation of these packages is a prerequisite for the installation of the system.

Upon successful account creation the following steps are used to host the flask server and to instruct how to use the system upon successful hosting.

1. When in the PythonAnywhere Dashboard navigate to ‘Web apps’ and click on “Open Web tab” and then “Add a new Web app” which should redirect you to a configuration page. Select Flask >Next and then Python 3.7.

2. Click on ‘Next’, you can now see that your web application has been created, a page will be visualized. This page is accessible via the ‘Web’ item on the top left bar.

3. The site is now hosting a default template provided by PythonAnywhere, to supply the page with the provided code, navigate within the configuration page shown above down to the ‘Code’ section, to the right of where it says ‘Source Code’ click on >Go to directory. 

4. Within that directory, click on the yellow button “Upload a file” and select the downloaded flask_app.py file.

5. Next, on the left hand side name the directory ‘templates’ and click on “New Directory”. This will serve as the default folder for templates to be read from during the system execution.

6. Navigate to the newly created directory by double clicking ‘Templates’ and add the ‘index.html’ and ‘switch.html’ file that was downloaded via the ‘Upload a file’ button. 

7. Now return to the configuration page by returning to the dashboard by selecting ‘Dashboard’ from the top left bar. Then selecting the web app listed under “Web Apps” . Towards the top of the screen click the green button labelled: “Reload <username>.pythonanywhere.com”

8. The site is now successfully hosted and you can navigate to that site on any device. The Flask Server is now up but the MySQL Database connection is not functional yet.

HOW TO HOST A DATABASE ON PYTHONANYWHERE
1. To create a MySQL database on PythonAnywhere navigate to the databases tab, where you will be met with a page asking for a password. Create a memorable password that you will use for your MySQL database access. Do not forget this password, however, it is changeable later on should you like to change it.

2. After creation you will be on the generic MySQL Page. From there under section ‘Create a database’, enter a database name you’d like to create and click the green ‘Create’ button. The created database will be listed underneath the section ‘Your databases’.

3. Now you can open a MySQL console for the created database by clicking on the blue link to the right of “Start a console on:..”. Select the database you just created, its name will be <username>$<name of db>.

4. When you have opened it, a MySQL terminal will be shown. To create a MySQL table type the following command: “CREATE TABLE <tablename> (user_id text, longitude text, latitude text, speed text, timestamp text, time_spent text);”. Replace ‘<tablename>’ with whatever name you want the table to be named.

5.To verify the table has been made you can type: “SHOW TABLES;” and the tablename you just created will be listed under “Tables in <db name>.”

6. The database has been created on PythonAnywhere and is stored safely.

7. Now for the flask server to successfully enter items in the MySQL database, navigate to https://pythonanywhere.com and go to the source code directory mentioned above.

8. When in the directory where flask_app.py exists, click on it and it will open a text editor.

9. Within the text editor, within the function “post_request” and “make_map” replace the contents of username, password, database, and port number with the respective items that you just obtained above. These are lines 110 and 150 in flask_app.py.
    -Port number will always be: “3306”
    -Host will always be “<username>.mysql.pythonanywhere-services.com”
    -User will always be your PythonAnywhere username: “<username>”
    -Password will be the password you set for MySQL: <password>
    -Database will be:  <username>$<database name>

10. Additionally replace on line 153: where it says locationdata2, replace with the name of your table: 

11. Return to the configuration page of your web app and click: “Reload <name>.pythonanywhere.com”

12. The contents sent through the flask server will now be sent and entered into the MySQL database you created. Furthermore, mapping functions will now use the data stored within your MySQL Database.

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
