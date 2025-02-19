from fastapi import FastAPI, HTTPException, Depends, Header, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import json
from utils.db_utils import *

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    is_admin: Optional[bool] = False

class User(BaseModel):
    email: str
    name: str
    picture: str
    given_name: str
    family_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    images: Optional[list[str]] = None
    category: int
    properties: Optional[dict] = None

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    images: Optional[list[str]] = None
    category: Optional[int] = None
    properties: Optional[dict] = None

class CategoryCreate(BaseModel):
    name: str
    parent: Optional[int] = None
    properties: Optional[dict] = None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, is_admin=is_admin)
    except JWTError:
        raise credentials_exception
    return token_data

def is_admin_user(current_user: TokenData = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

def check_role(email: str, role: str = 'STORE_ADMIN'):
    user = read_record('roles', conditions={'email': email})
    if user is None:
        return False
    return user.get('role') == role

def check_if_user_data_exists(email: str):
    user = read_record('roles', conditions={'email': email})
    user_data = read_record('store_users', conditions={'id': user.get('id')})
    if user_data is not None:
        return user.get('id')
    else:
        return None

def insert_user(user_id: str, user: User):
    user_id = read_record('roles', conditions={'email': user.email}).get('id')
    insert_record('store_users', attributes=['id', 'name', 'picture', 'given_name', 'family_name'], values=[user_id, user.name, user.picture, user.given_name, user.family_name])

def get_user(email: str):
    user = read_record('roles', conditions={'email': email})
    user_data = read_record('store_users', conditions={'id': user.get('id')})
    return user_data

api = APIRouter(prefix="/api")

@api.post("/auth/google", response_model=Token)
async def google_auth(user: User):
    print(user)
    if not check_role(user.email):
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        user_id = check_if_user_data_exists(user.email)
        if not user_id:
            insert_user(user_id, user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": True}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def validate_user(email: str, password: str) -> bool:
    """
    Validates a user's email and password.
    
    Args:
        email (str): The user's email.
        password (str): The user's plaintext password.
    
    Returns:
        bool: True if the email and password are valid, False otherwise.
    """
    # Fetch the user's data from the 'store_users' table
    user_data = read_record('store_users', conditions={'adress': email})
    if user_data is None:
        return False  # User does not exist in the 'store_users' table

    # Retrieve the stored hashed password
    stored_hashed_password = user_data.get('password_hash')
    if stored_hashed_password is None:
        return False  # No password hash stored for the user

    # Verify the provided password against the stored hash
    try:
        # Decode the stored hash to get the original password (for comparison)
        decoded_password = jwt.decode(stored_hashed_password, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_password.get('password') != password:
            return False  # Passwords do not match
    except JWTError:
        return False  # Invalid token or hash

    return True  # Email and password are valid

@api.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    # Validate the user's email and password
    if not validate_user(user.email, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check the user's role (optional, if needed)
    if not check_role(user.email):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Insert user data if it doesn't exist (optional, if needed)
    user_id = check_if_user_data_exists(user.email)
    if not user_id:
        insert_user(user_id, user)

    # Generate an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": True}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api.get("/users/me", response_model=User)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    user = get_user(current_user.email)
    return {
        "email": current_user.email,
        "name": user.get('name'),  
        "picture": user.get('picture'),  
        "given_name": user.get('given_name'),  
        "family_name": user.get('family_name')  
    }

@api.get("/products")
#async def get_products(current_user: TokenData = Depends(is_admin_user)):
async def get_products():
    products = read_records('products')
    # print(products)
    return products

# Get a single product
@api.get("/products/{product_id}")
async def get_product(product_id: str, current_user: TokenData = Depends(is_admin_user)):
    product = read_record('products', conditions={'id': product_id})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    print(product)
    return product 

@api.post("/products")
async def create_product(product: ProductCreate,current_user: TokenData = Depends(is_admin_user)):
    # Convert properties dictionary to JSON string
    properties_json = json.dumps(product.properties) if product.properties else None

    # Insert the new product into the database
    insert_record(
        'products',
        attributes=['title', 'description', 'price', 'images', 'category', 'properties'],
        values=[product.title, product.description, product.price, product.images, product.category, properties_json]
    )
    return {"message": "Product created successfully"}

@api.put("/products/{product_id}")
async def update_product(product_id: str, product: ProductUpdate, current_user: TokenData = Depends(is_admin_user)):
    # Convert properties dictionary to JSON string if it exists
    properties_json = json.dumps(product.properties) if product.properties else None

    # Create a dictionary of the fields to update
    update_data = {k: v for k, v in product.dict().items() if v is not None}
    if 'properties' in update_data:
        update_data['properties'] = properties_json

    print(update_data)
    # Update the product in the database
    update_record(
        'products',
        conditions={'id': product_id},
        attributes=update_data.keys(),
        values=list(update_data.values())
    )
    return {"message": "Product updated successfully"}

@api.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user: TokenData = Depends(is_admin_user)):
    delete_record('products', conditions={'id': product_id})
    return {"message": "Product deleted successfully"}

@api.get("/categories")
async def get_products(current_user: TokenData = Depends(is_admin_user)):
    categories = read_records('categories')
    print(categories)
    return categories

@api.put("/categories/{category_id}")
async def update_category(category_id: str, category: CategoryCreate, current_user: TokenData = Depends(is_admin_user)):
    # Convert properties dictionary to JSON string if it exists
    properties_json = json.dumps(category.properties) if category.properties else None

    # Create a dictionary of the fields to update
    update_data = {k: v for k, v in category.dict().items() if v is not None}
    if 'properties' in update_data:
        update_data['properties'] = properties_json
    # Update the category in the database
    update_record(
        'categories',
        conditions={'id': category_id},
        attributes=update_data.keys(),
        values=list(update_data.values())
    )
    return {"message": "Category updated successfully"}

@api.post("/categories")
async def create_category(category: CategoryCreate, current_user: TokenData = Depends(is_admin_user)):
    # Convert properties dictionary to JSON string
    properties_json = json.dumps(category.properties) if category.properties else None
    # if any properties contain empty strings, convert them to empty objects
    properties_json = json.dumps({k: v for k, v in json.loads(properties_json).items() if v})
    
    # Insert the new category into the database
    insert_record(
        'categories',
        attributes=['name', 'parent', 'properties'],
        values=[category.name, category.parent, properties_json]
    )
    return {"message": "Category created successfully"}

@api.delete("/categories/{category_id}")
async def delete_category(category_id: str, current_user: TokenData = Depends(is_admin_user)):
    delete_record('categories', conditions={'id': category_id})
    return {"message": "Category deleted successfully"}

app.include_router(api)

#products properties in json data
#TO DO: Implement image upload to database
#Something to get images
#image endpoint based on id : Create, Read, Delete
#TO DO: Orders : Create, Update, Read, Delete
#TO DO: /auth/ : Implement user email and password login system