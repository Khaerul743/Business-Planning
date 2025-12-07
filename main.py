import uvicorn
from fastapi import FastAPI, Request, status

from src.app.middlewares.error_handler import ErrorHandlerMiddleware
from src.core.exceptions import InternalServerError

app = FastAPI()

# Middlewares
app.add_middleware(ErrorHandlerMiddleware)


@app.get("/")
def root():
    raise InternalServerError()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info",
    )
