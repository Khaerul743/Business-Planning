import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.app.middlewares.error_handler import (
    custom_exception_handler,
    unexpected_exception_handler,
    validation_exception_handler,
)
from src.app.routes import (
    auth_route,
    business_knowladge_route,
    business_route,
    user_route,
    whatsapp_route,
)
from src.config.supabase import init_supabase
from src.core.exceptions import BaseCustomeException
from src.core.utils import get_logger

logger = get_logger(__name__)

app = FastAPI()

app.include_router(whatsapp_route.router)
app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(business_route.router)
app.include_router(business_knowladge_route.router)


@app.get("/")
def root():
    return "Ok"


# 1. Register Custom Errors
app.add_exception_handler(BaseCustomeException, custom_exception_handler)

# 2. Register Validation Errors (Penting untuk Pydantic)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 3. Register Database Errors
# app.add_exception_handler(SQLAlchemyError, db_exception_handler)

# 4. Register Catch-All (Selalu terakhir)
app.add_exception_handler(Exception, unexpected_exception_handler)


@app.on_event("startup")
async def startup_event():
    await init_supabase()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
