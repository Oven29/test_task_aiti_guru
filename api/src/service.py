from abc import ABC
import logging

from src.db.unitofwork import InterfaceUnitOfWork
from src.exceptions import (
    OrderNotFoundError,
    ProductNotFoundError,
    ProductOutOfStockError
)
from src.schemas import AddProductInOrder


class AbstractService(ABC):
    def __init__(self, uow: InterfaceUnitOfWork) -> None:
        self._uow: InterfaceUnitOfWork = uow
        self._logger = logging.getLogger(self.__class__.__name__)


class ApiService(AbstractService):
    async def add_product_in_order(self, data: AddProductInOrder) -> bool:
        async with self._uow:
            product = await self._uow.product.get(id=data.product_id)
            if product is None:
                raise ProductNotFoundError(product_id=data.product_id)

            if product.count < data.count:
                raise ProductOutOfStockError(product_id=data.product_id)

            order = await self._uow.order.get(id=data.order_id)
            if order is None:
                raise OrderNotFoundError(order_id=data.order_id)

            await self._uow.product.update(
                id=data.product_id,
                count=product.count - data.count
            )
            order_item, created = await self._uow.order_item.get_or_crete(
                order_id=data.order_id,
                product_id=data.product_id,
                defaults={"count": data.count}
            )
            await self._uow.order.update(
                id=data.order_id,
                amount=order.amount + data.count * product.price
            )
            if not created:
                await self._uow.order_item.update(
                    id=order_item.id,
                    count=order_item.count + data.count,
                )

            await self._uow.commit()
            return True
