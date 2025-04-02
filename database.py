import mysql.connector;
from datetime import datetime;

from user import User;

def get_database_connection():
    # Return a connection and cursor to the database
    return mysql.connector.connect(host="localhost",
        user="root",
        password="root",
        database="attendance_py")

def generate_new_user(company_id,password,name):

    conn = get_database_connection()
    cursor = conn.cursor()

    # # Create a table
    # create_table_query = """
        # CREATE TABLE IF NOT EXISTS users_table (
        #     user_id INT PRIMARY KEY,
        #     password VARCHAR(15) NOT Null,
        #     name VARCHAR(30) NOT NULL,
        #     type VARCHAR(10) NOT NULL
        # )
    #     """
    # cursor.execute(create_table_query)

    insert_data_query = """
        INSERT INTO users_table (user_id, password, name, type)
        VALUES (%s, %s, %s, %s)
    """

    # insert data andexecute query
    user_data = (company_id, password, name, "User")
    cursor.execute(insert_data_query, user_data)

    # Commit the changes to the database
    conn.commit()

    # Closing the connection
    cursor.close()
    conn.close() 

    return company_id

def get_all_users():
    conn = get_database_connection()
    cursor = conn.cursor()

    # query for fetching all records
    get_query_for_users = "SELECT * FROM users_table"
    cursor.execute(get_query_for_users)
    users_data = cursor.fetchall()

    # Convert data into list of User objects
    users = []
    for user_data in users_data:
        user_id, password, name, type = user_data
        user = User(user_id, name, password, type)
        users.append(user)

    # Closing the connection
    cursor.close()
    conn.close()

    return users

def get_all_attendance_records():
    
    conn = get_database_connection()
    cursor = conn.cursor()

    # query for fetching all records
    get_query_for_recorde = "SELECT * from attendance"
    cursor.execute(get_query_for_recorde)
    records = cursor.fetchall()

    # Closing the connection
    cursor.close()
    conn.close() 

    return records

def get_all_entries_by_user_id(user_id):

    conn = get_database_connection()
    cursor = conn.cursor()

    # query for fetching all records of one user
    get_query_for_entries = "SELECT * from attendance where user_id = %s"
    cursor.execute(get_query_for_entries,(user_id,))
    users = cursor.fetchall()

    # Closing the connection
    cursor.close()
    conn.close() 

    return users

def get_records_between_dates(user_id, sdate, edate):
    # database connection code
    conn = get_database_connection()
    cursor = conn.cursor()

    # taking data for perticular name and dates between
    select_query = "SELECT * FROM attendance where user_id = %s and date between %s and %s"
    cursor.execute(select_query, (user_id, sdate, edate))
    records = cursor.fetchall()

    # Closing the connection
    cursor.close()
    conn.close() 

    return records
