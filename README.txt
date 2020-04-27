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
