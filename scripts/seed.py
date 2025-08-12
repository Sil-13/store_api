import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from store.models.product import ProductModel
from store.schemas.product import ProductIn

async def seed_products():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["store_db"]
    collection = db["products"]

   
    await collection.delete_many({})

    products_to_seed = [
        ProductIn(name="Notebook Gamer", quantity=10, price=7500.00, status=True),
        ProductIn(name="Smartphone Pro", quantity=25, price=4800.00, status=True),
        ProductIn(name="Smart TV 55'", quantity=15, price=3200.50, status=True),
        ProductIn(name="Cadeira Gamer", quantity=30, price=1200.75, status=True),
        ProductIn(name="Monitor Ultrawide", quantity=12, price=5250.00, status=True),
        ProductIn(name="Teclado Mecânico", quantity=50, price=650.00, status=True),
        ProductIn(name="Mouse Gamer RGB", quantity=60, price=350.00, status=True),
        ProductIn(name="Headset 7.1", quantity=40, price=850.25, status=True),
        ProductIn(name="Placa de Vídeo", quantity=8, price=9800.00, status=True),
        ProductIn(name="Processador Core i9", quantity=5, price=6200.00, status=True),
    ]

    for product_data in products_to_seed:
        product_model = ProductModel(**product_data.model_dump())
        await collection.insert_one(product_model.model_dump())
        print(f"Produto '{product_model.name}' inserido com sucesso.")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed_products())
    print("Seed de produtos concluída.")
