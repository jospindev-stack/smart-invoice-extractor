import json

from groq import Groq

from ..config import settings

client = Groq(api_key=settings.groq_api_key)

_SYSTEM_PROMPT = """You are an expert invoice data extraction system with deep knowledge of French and international invoice formats.

Extract ALL structured data from the invoice text provided by the user.
Respond with valid JSON only — no markdown fences, no commentary, no extra text.

Rules:
- Use null for any field not found in the document — never invent data.
- Dates must be formatted as ISO 8601 strings: "YYYY-MM-DD". If only month/year is visible, use the 1st of the month.
- All monetary amounts must be plain floats (no currency symbols).
- Infer the currency from symbols (€→EUR, $→USD, £→GBP) or explicit mentions; default to "EUR".
- tax_rate is a percentage as a float (e.g., 20.0 for 20%).
- confidence_score: float between 0.0 (very uncertain) and 1.0 (all data clearly readable).
  Use 0.9+ only when all major fields (vendor, buyer, total, date) are unambiguous.

Return exactly this JSON structure (include every key, even if null):
{
  "invoice_number": "<string or null>",
  "invoice_date": "<YYYY-MM-DD or null>",
  "due_date": "<YYYY-MM-DD or null>",
  "currency": "<ISO 4217 code or null>",
  "vendor": {
    "name": "<string or null>",
    "address": "<full address string or null>",
    "email": "<string or null>",
    "phone": "<string or null>",
    "tax_id": "<VAT/tax number or null>",
    "siret": "<SIRET number or null>",
    "website": "<string or null>"
  },
  "buyer": {
    "name": "<string or null>",
    "address": "<full address string or null>",
    "email": "<string or null>",
    "phone": "<string or null>",
    "tax_id": "<string or null>",
    "siret": "<string or null>",
    "website": null
  },
  "line_items": [
    {
      "description": "<string>",
      "quantity": <float or null>,
      "unit": "<string or null>",
      "unit_price": <float or null>,
      "tax_rate": <float or null>,
      "amount": <float or null>
    }
  ],
  "subtotal": <float or null>,
  "tax_rate": <float or null>,
  "tax_amount": <float or null>,
  "discount": <float or null>,
  "total_amount": <float or null>,
  "payment_terms": "<string or null>",
  "payment_method": "<string or null>",
  "bank_details": "<IBAN / bank info string or null>",
  "notes": "<any additional notes or null>",
  "confidence_score": <float 0.0–1.0>
}"""


def parse_invoice(text: str) -> dict:
    """Send extracted invoice text to Groq and return structured dict."""
    user_content = f"Extract all invoice data from the following text:\n\n---\n{text[:settings.max_text_chars]}\n---"

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.1,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
