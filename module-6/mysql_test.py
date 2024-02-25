####
#Created for CSD310 by Ryan Norrbom
#Created Date: 2/10/2024
##Connects to a mysql table using a default user. 
#
#Password and username are not sanitized
####

#start

import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}

# Test connection
try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MysQl on host {} with database {}".format(config["user"], config["host"], config["database"]))
    input("\n\n Press any key to continue...")

#If there is a failure, handle it
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('The supplied username or password are invalid')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('The specified database does not exist')
    else:
        print(err)


#Close the connection when done
finally:
    db.close()

#end