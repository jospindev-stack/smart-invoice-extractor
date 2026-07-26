from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import invoice

app = FastAPI(
    title="Smart Invoice Extractor",
    description=(
        "Upload an invoice PDF and receive fully structured JSON data: "
        "vendor, buyer, line items, amounts, dates, payment details."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invoice.router)


@app.get("/", tags=["root"])
async def root():
    return {
        "service": "Smart Invoice Extractor",
        "version": "1.0.0",
        "endpoints": {
            "extract": "POST /api/extract",
            "health": "GET /api/health",
            "docs": "/docs",
        },
    }
