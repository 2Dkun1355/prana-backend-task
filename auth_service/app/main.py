from fastapi import FastAPI
from app.router import auth_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Auth Service",
    description="Service for user registration, authentication.",
    version="1.0.0"
)

app.include_router(auth_router)
