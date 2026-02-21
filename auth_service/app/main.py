from fastapi import FastAPI
from .router import auth_router

app = FastAPI(
    title="Auth Service",
    description="Service for user registration, authentication.",
    version="1.0.0"
)

app.include_router(auth_router)
