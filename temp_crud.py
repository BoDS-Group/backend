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

# create_table(table_name, attributes)
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