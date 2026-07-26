import time

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from ..models.schemas import InvoiceData, InvoiceResponse
from ..services.groq_parser import parse_invoice
from ..services.pdf_extractor import extract_text_from_pdf
from ..config import settings

router = APIRouter(prefix="/api", tags=["invoice"])


@router.post(
    "/extract",
    response_model=InvoiceResponse,
    summary="Extract structured data from an invoice PDF",
)
async def extract_invoice(
    invoice_file: UploadFile = File(..., description="Invoice PDF (max 20 MB)"),
):
    if invoice_file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    file_bytes = await invoice_file.read()

    if len(file_bytes) > settings.max_pdf_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {settings.max_pdf_size_mb} MB limit.",
        )

    start = time.time()

    try:
        raw_text, page_count = extract_text_from_pdf(file_bytes)
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Could not extract text from PDF: {exc}",
        ) from exc

    if not raw_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No text could be extracted. "
                "Make sure the PDF is not a scanned image without OCR layer."
            ),
        )

    try:
        parsed = parse_invoice(raw_text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI parsing failed: {exc}",
        ) from exc

    invoice_data = InvoiceData(**parsed)

    return InvoiceResponse(
        status="success",
        filename=invoice_file.filename or "invoice.pdf",
        pages=page_count,
        text_length=len(raw_text),
        processing_time=round(time.time() - start, 2),
        invoice=invoice_data,
    )


@router.get("/health", summary="Health check")
async def health():
    return {"status": "ok", "service": "Smart Invoice Extractor"}
