import re

# -----------------------------
# Train Number
# -----------------------------
def extract_train_number(text):

    match = re.search(r"\b\d{5}\b", text)

    if match:
        return match.group()

    return None


# -----------------------------
# Station Code
# -----------------------------
def extract_station_code(text):

    matches = re.findall(r"\b[A-Z]{2,5}\b", text.upper())

    return matches


# -----------------------------
# Source & Destination
# -----------------------------
def extract_source_destination(text):

    # Mumbai to Delhi
    match = re.search(r"(.+?)\s+to\s+(.+)", text, re.IGNORECASE)

    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Trains from Mumbai to Delhi
    match = re.search(r"from\s+(.+?)\s+to\s+(.+)", text, re.IGNORECASE)

    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Trains between Mumbai and Delhi
    match = re.search(r"between\s+(.+?)\s+and\s+(.+)", text, re.IGNORECASE)

    if match:
        return match.group(1).strip(), match.group(2).strip()

    return None, None


# -----------------------------
# Intent Detection
# -----------------------------
def detect_intent(text):

    text = text.lower()

    # Train between two places
    if "between" in text or " to " in text or ("from" in text and "to" in text):
        return "between"

    # Schedule
    elif "schedule" in text or "timetable" in text or "timing" in text:
        return "schedule"

    # Station
    elif "station" in text:
        return "station"

    # Train details
    elif "train" in text or "detail" in text or "information" in text:
        return "train"

    # If user enters only a train number (e.g. 04601)
    elif re.search(r"\b\d{5}\b", text):
        return "train"

    return "unknown"