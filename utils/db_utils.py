import re
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

ALLOWED_KEYWORDS = ['FOREIGN KEY', 'REFERENCES']

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def safe_identifier(identifier):
    """
    Validate that the identifier (table or column name) contains only allowed characters.
    Allowed: letters, digits, and underscores; must not start with a digit.
    Raises ValueError if the identifier is unsafe.
    """
    for keyword in ALLOWED_KEYWORDS:
        if keyword in identifier:
            return identifier
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
        raise ValueError(f"Unsafe identifier: {identifier}")
    return identifier

def build_where_clause(conditions):
    """
    Given a dictionary of conditions, build a SQL WHERE clause and a list of parameters.
    
    Example:
        conditions = {'id': 5, 'status': 'active'}
        returns ("WHERE id = %s AND status = %s", [5, 'active'])
    """
    if not conditions:
        return "", []
    clause_parts = []
    params = []
    for key, value in conditions.items():
        safe_key = safe_identifier(key)
        clause_parts.append(f"{safe_key} = %s")
        params.append(value)
    clause = " AND ".join(clause_parts)
    return f"WHERE {clause}", params

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a list of dictionaries.
    """
    return cursor.fetchall()

def dictfetchone(cursor):
    """
    Return one row from a cursor as a dictionary.
    """
    return cursor.fetchone()

def test_connection():
    """
    Test the database connection.
    
    Returns:
      - True if the connection is successful.
      - False if the connection fails.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        print(f"PostgreSQL connection successful | DB: {DB_NAME} | User: {DB_USER} |")
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

# --- Generalized CRUD Functions ---
def create_table(table_name, attributes):
    """
    Create a new table in the database.
    
    Parameters:
      - table_name (str): Name of the table.
      - attributes (dict): Dictionary of column names and their data types.
    
    Example:
      create_table('users', {'id': 'SERIAL PRIMARY KEY', 'username': 'VARCHAR(50)', 'password': 'VARCHAR(50)'})
    """
    table = safe_identifier(table_name)
    columns = ", ".join(f"{safe_identifier(col)} {dtype}" for col, dtype in attributes.items())
    query = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

def insert_record(table_name, attributes, values, returning_columns=None):
    """
    Insert a new row into the specified table.
    
    Parameters:
      - table_name (str): Name of the table.
      - attributes (list): List of column names.
      - values (list): List of corresponding values.
      - returning_columns (list, optional): List of columns to return (useful for PostgreSQL's RETURNING clause).
    
    Returns:
      - If returning_columns is provided, returns a list of dictionaries for the inserted row(s).
      - Otherwise, returns None.
    """
    if len(attributes) != len(values):
        raise ValueError("Attributes and values must have the same length.")

    table = safe_identifier(table_name)
    cols = ", ".join(safe_identifier(attr) for attr in attributes)
    placeholders = ", ".join(["%s"] * len(values))
    
    query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    if returning_columns:
        ret_cols = ", ".join(safe_identifier(col) for col in returning_columns)
        query += f" RETURNING {ret_cols}"

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, values)
            if returning_columns:
                return dictfetchall(cursor)
    return None

def read_records(table_name, attributes=None, conditions=None):
    """
    Retrieve multiple rows from the specified table.
    
    Parameters:
      - table_name (str): Name of the table.
      - attributes (list, optional): List of columns to retrieve. If not provided, selects all columns (*).
      - conditions (dict, optional): A dictionary of conditions to build the WHERE clause.
    
    Returns:
      - A list of dictionaries representing the rows.
    """
    table = safe_identifier(table_name)
    select_clause = ", ".join(safe_identifier(attr) for attr in attributes) if attributes else "*"
    query = f"SELECT {select_clause} FROM {table} "
    
    where_clause, params = build_where_clause(conditions)
    query += where_clause

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return dictfetchall(cursor)

def read_record(table_name, attributes=None, conditions=None):
    """
    Retrieve a single row from the specified table.
    
    Parameters:
      - table_name (str): Name of the table.
      - attributes (list, optional): List of columns to retrieve. If not provided, selects all columns.
      - conditions (dict, optional): Conditions for the WHERE clause.
    
    Returns:
      - A dictionary representing the row, or None if no row is found.
    """
    table = safe_identifier(table_name)
    select_clause = ", ".join(safe_identifier(attr) for attr in attributes) if attributes else "*"
    query = f"SELECT {select_clause} FROM {table} "
    
    where_clause, params = build_where_clause(conditions)
    query += where_clause

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return dictfetchone(cursor)

def update_record(table_name, attributes, values, conditions, returning_columns=None):
    """
    Update rows in the specified table.
    
    Parameters:
      - table_name (str): Name of the table.
      - attributes (list): List of columns to update.
      - values (list): List of new values corresponding to the attributes.
      - conditions (dict): Conditions to filter which rows to update.
      - returning_columns (list, optional): Columns to return after the update.
    
    Returns:
      - If returning_columns is provided, returns a list of dictionaries representing the updated row(s).
      - Otherwise, returns None.
    """
    if len(attributes) != len(values):
        raise ValueError("Attributes and values must have the same length.")

    table = safe_identifier(table_name)
    set_clause = ", ".join(f"{safe_identifier(attr)} = %s" for attr in attributes)
    query = f"UPDATE {table} SET {set_clause} "

    where_clause, condition_params = build_where_clause(conditions)
    query += where_clause

    params = values + condition_params
    if returning_columns:
        ret_cols = ", ".join(safe_identifier(col) for col in returning_columns)
        query += f" RETURNING {ret_cols}"

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if returning_columns:
                return dictfetchall(cursor)
    return None

def delete_record(table_name, conditions, returning_columns=None):
    """
    Delete rows from the specified table.
    
    Parameters:
      - table_name (str): Name of the table.
      - conditions (dict): Conditions to identify which rows to delete.
      - returning_columns (list, optional): Columns to return from the deleted rows.
    
    Returns:
      - If returning_columns is provided, returns a list of dictionaries representing the deleted row(s).
      - Otherwise, returns None.
    """
    table = safe_identifier(table_name)
    query = f"DELETE FROM {table} "
    
    where_clause, params = build_where_clause(conditions)
    query += where_clause
    
    if returning_columns:
        ret_cols = ", ".join(safe_identifier(col) for col in returning_columns)
        query += f" RETURNING {ret_cols}"

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if returning_columns:
                return dictfetchall(cursor)
    return None