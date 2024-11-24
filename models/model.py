from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterForm(BaseModel):
    email: EmailStr
    name: str
    address: str
    phone: int
    age: Optional[int] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[int] = None
    age: Optional[int] = None


class OtpVerfication(BaseModel):
    email: EmailStr
    otp: int


class EmailRequest(BaseModel):
    email: str


class ProducForm(BaseModel):
    n_id: str
    product_name: str
    product_price: int
    product_quantity: str
    stock: int
    category: str
