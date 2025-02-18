from utils.db_utils import *
import uuid

# Define the table name and attributes
table_name = 'roles'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'email': 'VARCHAR(255) NOT NULL',
    'role': 'VARCHAR(50) NOT NULL'
}

table_name = 'store_users'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'name': 'VARCHAR(127) NOT NULL',
    'picture': 'VARCHAR(255)',
    'given_name': 'VARCHAR(63) NOT NULL',
    'family_name': 'VARCHAR(63) NOT NULL',
    'adress': 'VARCHAR(255)',
    'FOREIGN KEY (id)': 'REFERENCES roles(id)'
}

table_name = 'categories'
attributes = {
    'id': 'SERIAL PRIMARY KEY',
    'name': 'VARCHAR(255) NOT NULL',
    'parent': 'INTEGER REFERENCES categories(id)',
    'properties': 'JSONB'
}

table_name = 'products'
attributes = {
    'id': 'SERIAL PRIMARY KEY',
    'title': 'VARCHAR(255) NOT NULL',
    'description': 'TEXT',
    'price': 'NUMERIC(10, 2) NOT NULL',
    'images': 'TEXT[]',
    'category': 'INTEGER REFERENCES categories(id)',
    'properties': 'JSONB',
    'created_at': 'TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP',
    'updated_at': 'TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP'
}

table_name = 'orders'
attributes = {
    'id': 'SERIAL PRIMARY KEY',
    'line_items': 'JSONB',
    'name': 'VARCHAR(255)',
    'email': 'VARCHAR(255)',
    'city': 'VARCHAR(255)',
    'postal_code': 'VARCHAR(20)',
    'street_address': 'VARCHAR(255)',
    'country': 'VARCHAR(255)',
    'paid': 'BOOLEAN',
    'created_at': 'TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP',
    'updated_at': 'TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP'
}

create_table(table_name, attributes)
print("Table Name:", table_name)

# Insert a record
# record_id = str(uuid.uuid4())
# email = 'hamidurrk@gmail.com'
# role = 'STORE_ADMIN'

# insert_record(
#     table_name,
#     attributes=['id', 'email', 'role'],
#     values=[record_id, email, role]
# )

# print(f"Inserted record with ID: {record_id}")
# existing_user = read_record('roles', conditions={'email': "hamidurrk@gmail.com"})
# print(existing_user.get('role'))