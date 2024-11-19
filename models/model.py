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


class ProducForm(BaseModel):
    n_id: str
    product_name: str
    product_price: int
    product_quantity: str
    stock: int
    category: str
