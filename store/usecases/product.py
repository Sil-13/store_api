from datetime import datetime
from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.core.exceptions import InsertionException, NotFoundException
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate

class ProductUsecase:
    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        self.db_client = db_client
        self.collection = self.db_client.get_database()["products"]

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product_model = ProductModel(**body.model_dump())
            await self.collection.insert_one(product_model.model_dump())
            return ProductOut(**product_model.model_dump())
        except pymongo.errors.PyMongoError as e:
         
            raise InsertionException(f"Error inserting product in database: {e}")


    async def get(self, id: str) -> ProductOut:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f"Product not found with id: {id}")
        return ProductOut(**result)

    async def query(self, price_min: float = None, price_max: float = None) -> List[ProductOut]:
        filter_query = {}
        if price_min is not None and price_max is not None:
            filter_query["price"] = {"$gt": price_min, "$lt": price_max}
        elif price_min is not None:
            filter_query["price"] = {"$gt": price_min}
        elif price_max is not None:
            filter_query["price"] = {"$lt": price_max}

        return [ProductOut(**item) async for item in self.collection.find(filter_query)]

    async def update(self, id: str, body: ProductUpdate) -> ProductOut:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with id: {id}")

        update_data = body.model_dump(exclude_unset=True)

        
        update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductOut(**result)

    async def delete(self, id: str) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with id: {id}")

        result = await self.collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False

usecase = ProductUsecase(db_client=...) 
