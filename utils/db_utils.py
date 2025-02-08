import re
from django.db import connection

def safe_identifier(identifier):
    """
    Validate that the identifier (table or column name) contains only allowed characters.
    Allowed: letters, digits, and underscores; must not start with a digit.
    Raises ValueError if the identifier is unsafe.
    """
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
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    """
    Return one row from a cursor as a dictionary.
    """
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# --- Generalized CRUD Functions ---

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

    with connection.cursor() as cursor:
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

    with connection.cursor() as cursor:
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

    with connection.cursor() as cursor:
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

    with connection.cursor() as cursor:
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

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if returning_columns:
            return dictfetchall(cursor)
    return None
