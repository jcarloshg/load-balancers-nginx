"""
    Module for creating LEGO model items with validation and error handling.
"""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, ValidationError
import os
import socket

from typing_extensions import Literal

from .model_validation_exception import ModelErrorException


class LegoModel(BaseModel):
    """Data model for a LEGO model item."""
    name: str
    pieces: int
    year: int
    theme: str
    difficulty: Literal["easy", "medium", "hard"] = Field(
        ...,
        description="Difficulty level of the LEGO model"
    )
    price_us: float

    @classmethod
    @field_validator('difficulty')
    def validate_difficulty(cls, v):
        """Validate that difficulty is one of the allowed values."""
        allowed_values = cls._get_allowed_difficulties()
        if v not in allowed_values:
            raise ValueError(f"difficulty must be one of {allowed_values}")
        return v

    @classmethod
    def _get_allowed_difficulties(cls):
        return {"easy", "medium", "hard"}


create_model_router = APIRouter()


@create_model_router.post("/models")
async def create_item(request: Request):
    """Create a new LEGO model item."""

    host_tag = os.environ.get("HOST_TAG", "")
    ip_address = "unknown"
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip_address = "unknown"

    try:
        body = await request.json()
        lego_validated = LegoModel(**body)
        return JSONResponse(
            content={
                "host": f"tag: {host_tag} - {ip_address}",
                "success": True,
                "message": "Item created successfully",
                "data": lego_validated.model_dump()
            },
            status_code=status.HTTP_200_OK,
        )
    except ValidationError as e:
        erro_info = ModelErrorException.generate_primitives(e)
        return JSONResponse(
            content={
                "host": host_name,
                "success": False,
                "message": "Something went wrong",
                "data": erro_info
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except ValueError:
        return JSONResponse(
            content={
                "host": host_name,
                "success": False,
                "message": "Something went wrong",
                "data": {
                    "user_message": "Something went wrong",
                    "developer_message": "Body could not be processed"
                }
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
