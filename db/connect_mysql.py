import os
import mysql.connector
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv() 

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "pune@1234"), 
        database=os.getenv("DB_NAME", "library_db")
    )

# CHANGE 1: Set params default to an empty tuple () instead of None
def run_query(query, params=()):
    """Executes a SELECT query and returns the results as a Pandas DataFrame."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    # CHANGE 2: Check if description is not None before iterating
    if cursor.description:
        column_names = [col[0] for col in cursor.description]
    else:
        column_names = []
    
    cursor.close()
    conn.close()
    
    # Create the DataFrame manually
    return pd.DataFrame(data, columns=column_names)

# CHANGE 3: Set params default to an empty tuple () instead of None
def execute_query(query, params=()):
    """Executes INSERT, UPDATE, or DELETE queries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        st.error(f"Database Error: {err}")
        success = False
    finally:
        cursor.close()
        conn.close()
    return success

def execute_transaction(queries_and_params):
    """
    Executes a list of queries as a single transaction.
    Takes a list of tuples: [(query1, params1), (query2, params2)]
    Returns (True, None) on success, or (False, error_message) on failure.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Loop through and execute every query in the transaction
        for query, params in queries_and_params:
            cursor.execute(query, params)
        
        # If all succeed, commit the changes permanently
        conn.commit()
        success = True
        error_msg = None
    except Exception as e:
        # If anything fails, undo all partial changes
        conn.rollback()
        success = False
        error_msg = str(e)
    finally:
        cursor.close()
        conn.close()
        
    return success, error_msg