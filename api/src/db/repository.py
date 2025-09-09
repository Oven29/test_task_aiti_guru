from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional, Tuple, Type

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Base


class AbstractRepository(ABC):
    """Abstract class for repositories"""

    @abstractmethod
    async def create(self, **data: Any) -> Any:
        """
        Create new record

        :param data: data for create
        :return: created record
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, **filter_by: Any) -> Base:
        """
        Get record by filter if exists, else return None

        :param filter_by: filter for get record
        :return: record or None
        """
        raise NotImplementedError

    @abstractmethod
    async def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> Tuple[Base, bool]:
        """
        Get record by filter if exists, else create new record

        :param defaults: data for create
        :param filter_by: filter for get record
        :return: record and created flag
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, **filter_by: Any) -> Optional[Base]:
        """
        Update record by id

        :param id: record id
        :param filter_by: data for update
        :return: updated record or None
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> Base:
        """
        Delete record by id

        :param id: record id
        :return: deleted record or None
        """
        raise NotImplementedError

    @abstractmethod
    async def select(self, **filter_by: Any) -> List[Base]:
        """
        Select records by filter

        :param filter_by: filter for select records
        :return: list of records
        """
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None

    def __init__(self, session: AsyncSession, model: Optional[Type[Base]] = None) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = session
        if model is not None:
            self.model = model

    async def create(self, **data: Any) -> Base:
        self.logger.debug(f'Creating with {data=}')
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.unique().scalar_one()

    async def get(self, **filter_by: Any) -> Optional[Base]:
        self.logger.debug(f'Getting with {filter_by=}')
        stmt = select(self.model).filter_by(
            **filter_by).options(selectinload('*'))
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def get_or_crete(self, defaults: Dict[str, Any], **filter_by: Any) -> Tuple[Base, bool]:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if res is not None:
            self.logger.debug(f'Getting with {filter_by=}')
            return res, False

        defaults.update(filter_by)
        return await self.create(**defaults), True

    async def update(self, id: int, **values: Any) -> Base:
        self.logger.debug(f'Updating with {id=} {values=}')
        stmt = update(self.model).where(self.model.id == id).\
            values(**values).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, id: int) -> Base:
        self.logger.debug(f'Deleting with {id=}')
        stmt = delete(self.model).filter_by(id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def select(self, **filer_by: Any) -> List[Base]:
        self.logger.debug(f'Selecting with {filer_by=}')
        stmt = select(self.model).filter_by(**filer_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()


class CategoryRepository(SQLAlchemyRepository):
    pass


class ProductRepository(SQLAlchemyRepository):
    pass


class UserRepository(SQLAlchemyRepository):
    pass


class OrderRepository(SQLAlchemyRepository):
    pass


class OrderItemRepository(SQLAlchemyRepository):
    pass
