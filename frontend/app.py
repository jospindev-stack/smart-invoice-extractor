import json
import os

import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Invoice Extractor",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    #MainMenu, header, footer { visibility: hidden; }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding: 2.4rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 { font-size: 2.4rem; margin: 0 0 .4rem; font-weight: 800; letter-spacing: -.5px; }
    .hero p  { font-size: 1.05rem; margin: 0; opacity: .85; }

    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
    }
    .card h3 { margin: 0 0 1rem; font-size: 1rem; color: #0f172a; text-transform: uppercase;
               letter-spacing: .6px; font-weight: 700; }

    .field-label { font-size: .75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;
                   letter-spacing: .4px; margin-bottom: .1rem; }
    .field-value { font-size: .95rem; color: #1e293b; font-weight: 500; margin-bottom: .7rem; }
    .field-null  { font-size: .92rem; color: #cbd5e1; font-style: italic; margin-bottom: .7rem; }

    .total-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        color: white;
        text-align: right;
    }
    .total-box .label { font-size: .8rem; opacity: .7; }
    .total-box .amount { font-size: 2.2rem; font-weight: 900; letter-spacing: -1px; }

    .confidence-badge {
        display: inline-block;
        padding: .3rem .9rem;
        border-radius: 12px;
        font-size: .82rem;
        font-weight: 700;
    }
    .conf-high   { background: #dcfce7; color: #15803d; }
    .conf-medium { background: #fef9c3; color: #854d0e; }
    .conf-low    { background: #fee2e2; color: #b91c1c; }

    .meta-row { font-size: .8rem; color: #64748b; text-align: center; margin-top: .6rem; }

    .divider { border: none; border-top: 1px solid #f1f5f9; margin: 1.2rem 0; }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1e3a5f, #3b82f6);
        border-radius: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _val(v, fmt: str = "") -> str:
    if v is None:
        return '<div class="field-null">—</div>'
    text = f"{v:{fmt}}" if fmt else str(v)
    return f'<div class="field-value">{text}</div>'


def _lbl(label: str) -> str:
    return f'<div class="field-label">{label}</div>'


def _field(label: str, value, fmt: str = "") -> str:
    return _lbl(label) + _val(value, fmt)


def _currency(amount, currency: str = "EUR") -> str:
    if amount is None:
        return "—"
    symbols = {"EUR": "€", "USD": "$", "GBP": "£"}
    sym = symbols.get(currency, currency + " ")
    return f"{amount:,.2f} {sym}"


def _confidence_badge(score: float) -> str:
    pct = int(score * 100)
    if score >= 0.80:
        cls, label = "conf-high", "Haute"
    elif score >= 0.50:
        cls, label = "conf-medium", "Moyenne"
    else:
        cls, label = "conf-low", "Faible"
    return f'<span class="confidence-badge {cls}">Confiance : {label} ({pct}%)</span>'


def _party_card(title: str, party: dict) -> None:
    fields = [
        ("Nom", party.get("name")),
        ("Adresse", party.get("address")),
        ("Email", party.get("email")),
        ("Téléphone", party.get("phone")),
        ("N° TVA / Tax ID", party.get("tax_id")),
        ("SIRET", party.get("siret")),
        ("Site web", party.get("website")),
    ]
    html = f'<div class="card"><h3>{title}</h3>'
    for label, value in fields:
        html += _field(label, value)
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def display_results(r: dict) -> None:
    inv = r["invoice"]
    currency = inv.get("currency") or "EUR"
    confidence = inv.get("confidence_score", 0.0)

    st.markdown("---")
    st.markdown("## Données extraites")

    # ── Meta bar ──────────────────────────────────────────────────────────────
    col_conf, col_meta = st.columns([1, 2])
    with col_conf:
        st.markdown(_confidence_badge(confidence), unsafe_allow_html=True)
        st.progress(confidence)
    with col_meta:
        st.markdown(
            f'<p class="meta-row">'
            f"Fichier : <b>{r['filename']}</b> &nbsp;·&nbsp; "
            f"{r['pages']} page(s) &nbsp;·&nbsp; "
            f"{r['text_length']:,} caractères &nbsp;·&nbsp; "
            f"Traitement : {r['processing_time']}s"
            f"</p>",
            unsafe_allow_html=True,
        )

    # ── Invoice header ────────────────────────────────────────────────────────
    st.markdown(
        '<div class="card"><h3>Informations générales</h3>'
        + _field("Numéro de facture", inv.get("invoice_number"))
        + _field("Date de facturation", inv.get("invoice_date"))
        + _field("Date d'échéance", inv.get("due_date"))
        + _field("Devise", currency)
        + "</div>",
        unsafe_allow_html=True,
    )

    # ── Vendor / Buyer ────────────────────────────────────────────────────────
    col_v, col_b = st.columns(2, gap="large")
    with col_v:
        _party_card("Vendeur / Émetteur", inv.get("vendor") or {})
    with col_b:
        _party_card("Acheteur / Client", inv.get("buyer") or {})

    # ── Line items ────────────────────────────────────────────────────────────
    line_items = inv.get("line_items") or []
    if line_items:
        st.markdown('<div class="card"><h3>Lignes de facturation</h3>', unsafe_allow_html=True)
        df = pd.DataFrame(line_items)
        col_labels = {
            "description": "Description",
            "quantity": "Qté",
            "unit": "Unité",
            "unit_price": f"Prix unitaire ({currency})",
            "tax_rate": "TVA (%)",
            "amount": f"Montant ({currency})",
        }
        df = df.rename(columns={k: v for k, v in col_labels.items() if k in df.columns})
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Aucune ligne de facturation détectée.")

    # ── Totals + payment ──────────────────────────────────────────────────────
    col_pay, col_total = st.columns([3, 2], gap="large")

    with col_pay:
        st.markdown(
            '<div class="card"><h3>Paiement</h3>'
            + _field("Conditions de paiement", inv.get("payment_terms"))
            + _field("Mode de paiement", inv.get("payment_method"))
            + _field("Coordonnées bancaires", inv.get("bank_details"))
            + _field("Notes", inv.get("notes"))
            + "</div>",
            unsafe_allow_html=True,
        )

    with col_total:
        subtotal = _currency(inv.get("subtotal"), currency)
        tax_rate = f"{inv.get('tax_rate', '—')} %" if inv.get("tax_rate") is not None else "—"
        tax_amt = _currency(inv.get("tax_amount"), currency)
        discount = _currency(inv.get("discount"), currency)
        total = _currency(inv.get("total_amount"), currency)

        st.markdown(
            '<div class="card"><h3>Récapitulatif</h3>'
            + _field("Sous-total HT", inv.get("subtotal") and subtotal)
            + _field("Taux de TVA", inv.get("tax_rate") and tax_rate)
            + _field("Montant TVA", inv.get("tax_amount") and tax_amt)
            + _field("Remise", inv.get("discount") and discount)
            + "</div>"
            + f'<div class="total-box"><div class="label">TOTAL TTC</div>'
            + f'<div class="amount">{total}</div></div>',
            unsafe_allow_html=True,
        )

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("")
    _, dl_col, _ = st.columns([1, 2, 1])
    with dl_col:
        filename = r.get("filename", "invoice").rsplit(".", 1)[0]
        st.download_button(
            label="Télécharger le JSON structuré",
            data=json.dumps(inv, ensure_ascii=False, indent=2),
            file_name=f"{filename}_extracted.json",
            mime="application/json",
            use_container_width=True,
        )


# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <h1>🧾 Smart Invoice Extractor</h1>
    <p>Uploadez une facture PDF &mdash; l'IA extrait automatiquement toutes les données
    structurées en quelques secondes et vous retourne un JSON propre et téléchargeable.</p>
</div>
""",
    unsafe_allow_html=True,
)

_, upload_col, _ = st.columns([1, 2, 1])
with upload_col:
    invoice_file = st.file_uploader(
        "Déposez votre facture PDF ici",
        type=["pdf"],
        help="Taille maximale : 20 MB. PDF avec couche texte requis (non scanné).",
    )
    if invoice_file:
        size_kb = invoice_file.size / 1024
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024:.2f} MB"
        st.success(f"Fichier chargé : **{invoice_file.name}** ({size_str})")

st.markdown("")
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    extract = st.button(
        "Extraire les données de la facture",
        use_container_width=True,
        type="primary",
        disabled=invoice_file is None,
        help="Uploadez un PDF pour activer l'extraction.",
    )

if invoice_file is None:
    st.info("Uploadez une facture PDF pour démarrer l'extraction automatique.")

if extract and invoice_file is not None:
    with st.spinner("Extraction en cours... L'IA analyse votre facture."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/extract",
                files={"invoice_file": (invoice_file.name, invoice_file.getvalue(), "application/pdf")},
                timeout=90,
            )
        except requests.exceptions.ConnectionError:
            st.error(
                f"Impossible de joindre le backend sur `{BACKEND_URL}`. "
                "Vérifiez qu'il est démarré (`uvicorn backend.main:app --reload`)."
            )
            st.stop()
        except requests.exceptions.Timeout:
            st.error("Le serveur a mis trop de temps à répondre. Réessayez.")
            st.stop()

    if response.status_code == 200:
        display_results(response.json())
    else:
        try:
            detail = response.json().get("detail", response.text)
        except Exception:
            detail = response.text
        st.error(f"Erreur {response.status_code} : {detail}")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ℹ️ À propos")
    st.markdown(
        """
**Smart Invoice Extractor** utilise Groq (LLaMA 3.3 70B) pour extraire
automatiquement toutes les données d'une facture PDF.

**Données extraites :**
- Vendeur & acheteur (nom, adresse, TVA, SIRET…)
- Numéro, date, échéance
- Lignes de facturation (qté, prix, TVA)
- Sous-total, TVA, total TTC
- Conditions & coordonnées bancaires

**Format supporté :**
PDF avec couche texte (généré par logiciel).
Les PDF scannés sans OCR ne sont pas supportés.

**Score de confiance :**
- 🟢 ≥ 80% — données claires
- 🟡 50-79% — quelques ambiguïtés
- 🔴 < 50% — vérifiez manuellement
"""
    )
    st.markdown("---")
    st.markdown(f"**Backend :** `{BACKEND_URL}`\n\n[Swagger UI]({BACKEND_URL}/docs)")
