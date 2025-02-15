from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db  # Absolute import
from .models import Product, Category, User
from .schemas import Product as ProductSchema, Category as CategorySchema, UserCreate, Token
from .auth import get_current_user, create_access_token, authenticate_user
from datetime import timedelta

app = FastAPI()

# Auth endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Products endpoints
@app.get("/products", response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{id}", response_model=ProductSchema)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Categories endpoint
@app.get("/categories", response_model=list[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Protected endpoint example
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authenticated!"}