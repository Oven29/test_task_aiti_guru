from abc import ABC, abstractmethod
from typing import Type

from . import async_session_maker
from .repository import (
    CategoryRepository,
    ProductRepository,
    UserRepository,
    OrderRepository,
    OrderItemRepository
)


class InterfaceUnitOfWork(ABC):
    category: Type[CategoryRepository]
    product: Type[ProductRepository]
    user: Type[UserRepository]
    order: Type[OrderRepository]
    order_item: Type[OrderItemRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(InterfaceUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.category = CategoryRepository(self.session)
        self.product = ProductRepository(self.session)
        self.user = UserRepository(self.session)
        self.order = OrderRepository(self.session)
        self.order_item = OrderItemRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
