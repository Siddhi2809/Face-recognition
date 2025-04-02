from datetime import datetime, timedelta;
import mysql.connector;
from mysql.connector import Error

def get_database_connection():
    # Return a connection and cursor to the database
    return mysql.connector.connect(host="localhost",
        user="root",
        password="root",
        database="attendance_py")



def markCheckInAttendances(user_id, name):

    # database connection code
    conn = get_database_connection()
    cursor = conn.cursor()

    # Create a table
    # create_table_query = """
    #     CREATE TABLE IF NOT EXISTS attendance (
    #         user_id INT primary key,
    #         name VARCHAR(30) NOT NULL,
    #         date DATE NOT NULL,
    #         in_time TIME,
    #         out_time TIME,
    #         status VARCHAR(1)
    #     )
    #     """
    # cursor.execute(create_table_query)

    # Check if the userId already exists in the database
    query_check = "SELECT * FROM attendance WHERE user_id = %s and date = %s"
    now_date = datetime.now().strftime('%Y-%m-%d')

    cursor.execute(query_check, (user_id, now_date))
    existing_record = cursor.fetchone()

    if not existing_record:
        # Insert a new record if the userId is not found
        now = datetime.now()
        time = now.strftime('%H:%M:%S')
        date = now.strftime('%Y-%m-%d')

        # Insert the new record into the database
        query_insert = "INSERT INTO attendance (user_id, name, date, in_time, out_time, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query_insert, (user_id, name, date, time, "", "A"))

        # Commit the changes
        conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def markCheckOutAttendances(user_id, name):

    # Connect to your MySQL database
    conn = get_database_connection()
    cursor = conn.cursor()

    # Create a table
    # create_table_query = """
    #     CREATE TABLE IF NOT EXISTS attendance (
    #         user_id INT Not Null,
    #         name VARCHAR(255) NOT Null,
    #         date DATE NOT NULL,
    #         in_time TIME,
    #         out_time TIME,
    #         status VARCHAR(7)
    #     )
    # """
    # cursor.execute(create_table_query)

    # getting date and time for checkout entry
    now = datetime.now()
    time = now.time()
    date = now.strftime('%Y-%m-%d')

    # check outtime is not marked by using date userId and name from database
    get_employee = "SELECT status from attendance where user_id = %s and name = %s and date = %s and in_time IS NOT NULL"
    cursor.execute(get_employee, (user_id, name, date))
    status = cursor.fetchone()

    if status[0] == "A":

        # Update the time for a specific entry
        update_query = "UPDATE attendance SET out_time = %s, status = %s WHERE user_id = %s and name = %s and date = %s and in_time IS NOT NULL"
        cursor.execute(update_query, (time, "P", user_id, name, date))

    # Commit the changes, Close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

