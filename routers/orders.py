from fastapi import APIRouter, HTTPException, Depends, Request
from utils.db_utils import *
from utils.auth_utils import *
from base_models.models import *
import json
import stripe

router = APIRouter(prefix="/api/orders")
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") 
PUBLIC_FRONTEND_URL = os.environ.get("PUBLIC_FRONTEND_URL") 

@router.post("/create-checkout-session")
async def create_checkout_session(cart_items: CartItems):
    # print(cart_items)
    try:
        line_items = []
        for item in cart_items.cart_items:
            print(item)
            line_items.append({
                "price_data": {
                    "currency": "euro",
                    "product_data": {"name": item.title},
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            success_url=f"{PUBLIC_FRONTEND_URL}/cart?success=true",
            cancel_url=f"{PUBLIC_FRONTEND_URL}/cart?canceled=true",
        )

        return {"sessionId": session.id}
    except Exception as e:
        print("Error creating checkout session:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/checkout")
async def create_order(order: OrderCreate, request: Request):
    print(order)
    if order.password:
        if check_if_customer_exists(order.email):
            if not check_password(order.email, order.password):
                raise HTTPException(status_code=400, detail="Password incorrect")
            else:
                print("User exists: Password correct")
        else:
            user_register = {
                "name": order.name,
                "email": order.email,
                "phone_number": order.phone_number,
                "city": order.city,
                "postal_code": order.postal_code,
                "street_address": order.street_address,
                "country": order.country,
                "password": order.password
            }
            account_created = create_customer_account(user_register)
            if not account_created:
                raise HTTPException(status_code=400, detail="Error creating user account")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": order.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        token = request.headers.get("Authorization")
        if not len(token) > 50:
            if check_if_customer_exists(order.email):
                raise HTTPException(status_code=400, detail="User already exists")
            else:
                raise HTTPException(status_code=400, detail="Password or JWT token required")
        else:
            print("Token:", token)
            user_update = {
                "name": order.name,
                "email": order.email,
                "phone_number": order.phone_number,
                "city": order.city,
                "postal_code": order.postal_code,
                "street_address": order.street_address,
                "country": order.country,
                "password": order.password
            }
            account_updated = update_customer_account(user_update)
            if not account_updated:
                raise HTTPException(status_code=400, detail="Error updating user account")
            return {"message": "Token received"}
    # return {"message": "Order created successfully"}