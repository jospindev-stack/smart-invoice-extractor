# Smart Invoice Extractor

> An AI-powered invoice extraction system that automatically converts PDF invoices into structured JSON using FastAPI, Groq Llama 3.3, and Streamlit.

![Python](...)
![FastAPI](...)
![Streamlit](...)
![Groq](...)
![Docker](...)
![License](https://img.shields.io/badge/License-MIT-green)

---

## About

Smart Invoice Extractor is a full-stack application that extracts structured information from PDF invoices using artificial intelligence.

The application combines PDF text extraction with Groq Llama 3.3 to automatically identify invoice metadata, vendor and customer information, line items, payment details, and financial totals. It exposes a REST API through FastAPI and provides an intuitive Streamlit interface for interactive document analysis.

---

## Technology Stack

| Category         | Technology     |
| ---------------- | -------------- |
| Backend          | FastAPI        |
| Frontend         | Streamlit      |
| AI               | Groq Llama 3.3 |
| PDF Processing   | pdfplumber     |
| Validation       | Pydantic       |
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
| Docker Support               | Ready for containerized deployment            |

---

## AI Processing Workflow

```text
PDF Invoice
      │
      ▼
PDF Text Extraction (pdfplumber)
      │
      ▼
Raw Invoice Text
      │
      ▼
Groq Llama 3.3
      │
      ▼
Structured JSON
      │
      ▼
FastAPI REST API
      │
      ▼
Streamlit Interface
      │
      ▼
JSON • CSV • API Integration
```

---

## Project Structure

```text
smart-invoice-extractor/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   └── schemas.py
│   ├── routers/
│   │   └── invoice.py
│   └── services/
│       ├── pdf_extractor.py
│       └── groq_parser.py
│
├── frontend/
│   └── app.py
│
├── Dockerfile
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── run.bat
├── run.sh
└── README.md
```

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.11 or later
- A free Groq API key
- Docker & Docker Compose (optional)

Create a free API key at:

https://console.groq.com

---

## Installation

```bash
# Clone the repository
git clone https://github.com/jospindev-stack/smart-invoice-extractor.git

cd smart-invoice-extractor

# Create a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit the `.env` file and add your Groq API key.

```text
GROQ_API_KEY=your_api_key
```

---

## Running Locally

### Option 1 – Helper Script

Windows

```bash
run.bat
```

Linux / macOS

```bash
chmod +x run.sh
./run.sh
```

### Option 2 – Manual Startup

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

Run in background

```bash
docker compose up -d
```

Stop services

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

```
POST /api/extract
```

Accepts a PDF invoice and returns structured JSON.

### Request

Content-Type

```
multipart/form-data
```

| Field        | Type     | Description                        |
| ------------ | -------- | ---------------------------------- |
| invoice_file | PDF File | Searchable PDF invoice (max 20 MB) |

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

Scanned PDFs without OCR are not supported.

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
| 0.90 – 1.00 | Excellent extraction            |
| 0.80 – 0.89 | High confidence                 |
| 0.60 – 0.79 | Medium confidence               |
| Below 0.60  | Manual verification recommended |

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

The application includes several security features:

- Environment-based API key management
- File size validation
- PDF file validation
- Structured JSON responses
- Server-side AI requests
- Pydantic request validation
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

Start command

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables

- GROQ_API_KEY
- GROQ_MODEL

---

### Frontend

Deploy the Streamlit application on:

- Streamlit Community Cloud
- Docker
- Railway

Start command

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
- Unit tests
- Integration tests

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

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute it under the terms of the MIT License.

---

## Author

**Jospin Meka**

Software Developer

Passionate about backend development, artificial intelligence, cloud technologies, and software architecture.

- GitHub: https://github.com/jospindev-stack
- Portfolio: https://jospindev.netlify.app
