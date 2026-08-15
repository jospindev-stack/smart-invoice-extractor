from types import SimpleNamespace

from backend.services.pdf_extractor import extract_text_from_pdf


def test_extract_text_from_pdf_returns_clean_text_and_page_count(monkeypatch):
    fake_pdf = SimpleNamespace(
        pages=[
            SimpleNamespace(extract_text=lambda: "Invoice 123\n\n\nVendor A"),
            SimpleNamespace(extract_text=lambda: "Total: 100.00"),
        ]
    )

    class PdfContext:
        def __enter__(self):
            return fake_pdf

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(
        "backend.services.pdf_extractor.pdfplumber.open",
        lambda *_args, **_kwargs: PdfContext(),
    )

    text, page_count = extract_text_from_pdf(b"fake-pdf")

    assert page_count == 2
    assert text == "Invoice 123\n\nVendor A\n\nTotal: 100.00"


def test_extract_text_from_pdf_skips_pages_without_text(monkeypatch):
    fake_pdf = SimpleNamespace(
        pages=[
            SimpleNamespace(extract_text=lambda: None),
            SimpleNamespace(extract_text=lambda: "Invoice content"),
        ]
    )

    class PdfContext:
        def __enter__(self):
            return fake_pdf

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(
        "backend.services.pdf_extractor.pdfplumber.open",
        lambda *_args, **_kwargs: PdfContext(),
    )

    text, page_count = extract_text_from_pdf(b"fake-pdf")

    assert page_count == 2
    assert text == "Invoice content"
