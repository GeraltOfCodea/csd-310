####
#Created for CSD310 by Ryan Norrbom
#Created Date: 2/17/2024
##Connects to a mysql table using a default user, Queries for DB content
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

cursor = db.cursor()

# Query 1: Select all fields from the studio table
print("\n-- DISPLAYING Studios --")
cursor.execute("SELECT * FROM studio")
studios = cursor.fetchall()
for studio in studios:
    print("\n\tStudio ID: {}\n\tStudio Name: {}".format(studio[0], studio[1]))

print("\n-- DISPLAYING Genres --")
# Query 2: Select all fields from the genre table
cursor.execute("SELECT * FROM genre")
genres = cursor.fetchall()
for genre in genres:
    print("\n\tGenre ID: {}\n\tGenre Name: {}".format(genre[0], genre[1]))

print("\n-- DISPLAYING Movies with a runtime of less than 2 hours --")
# Query 3: Select movie names(Film Table) for movies with a runtime of less than 2 hours
cursor.execute("SELECT film_name, film_runtime FROM film WHERE CAST(film_runtime AS SIGNED) < 120")
short_movies = cursor.fetchall()
for film in short_movies:
    print("\n\tFilm Name: {}\n\tRuntime: {} ".format(film[0],film[1]))

print("\n-- DISPLAYING Movies grouped by director --")
# Query 4 revised: List of film names concatenated and grouped by director
cursor.execute("SELECT GROUP_CONCAT(film_name) AS film_names, film_director FROM film GROUP BY film_director")
movies_by_director = cursor.fetchall()
for film in movies_by_director:
    # Splitting film_names to list each movie on a new line for readability
    film_names = film[0].split(',')
    print("\n\tDirector: {}".format(film[1]))
    for name in film_names:
        print("\t\tFilm Name: {}".format(name))

#Close the connection when done!
db.close()

#end