from fastapi import APIRouter, HTTPException
from config.config import category_collection, product_collection, order_collection, order_history_collection
from models.model import Category, Product, Order
from datetime import datetime

admin_router = APIRouter()


# 1️⃣ Add Category
@admin_router.post("/admin/category/add")
def add_category(category: Category):
    if category_collection.find_one({"name": category.name}):
        raise HTTPException(status_code=400, detail="Category already exists")
    category_collection.insert_one(category.dict())
    return {"message": "Category added successfully"}


# 2️⃣ Get All Categories
@admin_router.get("/admin/categories")
def get_all_categories():
    return list(category_collection.find({}, {"_id": 0}))


# 3️⃣ Delete Category
@admin_router.delete("/admin/category/delete/{name}")
def delete_category(name: str):
    result = category_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


# 4️⃣ Add Product
@admin_router.post("/admin/product/add")
def add_product(product: Product):
    if product_collection.find_one({"name": product.name}):
        raise HTTPException(status_code=400, detail="Product already exists")
    product_collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


# 5️⃣ Get All Products
@admin_router.get("/admin/products")
def get_all_products():
    return list(product_collection.find({}, {"_id": 0}))


# 6️⃣ Insert All Orders
@admin_router.post("/admin/orders/insert")
def insert_all_orders(orders: list[Order]):
    inserted_orders = []
    for order in orders:
        if order_collection.find_one({"order_id": order.order_id}):
            continue

        order_data = order.dict()
        order_data["order_date"] = datetime.utcnow()
        order_data["status"] = "pending"
        order_collection.insert_one(order_data)
        order_history_collection.insert_one(order_data)
        inserted_orders.append(order.order_id)

    if not inserted_orders:
        raise HTTPException(status_code=400, detail="No new orders inserted")
    return {"message": "Orders inserted successfully", "orders": inserted_orders}


# 7️⃣ Get All Orders
@admin_router.get("/admin/orders")
def get_all_orders():
    orders = list(order_collection.find({}, {"_id": 0}))
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return {"orders": orders}


# 8️⃣ Delete Order
@admin_router.delete("/admin/orders/delete/{order_id}")
def delete_order(order_id: str):
    result = order_collection.delete_one({"order_id": order_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order '{order_id}' deleted successfully"}
