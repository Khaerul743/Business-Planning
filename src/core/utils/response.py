import json
from typing import Any, Dict, List, Union

from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# 1. Tipe Data untuk Payload Error
# Digunakan untuk validasi error detail
ErrorDetail = Dict[str, str]


def auth_success_response(
    response: Response,
    data: Dict[str, Any],
    message: str = "Login successful",
) -> Response:
    payload = {
        "status": "success",
        "message": message,
        "data": data,
    }

    response.status_code = status.HTTP_200_OK
    response.headers["content-type"] = "application/json"
    response.body = json.dumps(payload).encode("utf-8")

    return response


# 2. Fungsi untuk Respons Sukses (2xx)
def success_response(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    message: str = "Operation successful.",
    status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    """
    Membuat respons JSON standar untuk kasus sukses.

    Args:
        data: Data yang ingin dikembalikan.
        message: Pesan singkat mengenai operasi yang sukses.
        status_code: Status HTTP (default 200 OK).

    Returns:
        JSONResponse: Objek respons FastAPI.
    """
    payload = {
        "status": "success",
        "message": message,
        "data": jsonable_encoder(data),
    }
    return JSONResponse(
        status_code=status_code,
        content=payload,
    )


# 3. Fungsi untuk Respons Error (4xx, 5xx)
def error_response(
    http_status: int,
    error_code: str,
    message: str,
    details: Union[None, List[ErrorDetail]] = None,
) -> JSONResponse:
    """
    Membuat respons JSON standar untuk kasus error (4xx atau 5xx).

    Args:
        http_status: Status HTTP (misalnya 404, 500).
        error_code: Kode error internal yang unik (misalnya "RESOURCE_NOT_FOUND").
        message: Deskripsi singkat error.
        details: Detail error tambahan (khususnya untuk validation error).

    Returns:
        JSONResponse: Objek respons FastAPI.
    """

    # Menentukan status payload berdasarkan HTTP status code
    if 400 <= http_status < 500:
        status_type = "fail"  # Client error
    elif http_status >= 500:
        status_type = "error"  # Server error
    else:
        # Fallback jika status code tidak standar
        status_type = "error"

    payload = {
        "status": status_type,
        "code": error_code,
        "message": message,
    }

    if details:
        payload["details"] = details

    return JSONResponse(
        status_code=http_status,
        content=payload,
    )
