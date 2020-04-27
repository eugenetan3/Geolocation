import mysql.connector
import csv

# check if there is any connection error
try:
    #connect to the mysql database
    connection = mysql.connector.connect(
        user='eugenettt', password='password',
        host='ix-dev.cs.uoregon.edu', database='my_db',
        port = "3226"
    )

# if there is an error, print out the error message
except mysql.connector.Error as err:
    print("Error: {}".format(err))

# otherwise
else:
    my_database = connection.cursor()
    #sql format to receive all data from desired table
    sql_statement = "SELECT * FROM locationdata2"
    my_database.execute(sql_statement)
    #put the data into a list of strings
    output = my_database.fetchall()
    #close the connection
    connection.close()

    #data from output fixed into desired format and order
    data_array = [None] * len(output)

    #create the tab delimited text file
    with open("output.txt", 'w') as tabdfile:
        i = 0
        for line in output:
            #Parse the data
            userid = line[1]
            date = line[5].replace("-","/")[0:10]
            time = line[5][11:]
            latitude = line[3]
            longitude = line[2]
            time_at_location = line[6]

            #add the data to the data array to be sorted
            data_array[i] = [userid, date, time, latitude, longitude, time_at_location]
            i += 1

            #write to the text file
            tabdfile.write("%s\t%s\t%s\t%s\t%s\t%s\n"
             % (userid, date, time, latitude, longitude, time_at_location))

    #sort the data array
    data_array = sorted(data_array, key = lambda x: x[0])

    #write to the csv file
    with open("output.csv","w") as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data_array:
            csvwriter.writerow(row)
        
    connection.close()
        



