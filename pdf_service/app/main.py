from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.router import pdf_router

app = FastAPI(
    title="PDF Generation Service",
    description="Independent service for generating profile PDFs via JWT",
    version="1.0.0"
)

app.include_router(pdf_router)
