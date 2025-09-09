from typing import Annotated
from fastapi import APIRouter, Depends

from src.db.unitofwork import InterfaceUnitOfWork, UnitOfWork
from src.schemas import AddProductInOrder
from src.service import ApiService


router = APIRouter(prefix="/api", tags=["API"])

UOWDep = Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]


@router.post("/add_product_in_order")
async def add_product_in_order(
    uow: UOWDep,
    data: AddProductInOrder,
) -> bool:
    """
    Метод принимает ID заказа, ID номенклатуры и количество.
    Если товар уже есть в заказе, его количество увеличивается.
    Если товара нет в наличии то возвращается соответствующая ошибка
    Возможные ошибки:
        `ProductNotFoundError` (404)
        `OrderNotFoundError` (404)
        `ProductOutOfStockError` (400)
    """
    service = ApiService(uow)
    return await service.add_product_in_order(data)
