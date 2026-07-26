import io
import re

import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, int]:
    """Return (full_text, page_count) extracted from a PDF."""
    pages_text: list[str] = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text.strip())

    full_text = "\n\n".join(pages_text)
    # Collapse excessive blank lines
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    return full_text.strip(), page_count
