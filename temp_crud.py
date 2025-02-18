from utils.db_utils import *
import uuid
import json

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

# create_table(table_name, attributes)
# print("Table Name:", table_name)

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

# # Insert a record into the categories table
# category_name = 'Uncategorized'
# parent_category = None  # Assuming this is a top-level category
# properties = properties = {
# }  # Assuming no additional properties

# # Convert properties dictionary to JSON string
# properties_json = json.dumps(properties)

# insert_record(
#     'categories',
#     attributes=['name', 'parent', 'properties'],
#     values=[category_name, parent_category, properties_json]
# )

# print("Inserted category with name:", category_name)

# # Insert a record into the products table
# title = 'Sample Product'
# description = 'This is a sample product description.'
# price = 19.99
# images = ['image1.jpg', 'image2.jpg']
# category = 1  # Assuming category with id 1 exists
# properties = {'color': 'red', 'size': 'M'}

# # Convert properties dictionary to JSON string
# properties_json = json.dumps(properties)

# insert_record(
#     'products',
#     attributes=['title', 'description', 'price', 'images', 'category', 'properties'],
#     values=[title, description, price, images, category, properties_json]
# )

# print("Inserted product with title:", title)

# delete_record('categories', conditions={'id': 1})
# print("Deleted category with ID: 1")