from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, Category, Order, Product, User
from src.db.unitofwork import UnitOfWork
from src.enums import OrderStatus
from src.main import app


TEST_DB_PATH = "test.sqlite"


class TestUnitOfWork(UnitOfWork):
    def __init__(self):
        engine = create_async_engine(f"sqlite+aiosqlite:///{TEST_DB_PATH}")
        self.session_factory = async_sessionmaker(
            engine, expire_on_commit=False
        )


engine = create_engine(f"sqlite:///{TEST_DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        yield session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[UnitOfWork] = lambda: TestUnitOfWork()
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def category_id(db_session):
    category = Category(
        name='test',
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category.id


@pytest.fixture(scope="session")
def product_id(db_session, category_id):
    product = Product(
        name='test',
        price=100,
        count=10,
        category_id=category_id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product.id


@pytest.fixture(scope="session")
def user_id(db_session):
    user = User(
        name='test',
        address='test',
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user.id


@pytest.fixture(scope="session")
def order_id(db_session, user_id):
    order = Order(
        user_id=user_id,
        status=OrderStatus.paid,
        amount=0,
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    return order.id
