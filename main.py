from fastapi import FastAPI
from routes.auth import router
from routes.user import user
from routes.product import product


app = FastAPI()

app.include_router(user)
app.include_router(product)
app.include_router(router)


@app.get("/")
async def start():
    return {"message": "Hello User..!"}
