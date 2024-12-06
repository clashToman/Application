from fastapi import FastAPI
from routes.auth import router
from routes.user import user
from routes.product import product
from routes.order import orders


app = FastAPI()

app.include_router(user)
app.include_router(product)
app.include_router(router)
app.include_router(orders)

@app.get("/")
async def start():
    return {"message": "Hello User..!"}
