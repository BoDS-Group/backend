# Second Chance Backend

This repository contains the backend code for the Second Chance project. It is built using FastAPI and PostgreSQL for managing user roles, store users, categories, products, and orders.

## Requirements

- Python 3.8+
- PostgreSQL

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/BoDS-Group/backend
    cd backend
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    ./venv/Scripts/activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the root directory:
    ```
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    ```

5. Start the PostgreSQL Database Server (if not already running) using pgAdmin or command line tools. 

6. Restore the database from the backup file `sc-test-backup.sql` under `/db_backup` directory using pgAdmin or command line tools.

5. Run the FastAPI application:
    ```sh
    uvicorn main:app --reload
    ```

## API Endpoints

### Authentication

#### Google Authentication
- **Endpoint:** `/api/auth/google`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "name": "User Name",
        "picture": "http://example.com/picture.jpg",
        "given_name": "User",
        "family_name": "Name"
    }
    ```
- **Response:**
    ```json
    {
        ":"access_token "your_access_token",
        "token_type": "bearer"
    }
    ```

### Users

#### Get Current User
- **Endpoint:** `/api/users/me`
- **Method:** `GET`
- **Response:**
    ```json
    {
        "email": "user@example.com",
        "name": "User Name",
        "picture": "http://example.com/picture.jpg",
        "given_name": "User",
        "family_name": "Name"
    }
    ```

### Products

#### Get All Products
- **Endpoint:** `/api/products`
- **Method:** `GET`
- **Response:** List of products

#### Get a Single Product
- **Endpoint:** `/api/products/{product_id}`
- **Method:** `GET`
- **Response:** Product details

#### Create a Product
- **Endpoint:** `/api/products`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "title": "Sample Product",
        "description": "This is a sample product description.",
        "price": 19.99,
        "images": ["image1.jpg", "image2.jpg"],
        "category": 1,
        "properties": {"color": "red", "size": "M"}
    }
    ```
- **Response:**
    ```json
    {
        "message": "Product created successfully"
    }
    ```

#### Update a Product
- **Endpoint:** `/api/products/{product_id}`
- **Method:** `PUT`
- **Request Body:** Partial or full product details to update
- **Response:**
    ```json
    {
        "message": "Product updated successfully"
    }
    ```

#### Delete a Product
- **Endpoint:** `/api/products/{product_id}`
- **Method:** `DELETE`
- **Response:**
    ```json
    {
        "message": "Product deleted successfully"
    }
    ```

### Categories

#### Get All Categories
- **Endpoint:** `/api/categories`
- **Method:** `GET`
- **Response:** List of categories

#### Create a Category
- **Endpoint:** `/api/categories`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "name": "Category Name",
        "parent": null,
        "properties": {"key": "value"}
    }
    ```
- **Response:**
    ```json
    {
        "message": "Category created successfully"
    }
    ```

#### Update a Category
- **Endpoint:** `/api/categories/{category_id}`
- **Method:** `PUT`
- **Request Body:** Partial or full category details to update
- **Response:**
    ```json
    {
        "message": "Category updated successfully"
    }
    ```

#### Delete a Category
- **Endpoint:** `/api/categories/{category_id}`
- **Method:** `DELETE`
- **Response:**
    ```json
    {
        "message": "Category deleted successfully"
    }
    ```

...TO BE CONTINUED

## Database Schema

### Tables

- **roles**
    - `id`: UUID PRIMARY KEY
    - `email`: VARCHAR(255) NOT NULL
    - `role`: VARCHAR(50) NOT NULL

- **store_users**
    - `id`: UUID PRIMARY KEY
    - `name`: VARCHAR(127) NOT NULL
    - `picture`: VARCHAR(255)
    - `given_name`: VARCHAR(63) NOT NULL
    - `family_name`: VARCHAR(63) NOT NULL
    - `address`: VARCHAR(255)
    - `FOREIGN KEY (id)`: REFERENCES roles(id)

- **categories**
    - `id`: SERIAL PRIMARY KEY
    - `name`: VARCHAR(255) NOT NULL
    - `parent`: INTEGER REFERENCES categories(id)
    - `properties`: JSONB

- **products**
    - `id`: SERIAL PRIMARY KEY
    - `title`: VARCHAR(255) NOT NULL
    - `description`: TEXT
    - `price`: NUMERIC(10, 2) NOT NULL
    - `images`: TEXT[]
    - `category`: INTEGER REFERENCES categories(id)
    - `properties`: JSONB
    - `created_at`: TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    - `updated_at`: TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP

- **orders**
    - `id`: SERIAL PRIMARY KEY
    - `line_items`: JSONB
    - `name`: VARCHAR(255)
    - `email`: VARCHAR(255)
    - `city`: VARCHAR(255)
    - `postal_code`: VARCHAR(20)
    - `street_address`: VARCHAR(255)
    - `country`: VARCHAR(255)
    - `paid`: BOOLEAN
    - `created_at`: TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    - `updated_at`: TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP

...TO BE CONTINUED
