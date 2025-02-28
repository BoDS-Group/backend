from fastapi import APIRouter, Depends
from utils.db_utils import *
from base_models.models import *
import json
from routers.authStore import is_admin_user

router = APIRouter(prefix="/api/categories")

@router.get("/")
async def get_products(current_user: TokenData = Depends(is_admin_user)):
    categories = read_records('categories')
    print(categories)
    return categories

@router.put("/{category_id}")
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

@router.post("/")
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

@router.delete("/{category_id}")
async def delete_category(category_id: str, current_user: TokenData = Depends(is_admin_user)):
    delete_record('categories', conditions={'id': category_id})
    return {"message": "Category deleted successfully"}