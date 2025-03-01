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
    picture: Optional[str] = None

class SysAdminUser(BaseModel):
    email: str
    name: str
    phone_number: Optional[str] = None

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

class OrderCreate(BaseModel):
    line_items: dict
    name: str
    email: str
    city: str
    postal_code: str
    street_address: str
    country: str
    paid: bool

class OrderUpdate(BaseModel):
    line_items: Optional[dict] = None
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    street_address: Optional[str] = None
    country: Optional[str] = None
    paid: bool

class CategoryCreate(BaseModel):
    name: str
    parent: Optional[int] = None
    properties: Optional[dict] = None
    
class StoreCreate(BaseModel):
    storeName: str
    storeDescription: Optional[str] = None
    city: str
    storeLocation: str
    storeAdminName: str
    storeAdminEmail: str