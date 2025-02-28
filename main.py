from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.db_utils import *
from base_models.models import *
import os
from routers import authStore, products, categories, orders, stores, image

IMAGE_BASE_DIR = os.getenv("IMAGE_BASE_DIR")

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

app.include_router(authStore.router)
app.include_router(categories.router)
app.include_router(image.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(stores.router)
