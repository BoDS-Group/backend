from fastapi import APIRouter, HTTPException, Depends
from utils.db_utils import *
from base_models.models import *
import json

router = APIRouter(prefix="/api/orders")

# Get a single order
@router.get("/orders/{order_id}")
async def get_order(order_id: str):#, current_user: TokenData = Depends(is_admin_user)):
    order = read_record('orders', conditions={'id': order_id})
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    print(order)
    return order 

@router.post("/orders")
async def create_order(order: OrderCreate):#,current_user: TokenData = Depends(is_admin_user)):
    # Convert properties dictionary to JSON string
    line_items_json = json.dumps(order.line_items) if order.line_items else None

    # Insert the new product into the database
    insert_record(
        'orders',
        attributes=['line_items', 'name', 'email', 'city', 'postal_code', 'street_address', 'country', 'paid'],
        values=[line_items_json, order.name, order.email, order.city, order.postal_code, order.street_address, order.country, order.paid]
    )
    return {"message": "Order created successfully"}

@router.put("/orders/{order_id}")
async def update_product(product_id: str, order: OrderUpdate):#, current_user: TokenData = Depends(is_admin_user)):
    # Convert properties dictionary to JSON string if it exists
    line_items_json = json.dumps(order.line_items) if order.line_items else None

    # Create a dictionary of the fields to update
    update_data = {k: v for k, v in order.model_dump().items() if v is not None} #Not sure about model_dump(). VS Code said dict() is deprecated ¯_(ツ)_/¯
    if 'line_items' in update_data:
        update_data['line_items'] = line_items_json

    print(update_data)
    # Update the product in the database
    update_record(
        'orders',
        conditions={'id': product_id},
        attributes=update_data.keys(),
        values=list(update_data.values())
    )
    return {"message": "Order updated successfully"}

@router.delete("/orders/{order_id}")
async def delete_order(order_id: str):#, current_user: TokenData = Depends(is_admin_user)):
    delete_record('orders', conditions={'id': order_id})
    return {"message": "Order deleted successfully"}