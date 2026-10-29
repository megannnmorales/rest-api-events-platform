from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.routes.events import events_router
from app.routes.auth import  auth_router

app = FastAPI()

app.include_router(events_router)
app.include_router(auth_router)

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.detail["code"],
                "message": exc.detail["message"],
                "details": [],
            }
        },
    )  



@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400,
                        content={
                            "error": {
                                "code": "Bad Request",
                                "message": "Invalid input",
                                "details": jsonable_encoder(exc.errors())
                            }})