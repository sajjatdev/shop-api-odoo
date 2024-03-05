from fastapi import FastAPI
from routes.product.product_route import productRoute
app=FastAPI()

app.include_router(productRoute,prefix="/api/v1")