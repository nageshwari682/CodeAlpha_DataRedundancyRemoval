import hashlib
import sqlite3
from fuzzywuzzy import fuzz
from database import get_all_records

def generate_hash(name, email):
    combined = f"{name.strip().lower()}{email.strip().lower()}"
    return hashlib.sha256(combined.encode()).hexdigest()

def is_exact_duplicate(record_hash):
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM records WHERE record_hash = ?", (record_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def is_near_duplicate(name, email, threshold=90):
    existing_records = get_all_records()
    for existing_name, existing_email in existing_records:
        name_score = fuzz.ratio(name.lower(), existing_name.lower())
        email_score = fuzz.ratio(email.lower(), existing_email.lower())
        if name_score >= threshold or email_score >= threshold:
            return True, existing_name, existing_email
    return False, None, None

def validate_and_classify(name, email):
    record_hash = generate_hash(name, email)

    if is_exact_duplicate(record_hash):
        return {"status": "rejected", "reason": "exact_duplicate"}

    near_dup, match_name, match_email = is_near_duplicate(name, email)
    if near_dup:
        return {
            "status": "flagged",
            "reason": "possible_false_positive",
            "similar_to": {"name": match_name, "email": match_email}
        }

    return {"status": "accepted", "hash": record_hash}