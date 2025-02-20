from fastapi import FastAPI, HTTPException, Depends, Header, status, APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from datetime import datetime, timedelta
import json
import uuid
import hashlib
from utils.db_utils import *
from base_models.models import *
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
IMAGE_BASE_DIR = os.getenv("IMAGE_BASE_DIR")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

app = FastAPI()
app.mount("/images", StaticFiles(directory=IMAGE_BASE_DIR), name="images")

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def encode_password(password: str) -> str:
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

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
    user = read_record('store_users', conditions={'email': email})
    role_data = read_record('roles', conditions={'id': user.get('id')})
    if role_data is None:
        return False
    return role_data.get('role') == role

def check_if_user_email_exists(email: str):
    user = read_record('store_users', conditions={'email': email})
    if user is None:
        return False
    return True

def check_if_user_data_exists(email: str):
    user_data = read_record('store_users', conditions={'email': email})
    if user_data.get('picture') is None:
        return False
    else:
        return True

def insert_user_registration_data(user_email: str, password: str, name: str):
    uuid_id = str(uuid.uuid4())
    insert_record('store_users', attributes=['id', 'email', 'name'], values=[uuid_id, user_email, name])
    insert_record('roles', attributes=['id', 'role'], values=[uuid_id, 'STORE_ADMIN'])
    insert_record('passwords', attributes=['id', 'password'], values=[uuid_id, password])

def insert_user_data(user_email: str, user: User):
    update_record('store_users', attributes=['name', 'picture'], values=[user.name, user.picture], conditions={'email': user_email})

def get_user(email: str):
    user_data = read_record('store_users', conditions={'email': email})
    return user_data

def update_product_img_id(img_id: str, product_id: str):
    product = read_record('products', conditions={'id': product_id})
    img_ids = product.get('images')
    img_ids.append(img_id)
    update_record('products', attributes=['images'], values=[img_ids], conditions={'id': product_id})

api = APIRouter(prefix="/api")

@api.post("/auth/store/google", response_model=Token)
async def google_auth(user: User):
    print(user)
    if not check_role(user.email):
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        if not check_if_user_data_exists(user.email):
            insert_user_data(user.email, user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": True}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api.post("/auth/store/register", response_model=Token)
async def register(user: UserRegister):
    print(user)
    if check_if_user_email_exists(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    insert_user_registration_data(user.email, encode_password(user.password), user.name)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": True}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
@api.post("/auth/store/login", response_model=Token)
async def login(user: UserLogin):
    print(user)
    if not check_role(user.email):
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_email = user.email
    user_password = user.password
    user_data = read_record('store_users', conditions={'email': user_email})
    if user_data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    password_hash = encode_password(user_password)
    password_data = read_record('passwords', conditions={'id': user_data.get('id')})
    if password_data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if password_data.get('password') != password_hash:
        raise HTTPException(status_code=401, detail="Unauthorized")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": True}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful" if password_data.get('password') == password_hash else "Login failed"
    }

@api.get("/users/me", response_model=User)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    user = get_user(current_user.email)
    return {
        "email": current_user.email,
        "name": user.get('name'),  
        "picture": user.get('picture'),  
        "address": user.get('address')
    }

@api.get("/products")
async def get_products(current_user: TokenData = Depends(is_admin_user)):
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

ITEMS_PER_PAGE = 10

@api.get("/products/recent/{page}")
async def get_recent_products(page: int):
    """
    Get a paginated list of the most recent products.
    
    Args:
        page (int): The page number to retrieve (starting from 1).
    
    Returns:
        list: A list of products for the requested page.
    """
    # Validate the page number
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be at least 1")

    try:
        products = read_by_page("products", page, ITEMS_PER_PAGE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {e}")

    # If no products are found, return an empty list
    if not products:
        return []

    # Return the paginated list of products
    return products

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

@api.get("/image/{image_id}")
async def get_image(image_id: str): #current_user: TokenData = Depends(is_admin_user) ommitted for testing
    image_metadata = read_record('images', conditions={'image_id': image_id})
    if image_metadata is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Constructing the URL for the image
    image_url = f"{BACKEND_URL}/images/{image_metadata['file_path']}/{image_metadata['file_name']}"
    
    return {"image_url": image_url}

@api.post("/image/upload")
async def upload_image(file: UploadFile = File(...), product_id: str = Form(...)): # current_user: TokenData = Depends(is_admin_user) ommitted for testing
    image_id = str(uuid.uuid4())
    
    # Create a directory structure based on the current date (e.g., 2023/10)
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    file_path = os.path.join(str(year), str(month))
    
    # Ensure the directory exists
    full_dir_path = os.path.join(IMAGE_BASE_DIR, file_path)
    os.makedirs(full_dir_path, exist_ok=True)
    
    # Save the file to the filesystem
    file_extension = os.path.splitext(file.filename)[1]  # Get the file extension
    file_name = f"{image_id}{file_extension}"  # Use the UUID as the file name
    full_file_path = os.path.join(full_dir_path, file_name)
    
    try:
        # Write the file to the filesystem
        with open(full_file_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image file: {e}")
    
    # Insert metadata into the database
    try:
        insert_record(
            'images',
            attributes=['image_id', 'file_path', 'file_name', 'mime_type'],
            values=[image_id, file_path, file_name, file.content_type]
        )
        update_product_img_id(image_id, product_id)
    except Exception as e:
        # Clean up the saved file if database insertion fails
        os.remove(full_file_path)
        raise HTTPException(status_code=500, detail=f"Failed to insert image metadata: {e}")
    
    return { "image_id": [image_id] }

@api.delete("/images/{image_id}") # current_user: TokenData = Depends(is_admin_user) ommitted for testing
async def delete_product_image(image_id: str):
    # Fetch image metadata from the database
    image_metadata = read_record('images', conditions={'image_id': image_id})
    if image_metadata is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Construct the full file path
    file_path = os.path.join(IMAGE_BASE_DIR, image_metadata['file_path'], image_metadata['file_name'])
    
    # Delete the image file from the filesystem
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete image file: {e}")
    else:
        raise HTTPException(status_code=404, detail="Image file not found")

    delete_record('images', conditions={'image_id': image_id})
    return {"message": "Image deleted successfully"}

app.include_router(api)

#TO DO: Orders : Create, Update, Read, Delete