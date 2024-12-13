from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from config.config import user_collection,orders_collection


admin = APIRouter()

def str_id(obj):
    return str(obj['_id'])


@admin.get("/admin/stats")
async def get_dashboard_stats():
    try:
        # Get total users, orders, and revenue
        total_users = user_collection.count_documents({})
        total_orders = orders_collection.count_documents({})
        total_revenue = sum(order["total_price"] for order in orders_collection.find())

        return JSONResponse(content={
            "total_users": total_users,
            "total_orders": total_orders,
            "total_revenue": total_revenue
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
