"""
Global exception handlers for the FastAPI application.
These handlers provide consistent error responses across the application.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions import DrivaultException
import logging

logger = logging.getLogger(__name__)


async def drivault_exception_handler(request: Request, exc: DrivaultException):
    """
    Handler for all custom Drivault exceptions.
    Returns a consistent JSON error response.
    """
    logger.error(f"DrivaultException: {exc.message} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "path": str(request.url.path)
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler for Pydantic validation errors.
    Provides detailed information about validation failures.
    """
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation error",
            "details": exc.errors(),
            "path": str(request.url.path)
        }
    )

