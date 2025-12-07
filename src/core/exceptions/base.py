# src/core/exceptions/base.py

from typing import Any, Dict, Optional

from fastapi import (  # Jika Anda tetap ingin mewarisi HTTPException
    HTTPException,
    status,
)


# Lebih baik mewarisi Exception agar tidak bertabrakan dengan Exception Handler bawaan FastAPI
# class BaseCustomeException(Exception):
class BaseCustomeException(
    HTTPException
):  # Tetap pakai HTTPException agar detail bisa digunakan
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: Dict[str, Any] = {
        "code": "GENERIC_CUSTOM_ERROR",
        "message": "An unspecified custom error occurred.",
    }

    def __init__(
        self, status_code: Optional[int] = None, detail: Optional[Dict[str, Any]] = None
    ):
        # Memastikan inisialisasi status_code dan detail
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail

        # Panggil constructor HTTPException
        super().__init__(status_code=self.status_code, detail=self.detail)
