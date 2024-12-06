from fastapi import APIRouter, HTTPException, status
from models.model import Order
from config.config import user_collection, product_collection, orders_collection
from bson import ObjectId
import logging


orders = APIRouter()
logging.basicConfig(level=logging.INFO)

def object_id(obj_id: ObjectId):
    return str(obj_id)

async def get_current_user(full_name: str):
    user = user_collection.find_one({"full_name": full_name})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated. Please log in to place an order.",
        )
    return user

@orders.post("/orders")
async def place_order(order: Order):
    # Extract user details from the database using the full_name from the order body
    user = user_collection.find_one({"full_name": order.full_name})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated. Please log in to place an order.",
        )

    user_address = user.get("address")
    if not user_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address not found for user '{user['full_name']}'.",
        )

    total_price = 0.0
    updated_items = []

    # Check if the user already has a pending order
    existing_order = orders_collection.find_one({
        "user_id": user["_id"],
        "status": "Pending"
    })

    # Process items
    for item in order.items:
        logging.info(f"Looking for product: {item.product_name}")
        product = product_collection.find_one({
            "product_name": {"$regex": f"^{item.product_name}$", "$options": "i"}
        })
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product '{item.product_name}' not found.",
            )
        if product["stock"] < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product '{product['product_name']}'. Available: {product['stock']}",
            )

        # Update stock
        product_collection.update_one(
            {"_id": product["_id"]},
            {"$inc": {"stock": -item.quantity}}
        )

        # Add item details to updated_items
        updated_items.append({
            "product_name": product["product_name"],
            "quantity": item.quantity,
            "price_per_unit": product["product_price"],
            "total_price": product["product_price"] * item.quantity
        })

        # Update total price
        total_price += product["product_price"] * item.quantity

    if existing_order:
        # Update the existing order
        orders_collection.update_one(
            {"_id": existing_order["_id"]},
            {
                "$push": {"items": {"$each": updated_items}},  # Append new items
                "$inc": {"total_price": total_price}          # Increment total price
            }
        )
        order_id = object_id(existing_order["_id"])
        message = "Existing order updated successfully."
    else:
        # Create a new order
        order_dict = {
            "user_id": user["_id"],
            "full_name": user["full_name"],
            "address": user_address,
            "items": updated_items,
            "total_price": total_price,
            "status": "Pending",
        }
        result = orders_collection.insert_one(order_dict)
        order_id = object_id(result.inserted_id) #type:ignore
        message = "New order placed successfully."

    return {
        "message": message,
        "order_id": order_id,
        "total_price": total_price,
        "delivery_address": user_address,
    }