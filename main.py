from fastapi import FastAPI
from routes.user import user
from routes.product import product
from routes.login import log

app = FastAPI()

app.include_router(user)
app.include_router(product)
app.include_router(log)


@app.get("/")
async def start():
    return {"message": "Hello User..!"}
