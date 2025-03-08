from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.auth import router
from fastapi.middleware.cors import CORSMiddleware
from routes.user import  user_router as user
from routes.product import product_router as product
from routes.order import order_router as orders
from routes.admin import admin_router as admin
from routes.home import home_router as home
from routes.subscription import subscription_router as subscription

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,                   # Allow cookies/auth if needed
    allow_methods=["GET", "POST", "OPTIONS"], # Allowed HTTP methods
    allow_headers=["Content-Type"],           # Allowed headers (adjust if needed)
)

app.mount("/upload_image", StaticFiles(directory="uploads_image"), name="upload_image")

app.include_router(user,prefix="/user")
app.include_router(product)
app.include_router(router,prefix="/auth")
app.include_router(orders)
app.include_router(admin)
app.include_router(home)
app.include_router(subscription)

@app.get("/")
async def start():
    return {"message": "Hello User..!"}
