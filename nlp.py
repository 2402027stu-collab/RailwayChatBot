import re


# =========================================================
# TRAIN NUMBER
# =========================================================

def extract_train_number(text):

    match = re.search(r"\b\d{5}\b", text)

    if match:
        return match.group()

    return None


# =========================================================
# STATION CODE
# =========================================================

def extract_station_code(text):

    matches = re.findall(
        r"\b[A-Z]{2,5}\b",
        text.upper()
    )

    return matches


# =========================================================
# SOURCE & DESTINATION
# =========================================================

def extract_source_destination(text):

    text = text.strip()

    # -----------------------------------------------------
    # 1. "Trains from Mumbai to Goa"
    # -----------------------------------------------------

    match = re.search(
        r"\bfrom\s+(.+?)\s+to\s+(.+?)(?:\s*$|\?)",
        text,
        re.IGNORECASE
    )

    if match:

        source = match.group(1).strip()
        destination = match.group(2).strip()

        return source, destination


    # -----------------------------------------------------
    # 2. "Trains between Mumbai and Goa"
    # -----------------------------------------------------

    match = re.search(
        r"\bbetween\s+(.+?)\s+and\s+(.+?)(?:\s*$|\?)",
        text,
        re.IGNORECASE
    )

    if match:

        source = match.group(1).strip()
        destination = match.group(2).strip()

        return source, destination


    # -----------------------------------------------------
    # 3. "Mumbai to Goa"
    # -----------------------------------------------------

    match = re.search(
        r"^(.+?)\s+to\s+(.+?)(?:\s*$|\?)",
        text,
        re.IGNORECASE
    )

    if match:

        source = match.group(1).strip()
        destination = match.group(2).strip()

        # Remove common words from beginning
        source = re.sub(
            r"^(trains?|railway|show|find|search)\s+",
            "",
            source,
            flags=re.IGNORECASE
        ).strip()

        return source, destination


    return None, None


# =========================================================
# INTENT DETECTION
# =========================================================

def detect_intent(text):

    text = text.lower().strip()


    # -----------------------------------------------------
    # TRAIN BETWEEN TWO PLACES
    # -----------------------------------------------------

    if (
        "between" in text
        or re.search(r"\bfrom\b.+\bto\b", text)
        or re.search(r"\bto\b", text)
    ):
        return "between"


    # -----------------------------------------------------
    # SCHEDULE
    # -----------------------------------------------------

    elif (
        "schedule" in text
        or "timetable" in text
        or "timing" in text
    ):
        return "schedule"


    # -----------------------------------------------------
    # STATION
    # -----------------------------------------------------

    elif "station" in text:
        return "station"


    # -----------------------------------------------------
    # TRAIN DETAILS
    # -----------------------------------------------------

    elif (
        "train" in text
        or "detail" in text
        or "information" in text
    ):
        return "train"


    # -----------------------------------------------------
    # ONLY TRAIN NUMBER
    # -----------------------------------------------------

    elif re.search(r"\b\d{5}\b", text):
        return "train"


    return "unknown"