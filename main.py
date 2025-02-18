# filepath: /path/to/your/fastapi/app/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class User(BaseModel):
    email: str
    name: str
    picture: str
    given_name: str
    family_name: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

@app.post("/api/auth/google", response_model=Token)
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
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=User)
async def read_users_me(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ")[1]
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(payload)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user(token_data.email)
    return {
        "email": token_data.email,
        "name": user.get('name'),  
        "picture": user.get('picture'),  
        "given_name": user.get('given_name'),  
        "family_name": user.get('family_name')  
    }
    
