import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Function to establish a connection to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

# Function to execute a single query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to load a single CSV file into the database
def load_csv_to_db(connection, csv_file, table_name):
    # Load CSV file into a DataFrame
    df = pd.read_csv(csv_file, delimiter=';', header=0, dtype=str)
    
    # Replace missing values with None
    df = df.where(pd.notnull(df), None)
    
    # Create a list of tuples from the DataFrame values
    records = df.values.tolist()
    
    # Create the SQL query to insert data
    insert_query = f"""
    INSERT INTO {table_name} (
        `id`, `start`, `end`, `Polluant`, `value`, `measure_unit`, 
        `verif`, `valid`, `name`, `municipality`, `latitude`, `longitude`, `altitude`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Insert data into the database
    cursor = connection.cursor()
    try:
        cursor.executemany(insert_query, records)
        connection.commit()
        print(f"{csv_file} data loaded successfully into {table_name}")
    except Error as e:
        print(f"The error '{e}' occurred while loading {csv_file}")

# Main function to load all CSV files in a directory into the same table
def load_all_csv_files_to_db(directory_path, table_name, db_details):
    connection = create_connection(
        db_details["host_name"], 
        db_details["user_name"], 
        db_details["user_password"], 
        db_details["db_name"]
    )
    
    if connection:
        for filename in os.listdir(directory_path):
            if filename.endswith(".csv"):
                csv_file = os.path.join(directory_path, filename)
                load_csv_to_db(connection, csv_file, table_name)
        
        connection.close()
        print("All CSV files loaded successfully")

# Database connection details
db_details = {
    "host_name": "localhost",
    "user_name": "root",
    "user_password": "1995",
    "db_name": "pollution_forecast_data"
}

# Directory containing CSV files
directory_path = "C:/Users/Administrateur/Documents/intermediate_csvs"

# Name of the table to load data into
table_name = "data_from_xml"


# Load all CSV files into the database table
load_all_csv_files_to_db(directory_path, table_name, db_details)