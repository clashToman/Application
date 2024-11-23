from fastapi import APIRouter, HTTPException
from models.model import ProducForm
from config.config import product_collection
from typing import List,Optional

product = APIRouter()

@product.post("/product")
async def register_product(stock: ProducForm):
    try:
        # Check if the product with the same n_id already exists in the given category
        existing_product = product_collection.find_one({"n_id": stock.n_id, "category": stock.category})
        if existing_product:
            raise HTTPException(status_code=400, detail="Product already exists in this category")

        # Prepare the new product data
        new_product = {
            "n_id": stock.n_id,
            "product_name": stock.product_name,
            "product_price": stock.product_price,
            "product_quantity": stock.product_quantity,
            "stock": stock.stock,
            "category": stock.category
        }

        # Insert the new product into the database
        result = product_collection.insert_one(new_product)

        return {"message": "Product added successfully!", "_id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@product.get("/products", response_model=List[ProducForm])
async def get_all_products(category: Optional[str] = None):
    try:
        # Query all products, or filter by category if provided
        query = {"category": category} if category else {}
        products = list(product_collection.find(query))
        
        # Convert ObjectId to string for JSON compatibility
        for product in products:
            product["_id"] = str(product["_id"])

        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
