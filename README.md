# Smart Invoice Extractor

> An AI-powered invoice extraction system that automatically converts PDF invoices into structured JSON using FastAPI, Groq Llama 3.3, and Streamlit.

![CI](https://github.com/jospindev-stack/smart-invoice-extractor/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40.1-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## About

Smart Invoice Extractor is a full-stack application that extracts structured information from PDF invoices using artificial intelligence.

The application combines PDF text extraction with Groq Llama 3.3 to identify invoice metadata, vendor and customer information, line items, payment details, and financial totals. It exposes a REST API through FastAPI and provides a Streamlit interface for interactive document analysis.

---

## Technology Stack

| Category         | Technology     |
| ---------------- | -------------- |
| Backend          | FastAPI        |
| Frontend         | Streamlit      |
| AI               | Groq Llama 3.3 |
| PDF Processing   | pdfplumber     |
| Validation       | Pydantic       |
| Testing          | pytest         |
| Coverage         | pytest-cov     |
| CI               | GitHub Actions |
| Containerization | Docker         |

---

## Features

| Feature                      | Description                                   |
| ---------------------------- | --------------------------------------------- |
| PDF Parsing                  | Extract text from searchable PDF invoices     |
| AI Invoice Parsing           | Convert invoice text into structured JSON     |
| Vendor & Customer Extraction | Extract business information automatically    |
| Line Item Detection          | Parse products, quantities, prices, and taxes |
| Financial Totals             | Extract subtotal, tax, discount, and total    |
| Confidence Score             | AI confidence estimation for extracted data   |
| REST API                     | FastAPI endpoints for integration             |
| Interactive Interface        | Streamlit web application                     |
| Automated Tests              | API and PDF extraction tests with pytest      |
| Continuous Integration       | Automated test execution with GitHub Actions  |
| Docker Support               | Ready for containerized deployment            |

---

## AI Processing Workflow

```text
PDF Invoice
      |
      v
PDF Text Extraction (pdfplumber)
      |
      v
Raw Invoice Text
      |
      v
Groq Llama 3.3
      |
      v
Structured JSON
      |
      v
FastAPI REST API
      |
      v
Streamlit Interface
      |
      v
JSON / CSV / API Integration
```

---

## Project Structure

```text
smart-invoice-extractor/
|
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- backend/
|   |-- main.py
|   |-- config.py
|   |-- models/
|   |   `-- schemas.py
|   |-- routers/
|   |   `-- invoice.py
|   `-- services/
|       |-- pdf_extractor.py
|       `-- groq_parser.py
|-- frontend/
|   `-- app.py
|-- tests/
|   |-- conftest.py
|   |-- test_invoice_api.py
|   `-- test_pdf_extractor.py
|-- Dockerfile
|-- Dockerfile.frontend
|-- docker-compose.yml
|-- requirements.txt
|-- requirements-dev.txt
|-- .env.example
|-- run.bat
|-- run.sh
`-- README.md
```

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.11 or later
- A Groq API key
- Docker and Docker Compose (optional)

Groq API keys can be created from the Groq Console.

---

## Installation

```bash
git clone https://github.com/jospindev-stack/smart-invoice-extractor.git
cd smart-invoice-extractor

python -m venv .venv
```

Windows

```powershell
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Then set your Groq API key in `.env`:

```text
GROQ_API_KEY=your_api_key
```

---

## Running Locally

### Option 1 - Helper Script

Windows

```bash
run.bat
```

Linux / macOS

```bash
chmod +x run.sh
./run.sh
```

### Option 2 - Manual Startup

Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Frontend

```bash
streamlit run frontend/app.py
```

---

## Running with Docker

```bash
cp .env.example .env
docker compose up --build
```

Run in background:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

| Service    | URL                         |
| ---------- | --------------------------- |
| Streamlit  | http://localhost:8501       |
| FastAPI    | http://localhost:8000       |
| Swagger UI | http://localhost:8000/docs  |
| ReDoc      | http://localhost:8000/redoc |

---

## API Reference

### Extract Invoice

```text
POST /api/extract
```

Accepts a PDF invoice and returns structured JSON.

Request content type:

```text
multipart/form-data
```

| Field        | Type     | Description                        |
| ------------ | -------- | ---------------------------------- |
| invoice_file | PDF File | Searchable PDF invoice (max 20 MB) |

### Health Check

```text
GET /api/health
```

Returns the current API service status.

---

## Example Response

```json
{
  "status": "success",
  "filename": "invoice.pdf",
  "processing_time": 1.52,
  "invoice": {
    "invoice_number": "INV-2025-001",
    "invoice_date": "2025-03-12",
    "vendor": {
      "name": "Acme Ltd"
    },
    "buyer": {
      "name": "Example Company"
    },
    "subtotal": 1250,
    "tax_amount": 250,
    "total_amount": 1500,
    "confidence_score": 0.97
  }
}
```

---

## Supported PDF Requirements

The application currently supports:

- Searchable PDF invoices
- Digital invoices exported from accounting software
- Multi-page invoices
- English and French invoices

Scanned PDFs without an OCR text layer are not supported.

---

## Error Codes

| Status | Description                    |
| ------ | ------------------------------ |
| 200    | Invoice successfully processed |
| 400    | Invalid PDF file               |
| 413    | File exceeds maximum size      |
| 422    | No extractable text found      |
| 500    | AI processing failed           |

---

## Confidence Score

The AI returns a confidence score for each extraction.

| Score       | Interpretation                  |
| ----------- | ------------------------------- |
| 0.90 - 1.00 | Excellent extraction            |
| 0.80 - 0.89 | High confidence                 |
| 0.60 - 0.79 | Medium confidence               |
| Below 0.60  | Manual verification recommended |

---

## Testing

Development dependencies are isolated in `requirements-dev.txt`.

Install them with:

```bash
pip install -r requirements-dev.txt
```

Run the test suite with coverage:

```bash
pytest -q --cov=backend --cov-report=term-missing
```

The current suite covers:

- PDF text extraction and page counting
- skipping PDF pages without extractable text
- health endpoint behavior
- rejection of non-PDF uploads
- successful structured invoice responses with the Groq parser mocked
- rejection of PDFs without extractable text
- AI parser failure handling

Tests do not require a real Groq API call.

---

## Continuous Integration

GitHub Actions runs the test suite automatically on pushes to `main`, pushes to `test/**` branches, and pull requests targeting `main`.

The workflow uses Python 3.12 and validates the backend with pytest and coverage reporting.

---

## Environment Variables

| Variable           | Description                     |
| ------------------ | ------------------------------- |
| GROQ_API_KEY       | Groq API key                    |
| GROQ_MODEL         | Llama model used for extraction |
| BACKEND_URL        | Backend API URL                 |
| MAX_UPLOAD_SIZE_MB | Maximum PDF size                |

---

## Security

The application includes:

- Environment-based API key management
- File size validation
- PDF content type validation
- Structured JSON responses
- Server-side AI requests
- Pydantic response validation
- Configurable CORS policy

---

## Deployment

### Backend

Compatible with:

- Railway
- Render
- Docker
- Azure App Service
- Google Cloud Run

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

- GROQ_API_KEY
- GROQ_MODEL

### Frontend

The Streamlit application can be deployed with:

- Streamlit Community Cloud
- Docker
- Railway

Start command:

```bash
streamlit run frontend/app.py
```

---

## Roadmap

Planned improvements:

- OCR support for scanned invoices
- Image invoice support (PNG, JPG)
- Batch invoice processing
- Excel export
- ERP integration
- Multi-language invoice support
- User authentication
- Invoice history
- Search functionality
- More integration and edge-case tests

---

## Future Improvements

Possible future features include:

- Receipt extraction
- Purchase order parsing
- Expense categorization
- Accounting software integration
- AI anomaly detection
- Vendor analytics dashboard
- Automatic currency conversion
- Invoice comparison

---

## License

This project is licensed under the MIT License.

---

## Author

**Jospin Meka**

Software Developer

- GitHub: https://github.com/jospindev-stack
- Portfolio: https://jospindev.netlify.app
