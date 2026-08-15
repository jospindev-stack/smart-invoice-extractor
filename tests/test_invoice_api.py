from fastapi.testclient import TestClient

from backend.main import app
from backend.routers import invoice as invoice_router

client = TestClient(app)


def _parsed_invoice():
    return {
        "invoice_number": "INV-001",
        "invoice_date": "2026-08-15",
        "due_date": None,
        "currency": "CAD",
        "vendor": {"name": "Vendor Inc."},
        "buyer": {"name": "Buyer Inc."},
        "line_items": [
            {
                "description": "Service",
                "quantity": 1,
                "unit": None,
                "unit_price": 100.0,
                "tax_rate": 5.0,
                "amount": 100.0,
            }
        ],
        "subtotal": 100.0,
        "tax_rate": 5.0,
        "tax_amount": 5.0,
        "discount": None,
        "total_amount": 105.0,
        "payment_terms": None,
        "payment_method": None,
        "bank_details": None,
        "notes": None,
        "confidence_score": 0.95,
    }


def test_health_endpoint_returns_service_status():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Smart Invoice Extractor",
    }


def test_extract_rejects_non_pdf_file():
    response = client.post(
        "/api/extract",
        files={"invoice_file": ("invoice.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are accepted."


def test_extract_returns_structured_invoice(monkeypatch):
    monkeypatch.setattr(
        invoice_router,
        "extract_text_from_pdf",
        lambda _data: ("invoice text", 2),
    )
    monkeypatch.setattr(invoice_router, "parse_invoice", lambda _text: _parsed_invoice())

    response = client.post(
        "/api/extract",
        files={"invoice_file": ("invoice.pdf", b"pdf bytes", "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["filename"] == "invoice.pdf"
    assert body["pages"] == 2
    assert body["invoice"]["invoice_number"] == "INV-001"
    assert body["invoice"]["total_amount"] == 105.0


def test_extract_rejects_pdf_without_text(monkeypatch):
    monkeypatch.setattr(
        invoice_router,
        "extract_text_from_pdf",
        lambda _data: ("", 1),
    )

    response = client.post(
        "/api/extract",
        files={"invoice_file": ("scan.pdf", b"pdf bytes", "application/pdf")},
    )

    assert response.status_code == 422
    assert "No text could be extracted" in response.json()["detail"]


def test_extract_returns_server_error_when_parser_fails(monkeypatch):
    monkeypatch.setattr(
        invoice_router,
        "extract_text_from_pdf",
        lambda _data: ("invoice text", 1),
    )

    def fail_parser(_text):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(invoice_router, "parse_invoice", fail_parser)

    response = client.post(
        "/api/extract",
        files={"invoice_file": ("invoice.pdf", b"pdf bytes", "application/pdf")},
    )

    assert response.status_code == 500
    assert "AI parsing failed" in response.json()["detail"]
