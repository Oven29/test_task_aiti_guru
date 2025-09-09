from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

from src.schemas import ErrorResponse


class BaseApiError(HTTPException):
    status_code: int
    detail: str

    def __init__(self, **kwargs):
        detail = self.detail.format(**kwargs)
        super().__init__(status_code=self.status_code, detail=detail)
        self.error_response = ErrorResponse(
            status_code=self.status_code,
            detail=detail,
        )


class ProductNotFoundError(BaseApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Product with id {product_id} not found'


class OrderNotFoundError(BaseApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Order with id {order_id} not found'


class ProductOutOfStockError(BaseApiError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Product with id {product_id} out of stock'


async def exception_handler(request: Request, exc: BaseApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.error_response.model_dump()
    )
