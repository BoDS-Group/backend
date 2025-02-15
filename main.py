from fastapi import FastAPI, Depends, HTTPException, status
from .database import get_db
from .queries import GET_ALL_PRODUCTS, GET_PRODUCT_BY_ID, GET_ALL_CATEGORIES
from .schemas import Product, Category, UserCreate, Token
from .auth import get_current_user, create_access_token, authenticate_user
from datetime import timedelta
import psycopg2

app = FastAPI()

# Auth endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserCreate, db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Products endpoints
@app.get("/products", response_model=list[Product])
def get_products(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(GET_ALL_PRODUCTS)
    products = cursor.fetchall()
    cursor.close()
    return products

@app.get("/products/{id}", response_model=Product)
def get_product(id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(GET_PRODUCT_BY_ID, (id,))
    product = cursor.fetchone()
    cursor.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Categories endpoint
@app.get("/categories", response_model=list[Category])
def get_categories(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(GET_ALL_CATEGORIES)
    categories = cursor.fetchall()
    cursor.close()
    return categories

# Protected endpoint example
@app.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, you are authenticated!"}