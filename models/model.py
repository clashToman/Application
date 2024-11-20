from pydantic import BaseModel


class RegisterForm(BaseModel):
    name: str
    email: str
    password: str


class LoginForm(BaseModel):
    email: str
    password: str


class Profile(BaseModel):
    name: str | None = None
    address: str | None = None
    password: str | None = None


class ProductForm(BaseModel):
    n_id: str | None = None
    product_name: str | None = None
    product_price: int | None = None
    product_quantity: str | None = None
    stock: int | None = None
    category: str | None = None
