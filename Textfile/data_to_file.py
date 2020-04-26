'''
Description: The contained data_to_file.py file establishes a connection to the MySQL
database and reads and formats the data. It first writes the data into a tab delimited
text file, output.txt, and then sorts the data by user ID while maintaining relative
chronological order and writes that sorted data into a csv file, output.csv.

Authors: Eugene Tan, Ellie Yun, Gaoyuan Chen, Jackson Klagge, Matthew Struble

Group: 2020 Spring CIS422 Group 3

Created: 4/21/2020

Course: CIS 422 - Software Methodology Project 2 under Professor Anthony Hornof

'''

import mysql.connector
import csv

#establish a connection to the ix-dev MySQL database
connection = mysql.connector.connect(
    user='eugenet', password='password',
    host='ix-dev.cs.uoregon.edu', database='my_db',
    port = "3226"
)


my_database = connection.cursor()
#statement to receive all data in 
sql_statement = "SELECT * FROM locationdata2"

#execute the sql statement and put it into a list of strings 
my_database.execute(sql_statement)
output = my_database.fetchall()

print(type(output))
#data from output fixed into desired format and order
data_array = [None] * len(output)

#write the tab delimited text file
with open("output.txt", 'w') as tabdfile:
    #iterate over the output data
    i = 0
    for line in output:
        #format the strings
        userid = line[1]
        date = line[5].replace("-","/")[0:10]
        time = line[5][11:]
        latitude = line[3]
        longitude = line[2]
        time_at_location = line[6]

        #insert the data into array for sorting
        data_array[i] = [userid, date, time, latitude, longitude, time_at_location]
        i += 1

        #write to text file
        tabdfile.write("%s\t%s\t%s\t%s\t%s\t%s\n"
         % (userid, date, time, latitude, longitude, time_at_location))


#sort the data array
data_array = sorted(data_array, key = lambda x: x[0])

#write sorted data to csv file
with open("output.csv","w") as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data_array:
        csvwriter.writerow(row)
    

    

connection.close()
