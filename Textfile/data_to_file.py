import mysql.connector

connection = mysql.connector.connect(
    user='eugenet', password='password',
    host='ix-dev.cs.uoregon.edu', database='my_db',
    port = "3226"
)

my_database = connection.cursor()
sql_statement = "SELECT * FROM locationdata2"
    
my_database.execute(sql_statement)
output = my_database.fetchall()

with open("data_output.txt", 'w') as df:
    for line in output:
        userid = line[1]
        date = line[5].replace("-","/")[0:10]
        time = line[5][11:]
        latitude = line[3]
        longitude = line[2]
        time_at_location = line[6]

        df.write("%s\t%s\t%s\t%s\t%s\t%s\n"
                 % (userid, date, time, latitude, longitude, time_at_location))
    
connection.close()
