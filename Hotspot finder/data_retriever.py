import mysql.connector
import sshtunnel
import csv

# check if there is any connection error
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
#connect to the mysql database
with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username = 'eugenet',
    ssh_password = 'Group3422',
    remote_bind_address=('eugenet.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = mysql.connector.connect(
        host='127.0.0.1', user='eugenet',
        password='Swimming1337', database='eugenet$comments',
        port = tunnel.local_bind_port
    )



    my_database = connection.cursor()
    #sql format to receive all data from desired table
    sql_statement = "SELECT * FROM comments"
    my_database.execute(sql_statement)
    #put the data into a list of strings
    output = my_database.fetchall()
    #close the connection
    connection.close()

    for line in output:
        print(line)
        print()
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

connection.close()



