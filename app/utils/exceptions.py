from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def error_handlers(app: FastAPI):

    @app.exception_handler(404)
    async def not_found(request: Request, exc: StarletteHTTPException):
        return JSONResponse(content={"error": "Resource not found"}, status_code=404)

    @app.exception_handler(405)
    async def method_not_allowed(request: Request, exc: StarletteHTTPException):
        return JSONResponse(content={"error": "Method not allowed"}, status_code=405)

    @app.exception_handler(500)
    async def internal_error(request: Request, exc: StarletteHTTPException):
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        errors = exc.errors()

        body_missing = any(
            error.get("type") == "missing" and error.get("loc") == ("body",)
            for error in errors
        )
        if body_missing:
            return JSONResponse(
                content={"error": "No data provided"},
                status_code=400,
            )

        details = []
        for error in errors:
            message = error.get("msg", "Invalid value")
            if message.startswith("Value error, "):
                message = message[len("Value error, "):]
            details.append(message)

        return JSONResponse(
            content={"error": "Validation failed", "details": details},
            status_code=400,
        )
