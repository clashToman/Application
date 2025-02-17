from pydantic import BaseModel, Field, EmailStr, constr
from typing import List, Optional
from datetime import datetime


# 1. User Model
class User(BaseModel):
    user_id: constr(pattern="^user\d+$") = Field(...) #type:ignore # Pattern like user1, user2, etc.
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 2. Product Model
class Product(BaseModel):
    product_id: str
    name: str
    category_id: str
    price: float
    stock: int
    description: str

# 3. Order Item Model
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float

# 4. Order Model

class Order(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    category: str
    total_price: float
    status: str = Field(default="pending")
    order_date: datetime = Field(default_factory=datetime.utcnow)

# 5. Order History Model
class OrderHistory(BaseModel):
    user_id: str
    order_id: str
    items: List[OrderItem]
    total_price: float
    status: str
    order_date: datetime

# 6. Subscription Model
class Subscription(BaseModel):
    user_id: str
    product_id: str
    quantity: int
    frequency: str  # daily, weekly, monthly
    next_delivery_date: datetime

# 7. Email Request Model
class EmailRequest(BaseModel):
    email: EmailStr

# 8. OTP Verification Model
class OtpVerification(BaseModel):
    email: EmailStr
    otp: int

# 9. Profile Update Model
class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class RegisterForm(BaseModel):
    full_name: str
    phone_number: str
    email: str
    age:int
    gender:str

class OrderStatus(BaseModel):
    status: str

# 10. Category Model
class Category(BaseModel):
    category_id: constr(pattern="^category\d+$") = Field(...)#type:ignore  # Pattern like category1, category2, etc.
    name: str = Field(..., min_length=2, max_length=50)


# --------------------
# MongoDB Optimization
# --------------------
def create_indexes(db):
    db.users.create_index("phone_number", unique=True)
    db.products.create_index("category")
    db.orders.create_index("user_id")
    db.orders.create_index("order_date")
    db.order_history.create_index("user_id")
    db.subscriptions.create_index("user_id")
    db.users.create_index("otp")
    print("Indexes created successfully")
