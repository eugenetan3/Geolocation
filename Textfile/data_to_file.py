import mysql.connector
import csv

connection = mysql.connector.connect(
    user='eugenet', password='password',
    host='ix-dev.cs.uoregon.edu', database='my_db',
    port = "3226"
)

my_database = connection.cursor()
sql_statement = "SELECT * FROM locationdata2"
    
my_database.execute(sql_statement)
output = my_database.fetchall()

#data from output fixed into desired format and order
data_array = [None] * len(output)

with open("output.txt", 'w') as tabdfile:
    i = 0
    for line in output:
        userid = line[1]
        date = line[5].replace("-","/")[0:10]
        time = line[5][11:]
        latitude = line[3]
        longitude = line[2]
        time_at_location = line[6]
            
        data_array[i] = [userid, date, time, latitude, longitude, time_at_location]
        i += 1
        
        tabdfile.write("%s\t%s\t%s\t%s\t%s\t%s\n"
         % (userid, date, time, latitude, longitude, time_at_location))

    
data_array = sorted(data_array, key = lambda x: x[0])


with open("output.csv","w") as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data_array:
        csvwriter.writerow(row)
    

    

connection.close()
