from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from store.core.exceptions import InsertionException, NotFoundException
from store.routers import api_router

app = FastAPI(title="Store API")
app.include_router(api_router)

@app.exception_handler(InsertionException)
def insertion_exception_handler(request: Request, exc: InsertionException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )

@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )
