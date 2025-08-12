from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, AfterValidator
from bson import ObjectId

def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError(f"Invalid ObjectId: {value}")
    return value

PyObjectId = Annotated[str, AfterValidator(check_object_id)]

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: float = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase):
    ...

class ProductOut(ProductIn):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime = Field()
    updated_at: datetime = Field()

class ProductUpdate(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None
    status: Optional[bool] = None
    updated_at: Optional[datetime] = None
