# Queries for products
GET_ALL_PRODUCTS = """
    SELECT id, name, description, price, category_id
    FROM products;
"""

GET_PRODUCT_BY_ID = """
    SELECT id, name, description, price, category_id
    FROM products
    WHERE id = %s;
"""

# Queries for categories
GET_ALL_CATEGORIES = """
    SELECT id, name
    FROM categories;
"""

# Queries for users
GET_USER_BY_USERNAME = """
    SELECT id, username, password_hash, auth_level
    FROM users
    WHERE username = %s;
"""