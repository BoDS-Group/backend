# from ..utils.db_utils import *
from db_utils import *
import pandas as pd
from collections import Counter
import os
import uuid
from datetime import datetime
import requests
import asyncio
from starlette.datastructures import UploadFile
from tempfile import SpooledTemporaryFile


IMAGE_BASE_DIR = os.getenv("IMAGE_BASE_DIR")

def update_product_img_id(img_id: str, product_id: str):
    product = read_record('products', conditions={'id': product_id})
    img_ids = product.get('images')
    if img_ids is None:
        img_ids = []
    img_ids.append(img_id)
    update_record('products', attributes=['images'], values=[img_ids], conditions={'id': product_id})

async def upload_image(file, product_id: str, mime_type: str): 
    image_id = str(uuid.uuid4())
    # print(product_id)
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    file_path = os.path.join(str(year), str(month))
    
    full_dir_path = os.path.join(IMAGE_BASE_DIR, file_path)
    os.makedirs(full_dir_path, exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1]  
    file_name = f"{image_id}{file_extension}"  
    full_file_path = os.path.join(full_dir_path, file_name)
    
    try:
        with open(full_file_path, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        print(f"Failed to save image file: {e}")
    
    try:
        insert_record(
            'images',
            attributes=['image_id', 'file_path', 'file_name', 'mime_type'],
            values=[image_id, file_path, file_name, mime_type]
        )
        update_product_img_id(image_id, product_id)
    except Exception as e:
        os.remove(full_file_path)
        print(f"Failed to insert image metadata: {e}")
    

async def download_and_upload_image(image_url: str, product_id: str):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        file = SpooledTemporaryFile()
        file.write(response.content)
        file.seek(0)

        mime_type = response.headers.get('Content-Type', 'application/octet-stream')
        
        upload_file = UploadFile(
            filename=os.path.basename(image_url),
            file=file,
        )
        result = await upload_image(upload_file, product_id, mime_type)
        return result
    except Exception as e:
        print(f"Failed to download or upload image: {e}")
        return None

def load_and_print_data(file_path, columns):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    
    data = pd.read_csv(file_path)
    selected_data = data[columns]
    print(selected_data.head(200))

def analyze_categories(file_path, column):
    data = pd.read_csv(file_path)
    categories = data[column].dropna().apply(eval)  
    all_categories = [category for sublist in categories for category in sublist]
    category_counts = Counter(all_categories)
    sorted_category_counts = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    
    with open('./data/category_frequency.txt', 'w') as file:
        file.write("Category Frequency Ranking:\n")
        for category, count in sorted_category_counts:
            file.write(f"{category}: {count}\n")

def check_rows_without_top_categories(file_path, column):
    with open('./data/category_frequency.txt', 'r') as file:
        lines = file.readlines()[1:31]  
        top_categories = [line.split(':')[0].strip() for line in lines]

    data = pd.read_csv(file_path)
    categories = data[column].dropna().apply(eval)  

    count = 0
    for category_list in categories:
        if not any(category in top_categories for category in category_list):
            count += 1

    print(f"Number of rows that do not include any of the top 20 categories: {count}")

def insert_top_categories_to_db():
    with open('./data/category_frequency.txt', 'r') as file:
        lines = file.readlines()[1:31]  # Read the first 30 categories
        top_categories = [line.split(':')[0].strip() for line in lines]

    for category in top_categories:
        insert_record('categories', ['name'], [category])
        
file_path = './data/amazon-products.csv'
columns = ['title', 'description', 'final_price', 'categories', 'image_url'] 
# load_and_print_data(file_path, ['image_url'])
# analyze_categories(file_path, 'categories')
# check_rows_without_top_categories(file_path, 'categories')
# insert_top_categories_to_db()

def get_store_id_by_name(store_name):
    store = read_record('stores', conditions={'name': store_name})
    return store['id']

# print(get_store_id_by_name('Red'))

async def insert_products_from_csv(file_path):
    data = pd.read_csv(file_path)
    store_id = get_store_id_by_name('Red')
    upper_limit = 200
    lower_limit = 21
    for index, row in data.iterrows():
        if index < lower_limit:
            continue
        if index >= upper_limit:
            break
        print(f"Processing row {index}...")
        try:
            price_str = row['final_price'].strip('"')  
            product = [row['title'], row['description'], float(price_str), store_id]
            categories = row['categories']
            if pd.notna(categories):
                categories = eval(categories)
                cat_id_list = []
                for category in categories:
                    category_id = read_record('categories', conditions={'name': category})
                    if category_id is not None:
                        # print(category_id.get('id'))
                        cat_id_list.append(category_id.get('id'))
                    
            product.append(cat_id_list)
            
            insert_record('products', ['title', 'description', 'price', 'store_id', 'category'], product)
            product_id = read_record('products', conditions={'title': row['title']})
            print(index, product_id.get('id'))
            image_url = row['image_url']
            if pd.notna(image_url):
                await download_and_upload_image(image_url, product_id.get('id'))
            print(f"Successfully inserted product: {row['title']}\n")
        except Exception as e:
            print(f"Failed to insert product: {e}")
            continue

async def main():
    await insert_products_from_csv(file_path)

asyncio.run(main())