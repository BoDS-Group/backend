from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.db_utils import *
from base_models.models import *
import os
from routers import auth_admin, admin, auth_store, products, categories, orders, stores, image

IMAGE_BASE_DIR = os.getenv("IMAGE_BASE_DIR")

app = FastAPI()
app.mount("/images", StaticFiles(directory=IMAGE_BASE_DIR), name="images")

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_admin.router)
app.include_router(admin.router)
app.include_router(auth_store.router)
app.include_router(categories.router)
app.include_router(image.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(stores.router)
