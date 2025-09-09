from fastapi import status

from src.api import router
from src.schemas import AddProductInOrder
from .conftest import client, db_session, order_id, product_id


base_endpoint = router.prefix


def test_product_not_found(client, db_session, order_id):
    not_exists_product_id = 99

    response = client.post(
        f"{base_endpoint}/add_product_in_order",
        json=AddProductInOrder(
            order_id=order_id,
            product_id=not_exists_product_id,
            count=1,
        ).model_dump()
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_order_not_found(client, db_session, product_id):
    not_exists_order_id = 99

    response = client.post(
        f"{base_endpoint}/add_product_in_order",
        json=AddProductInOrder(
            order_id=not_exists_order_id,
            product_id=product_id,
            count=1,
        ).model_dump()
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_product_out_of_stock(client, db_session, order_id, product_id):
    response = client.post(
        f"{base_endpoint}/add_product_in_order",
        json=AddProductInOrder(
            order_id=order_id,
            product_id=product_id,
            count=1000,
        ).model_dump()
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_success(client, db_session, order_id, product_id):
    response = client.post(
        f"{base_endpoint}/add_product_in_order",
        json=AddProductInOrder(
            order_id=order_id,
            product_id=product_id,
            count=1,
        ).model_dump()
    )

    assert response.status_code == status.HTTP_200_OK
