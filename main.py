import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from src.app.middlewares.error_handler import (
    custom_exception_handler,
    db_exception_handler,
    unexpected_exception_handler,
    validation_exception_handler,
)
from src.core.exceptions import BaseCustomeException
from src.core.utils import get_logger

logger = get_logger(__name__)

app = FastAPI()


class Test(BaseModel):
    name: str
    umur: int


@app.post("/")
def root(request: Request, payload: Test):
    return "Ok"


# 1. Register Custom Errors
app.add_exception_handler(BaseCustomeException, custom_exception_handler)

# 2. Register Validation Errors (Penting untuk Pydantic)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 3. Register Database Errors
app.add_exception_handler(SQLAlchemyError, db_exception_handler)

# 4. Register Catch-All (Selalu terakhir)
app.add_exception_handler(Exception, unexpected_exception_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
