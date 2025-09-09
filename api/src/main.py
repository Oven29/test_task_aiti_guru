from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router
from src.exceptions import BaseApiError, exception_handler


app = FastAPI(
    title="Test task Aiti Guru",
)

app.add_exception_handler(BaseApiError, exception_handler)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
