from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int
    detail: str


class AddProductInOrder(BaseModel):
    order_id: int
    product_id: int
    count: int
