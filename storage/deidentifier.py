# text_cleaning/deid.py
from utils.logger import log

try:
    import spacy
    try:
        # Load spaCy model for NER (using a general English model; could use a clinical NER model if available)
        nlp = spacy.load("en_core_web_sm")
    except OSError:  # model not found
        log("Warning: spaCy model 'en_core_web_sm' not found. PHI will not be removed.")
        nlp = None
except ModuleNotFoundError:  # spaCy not installed at all
    log("Warning: spaCy is not installed. PHI will not be removed.")
    nlp = None

# Define which entity labels to redact (PHI categories)
PHI_LABELS = {"PERSON", "ORG", "GPE", "LOC", "FAC", "DATE"}  # Names, Orgs, Geographical, Facilities, Dates, etc.

def deidentify_text(text: str) -> str:
    """Remove or mask PHI entities from the input text."""
    if nlp is None:
        # spaCy unavailable, just return original text
        log("deidentifier unavailable - returning input text")
        return text

    doc = nlp(text)
    cleaned_text = text
    # Optional feedback via logging
    log("deidentifier loaded")

    for ent in doc.ents:
        if ent.label_ in PHI_LABELS:
            # Replace the entity text with a generic tag to indicate removal
            placeholder = f"[{ent.label_}]"
            cleaned_text = cleaned_text.replace(ent.text, placeholder)
    return cleaned_text
