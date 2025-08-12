from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
   
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: str = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:

    return await usecase.get(id=id)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    price_min: float = Query(None, alias="price_min"),
    price_max: float = Query(None, alias="price_max"),
    usecase: ProductUsecase = Depends()
) -> List[ProductOut]:
    return await usecase.query(price_min=price_min, price_max=price_max)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: str = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
   
    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
