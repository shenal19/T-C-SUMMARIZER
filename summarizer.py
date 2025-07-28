import spacy
import json
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

with open("clause_keywords.json", encoding="utf-8") as f:
    CLAUSES = json.load(f)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def get_relevant_clauses(text):
    summary = {tag: [] for tag in CLAUSES}
    doc = nlp(text)

    for sent in doc.sents:
        cleaned = sent.text.strip()
        lowered = cleaned.lower()
        for tag, keywords in CLAUSES.items():
            if any(f" {keyword} " in lowered for keyword in keywords):

                if len(cleaned) > 150:
                    cleaned = cleaned[:150].rsplit('.', 1)[0].rsplit(' ', 1)[0] + '...'
                if cleaned not in summary[tag] and len(summary[tag]) < 3:
                    summary[tag].append(f"• {cleaned}")

    matched = sum(1 for val in summary.values() if val)
    total = len(CLAUSES)
    score = round((matched / total) * 100, 2)

    return {
        "clauses": summary,
        "score": score
    }
