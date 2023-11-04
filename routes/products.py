from fastapi import APIRouter
from models.request.product import ProductCreation
from models.mongo.product import MongoProducts
from datetime import datetime
import json
from typing import Optional
from mongoengine.errors import DoesNotExist

products_api = APIRouter(prefix='/products')


@products_api.post('', tags=["Product"])
async def create_products(product_creation: ProductCreation):
    product_dict = product_creation.model_dump()
    product_dict['created_at'] = datetime.utcnow()
    mongo_product = MongoProducts(**product_dict)
    mongo_product.save()

    return json.loads(mongo_product.to_json())


@products_api.get('', tags=["Product"])
async def get_products(product_id: Optional[str] = None):
    try:
        if product_id:
            mongo_product = MongoProducts.objects.get(id=product_id)
        else:
            mongo_product = MongoProducts.objects()

        return json.loads(mongo_product.to_json())
    except DoesNotExist:
        return {"error": "Product not found"}


@products_api.get('/search', tags=["Product"])
async def search_product(query_str: Optional[str] = None):
    mongo_products = MongoProducts.objects(product_name__icontains=query_str)

    return json.loads(mongo_products.to_json())


@products_api.put('', tags=["Product"])
async def edit_products(product_id: str, product_edit: ProductCreation):
    try:
        mongo_product = MongoProducts.objects.get(id=product_id)
        product_dict = product_edit.model_dump()
        mongo_product.update(**product_dict)
        mongo_product.reload()

        return json.loads(mongo_product.to_json())
    except DoesNotExist:
        return {"error": "Product not found"}


@products_api.delete('', tags=["Product"])
async def delete_products(product_id: str):
    try:
        mongo_product = MongoProducts.objects.get(id=product_id)
        mongo_product.delete()

        return {"status": "success"}
    except DoesNotExist:
        return {"error": "Product not found"}
