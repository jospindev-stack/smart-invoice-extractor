from typing import List, Optional

from pydantic import BaseModel, Field


class Party(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tax_id: Optional[str] = None
    siret: Optional[str] = None
    website: Optional[str] = None


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    tax_rate: Optional[float] = None
    amount: Optional[float] = None


class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    currency: Optional[str] = None
    vendor: Party = Field(default_factory=Party)
    buyer: Party = Field(default_factory=Party)
    line_items: List[LineItem] = Field(default_factory=list)
    subtotal: Optional[float] = None
    tax_rate: Optional[float] = None
    tax_amount: Optional[float] = None
    discount: Optional[float] = None
    total_amount: Optional[float] = None
    payment_terms: Optional[str] = None
    payment_method: Optional[str] = None
    bank_details: Optional[str] = None
    notes: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence 0–1")


class InvoiceResponse(BaseModel):
    status: str
    filename: str
    pages: int
    text_length: int
    processing_time: float
    invoice: InvoiceData
