import spacy

# Load specialized healthcare model or fall back to general spaCy model
try:
    nlp = spacy.load("en_ner_bc5cdr_md")  # Use a specialized model for biomedical data if available
except:
    nlp = spacy.load("en_core_web_sm")    # Fallback to general spaCy model

def generate_boolean_query(user_query):
    doc = nlp(user_query)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    boolean_query = " AND ".join(keywords)
    return boolean_query

def search_database(boolean_query, database):
    query_terms = set(boolean_query.split(" AND "))
    results = []
    for entry in database:
        if query_terms.intersection(set(entry["terms"])):
            results.append(entry)
    return results
