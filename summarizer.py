import spacy
import json
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

# Load clause keywords
with open("clause_keywords.json", encoding="utf-8") as f:
    CLAUSES = json.load(f)

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

# concise clause-based summary
def get_relevant_clauses(text):
    summary = {tag: [] for tag in CLAUSES}
    doc = nlp(text)

    for sent in doc.sents:
        cleaned = sent.text.strip()
        lowered = cleaned.lower()
        for tag, keywords in CLAUSES.items():
            if any(keyword in lowered for keyword in keywords):
                # Keep only first 150 characters (cutting at last full stop or space)
                if len(cleaned) > 150:
                    cleaned = cleaned[:150].rsplit('.', 1)[0].rsplit(' ', 1)[0] + '...'
                # Add only unique and relevant bullets (max 2-3 per tag)
                if cleaned not in summary[tag] and len(summary[tag]) < 3:
                    summary[tag].append(f"• {cleaned}")
    return summary
