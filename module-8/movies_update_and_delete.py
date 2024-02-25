####
#Created for CSD310 by Ryan Norrbom
#Created Date: 2/17/2024
##Connects to a mysql table using a default user, Creates/Updates/Deletes DB content and JOINS
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


# Main Function
def main():
    # Test connection
    try:
        db = mysql.connector.connect(**config)
        print("\n Database user {} connected to MysQl on host {} with database {}".format(config["user"], config["host"], config["database"]))
        input("\n\n Press any key to continue...")

        #If there is a failure, handle it
        cursor = db.cursor()                                        

        while True:
            print("\nMovie Database Management")
            print("1. Display Films")
            print("2. Add or Update a Movie")
            print("3. Delete a Movie")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                show_films(cursor, "DISPLAYING FILMS")
            elif choice == '2':
                add_or_update_movie(cursor, db)
            elif choice == '3':
                delete_movie_record(cursor, db)
            elif choice == '4':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    #If there is a failure, handle it
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('The supplied username or password are invalid')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('The specified database does not exist')
        else:
            print(err)


# User Confirmation Function
def get_user_confirmation(prompt):
    return input(prompt).lower() in ['yes', 'y']

# Delete Record
def delete_movie_record(cursor, db):
    film_name = input("Enter the name of the film to delete: ")
    cursor.execute("SELECT film_id FROM film WHERE film_name = %s", (film_name,))
    if cursor.fetchone():
        if get_user_confirmation(f"Are you sure you want to delete {film_name}? (yes/no): "):
            cursor.execute("DELETE FROM film WHERE film_name = %s", (film_name,))
            db.commit()
            print(f"{film_name} was deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("Film not found.")

#Add Records
def add_or_update_movie(cursor, db):
    film_name = input("Enter the film name: ")
    director = input("Enter the director's name: ")
    film_release = input("Enter the Release year: ")
    film_runtime = input("Enter Film Runtime (In minutes): ")
    genre_input = input("Enter the genre (name or ID): ")
    studio_input = input("Enter the studio (name or ID): ")

    # Handle genre and studio inputs
    genre_id = handle_genre(cursor, db, genre_input)
    if genre_id is None:
        print("Operation cancelled or failed due to genre issue.")
        return

    studio_id = handle_studio(cursor, db, studio_input)
    if studio_id is None:
        print("Operation cancelled or failed due to studio issue.")
        return

    # Check if the movie exists
    cursor.execute("SELECT film_id FROM film WHERE film_name = %s", (film_name,))
    film_result = cursor.fetchone()

    if film_result:
        # Movie exists, prompt for update
        if get_user_confirmation(f"The movie '{film_name}' already exists. Do you want to update its details? (yes/no): "):
            cursor.execute("UPDATE film SET film_director = %s, film_releaseDate = %s, film_runtime = %s ,genre_id = %s, studio_id = %s WHERE film_name = %s",
                           (director, film_release, film_runtime, genre_id, studio_id, film_name))
            db.commit()
            print(f"Movie '{film_name}' updated successfully!")
    else:
        # Movie does not exist, insert as new
        if get_user_confirmation("This movie does not exist. Would you like to add it as a new movie? (yes/no): "):
            cursor.execute("INSERT INTO film (film_name, film_director, film_releaseDate, film_runtime, genre_id, studio_id) VALUES (%s, %s, %s, %s, %s, %s)",
                           (film_name, director, film_release, film_runtime, genre_id, studio_id))
            db.commit()
            print(f"Movie '{film_name}' added successfully!")


#Handle for Genre/Genre ID
def handle_genre(cursor, db, genre_input):
    if genre_input.isdigit():
        cursor.execute("SELECT genre_id FROM genre WHERE genre_id = %s", (genre_input,))
    else:
        cursor.execute("SELECT genre_id FROM genre WHERE genre_name = %s", (genre_input,))
    genre_result = cursor.fetchone()

    if not genre_result:
        if get_user_confirmation("This genre does not exist. Would you like to add it? (yes/no): "):
            cursor.execute("INSERT INTO genre (genre_name) VALUES (%s)", (genre_input,))
            db.commit()
            return cursor.lastrowid  # Return the new genre ID
        else:
            return None  # No genre ID to return
    else:
        return genre_result[0]  # Return existing genre ID

# Handle for Studio and Studio ID
def handle_studio(cursor, db, studio_input):
    if studio_input.isdigit():
        cursor.execute("SELECT studio_id FROM studio WHERE studio_id = %s", (studio_input,))
    else:
        cursor.execute("SELECT studio_id FROM studio WHERE studio_name = %s", (studio_input,))
    studio_result = cursor.fetchone()

    if not studio_result:
        if get_user_confirmation("This studio does not exist. Would you like to add it? (yes/no): "):
            cursor.execute("INSERT INTO studio (studio_name) VALUES (%s)", (studio_input,))
            db.commit()
            return cursor.lastrowid  # Return the new studio ID
        else:
            return None  # No studio ID to return
    else:
        return studio_result[0]  # Return existing studio ID


# The JOIN tables funciton
def show_films(cursor, title):
    print(title)
    query = """SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name' 
               FROM film 
               INNER JOIN genre ON film.genre_id=genre.genre_id 
               INNER JOIN studio ON film.studio_id=studio.studio_id"""
    cursor.execute(query)
    results = cursor.fetchall()
    for film in results:
        print(f"Name: {film[0]}, Director: {film[1]}, Genre: {film[2]}, Studio Name: {film[3]}")

# Initialize the Primary Function
main()

#End