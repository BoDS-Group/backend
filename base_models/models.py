from pydantic import BaseModel
from typing import Optional

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

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

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