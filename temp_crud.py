from utils.db_utils import *
import uuid
import json
import hashlib
import pandas as pd

def encode_password(password: str) -> str:
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

# Define the table name and attributes
table_name = 'roles'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'role': 'VARCHAR(50) NOT NULL',
    'FOREIGN KEY (id)': 'REFERENCES store_users(id)'
}

table_name = 'store_users'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'email': 'VARCHAR(255) NOT NULL',
    'name': 'VARCHAR(127) NOT NULL',
    'picture': 'VARCHAR(255)',
    'address': 'VARCHAR(255)',
    'store_id': 'UUID',
    'FOREIGN KEY (store_id)': 'REFERENCES stores(id)'
}

table_name = 'categories'
attributes = {
    'id': 'SERIAL PRIMARY KEY',
    'name': 'VARCHAR(255) NOT NULL',
    'parent': 'INTEGER REFERENCES categories(id)',
    'properties': 'JSONB'
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

table_name = 'passwords'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'password': 'VARCHAR(255) NOT NULL',
    'FOREIGN KEY (id)': 'REFERENCES store_users(id)'
}

table_name = 'system_admin'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'name': 'VARCHAR(255) NOT NULL',
    'email': 'VARCHAR(255) NOT NULL',
    'password': 'VARCHAR(255) NOT NULL',
    'phone_number': 'VARCHAR',
    'created_at': 'TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP',
    'updated_at': 'TIMESTAMPTZ',
    'deleted_at': 'TIMESTAMPTZ'
}

table_name = 'cities'
attributes = {
    'id': 'SERIAL PRIMARY KEY',
    'city': 'VARCHAR(50) NOT NULL',
    'lat': 'VARCHAR(20)',
    'lng': 'VARCHAR(20)'
}

table_name = 'stores'
attributes = {
    'id': 'UUID PRIMARY KEY',
    'name': 'VARCHAR(127) NOT NULL',
    'description': 'TEXT',
    'city': 'VARCHAR(50) NOT NULL',
    'location': 'VARCHAR(255) NOT NULL',
    'image': 'UUID',
    'sustainability_achievement': 'TEXT',
    'home_delivery': 'BOOLEAN'
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
    'store_id': 'UUID REFERENCES stores(id)',
    'barcode': 'VARCHAR',
    'carbon_savings': 'VARCHAR(127)',
    'status': 'BOOLEAN',
    'created_at': 'TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP',
    'updated_at': 'TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP'
}

# attributes = [
#         "store_users.id AS user_id", 
#         "store_users.email", 
#         "store_users.name AS user_name", 
#         "stores.id AS store_id", 
#         "stores.name AS store_name", 
#         "stores.description", 
#         "stores.city", 
#         "stores.location"
#     ]
# tables = ["store_users", "stores", "roles"]
# join_conditions = ["store_users.store_id = stores.id", "store_users.id = roles.id"]
# conditions = {"roles.role": "STORE_ADMIN"}

# system_admins_with_stores = read_joined_records(tables, join_conditions, attributes, conditions)
# print(system_admins_with_stores)

# delete_all_records("products")
# delete_all_records("categories")
# delete_all_records("images")
# delete_all_records("orders")
# # delete_all_records("passwords")
# delete_all_records("roles")
# delete_all_records("store_users")
# delete_all_records("stores")

# create_table(table_name, attributes)
# print("Table Name:", table_name)

# alter_table(table_name='products', action='ADD', column_name='store_id', column_type='UUID REFERENCES stores(id)')
# alter_table(table_name='products', action='ADD', column_name='barcode', column_type='VARCHAR')
# alter_table(table_name='products', action='ADD', column_name='carbon_savings', column_type='VARCHAR(127)')
# alter_table(table_name='products', action='ADD', column_name='status', column_type='BOOLEAN')
# print("Table Name:", table_name)

# drop_table('stores')

# csv_file_path = 'data/fi.csv'
# cities_data = pd.read_csv(csv_file_path)

# # Insert data into the cities table
# for index, row in cities_data.iterrows():
#     city = row['city']
#     lat = row['lat']
#     lng = row['lng']
#     insert_record(
#         table_name,
#         attributes=['city', 'lat', 'lng'],
#         values=[city, lat, lng]
#     )

# print("Inserted data from CSV into cities table")

# record_id = str(uuid.uuid4())
# name = 'Md Hamidur Rahman Khan'
# email = 'hrk.admin@sc.com'
# password = encode_password('test1234')  
# phone_number = '1234567890'

# insert_record(
#     table_name,
#     attributes=['id', 'name', 'email', 'password', 'phone_number'],
#     values=[record_id, name, email, password, phone_number]
# )

# print(f"Inserted test entry with ID: {record_id}")

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

# def get_all_cities():
#     cities = read_column(table_name='cities', column_name='city')
#     return cities

# print(get_all_cities())