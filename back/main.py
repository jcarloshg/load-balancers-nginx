"""
    Main application module for the API v2.

"""
from fastapi import FastAPI
# domain
from src.app.create_model.create_model_use_case import create_model_router

app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint of the API v2."""
    return "Hello, this is the main endpoint of the API v2"


app.include_router(create_model_router)
