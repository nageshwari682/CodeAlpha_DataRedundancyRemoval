# Data Redundancy Removal System

A system that identifies and prevents redundant data using a two-layer validation approach.

## How it works
- **Layer 1 (Exact Duplicate Detection):** Each record is hashed (SHA-256) based on name + email. If the exact same hash exists, the record is rejected.
- **Layer 2 (Near-Duplicate Detection):** New records are compared against existing ones using fuzzy string matching (fuzzywuzzy). If similarity crosses a threshold, the record is flagged for review instead of being silently added or rejected.

## Tech Stack
- Python, Flask
- SQLite
- fuzzywuzzy + python-Levenshtein

## How to run
1. `pip install -r requirements.txt`
2. `python app.py`
3. Open `http://127.0.0.1:5000`

## Screenshots
## Screenshots

**Accepted:**


![Accepted](screenshot/accepted.png)



**Rejected (exact duplicate):**


![Rejected](screenshot/rejected.png)



**Flagged (near duplicate):**


![Flagged](screenshot/flagged.png)