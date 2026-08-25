# ==========================================
# CITY -> RAILWAY STATION CODE MAPPING
# ==========================================

CITY_STATIONS = {

    # ======================================
    # MUMBAI
    # ======================================

    "mumbai": [
        "ADH",
        "BA",
        "MSD",
        "BVI",
        "BY",
        "DIC",
        "GMN",
        "JOS",
        "KLMC",
        "KLMG",
        "KILE",
        "KHAR",
        "MDD",
        "BDTS",
        "CHG",
        "CSTM",
        "CRD",
        "DR",
        "DDR",
        "MM",
        "MTN",
        "MRU",
        "PR",
        "SNRD",
        "SIN",
        "BCT",
        "EPR",
        "PL",
        "MX",
        "STC",
        "TPND",
        "VLP"
    ],


    # ======================================
    # GOA
    # ======================================

    "goa": [
        "BLLI",
        "CNO",
        "CSM",
        "CNR",
        "DBM",
        "KM",
        "KRMI",
        "QLM",
        "MAO",
        "MJO",
        "PERN",
        "SJDA",
        "SKVL",
        "SVM",
        "SRVX",
        "THVM",
        "VSG",
        "VEN"
    ],


    # ======================================
    # DELHI
    # ======================================

    "delhi": [
        "ANDI",
        "ASE",
        "BWSN",
        "BRSQ",
        "CNKP",
        "DBSI",
        "DAZ",
        "DEC",
        "NZM",
        "DKZ",
        "DSB",
        "DSJ",
        "DEE",
        "DSA",
        "DSAP",
        "DSBP",
        "DSBC",
        "HNZM",
        "GHE",
        "DLPI",
        "KRTN",
        "LPNR",
        "LDCY",
        "MGLP",
        "MQC",
        "NNO",
        "NRVR",
        "NDLS",
        "DLI",
        "PM",
        "PTNR",
        "ROHN",
        "SDPR",
        "SOJ",
        "SWNR",
        "SMDP",
        "SSB",
        "VVB",
        "VVKP"
    ],


    # ======================================
    # BANGALORE
    # ======================================

    "bangalore": [
        "SBC",
        "YPR",
        "BNC",
        "BNCE",
        "KJM",
        "KJM-D",
        "BAND",
        "BYPL",
        "YNK",
        "HEB",
        "LOGH",
        "BNKH",
        "KIAD",
        "BWT",
        "WFD"
    ],

    # Bangalore alternative spelling
    "bengaluru": [
        "SBC",
        "YPR",
        "BNC",
        "BNCE",
        "KJM",
        "KJM-D",
        "BAND",
        "BYPL",
        "YNK",
        "HEB",
        "LOGH",
        "BNKH",
        "KIAD",
        "BWT",
        "WFD"
    ]
}


# ==========================================
# CITY NAME ALIASES
# ==========================================

CITY_ALIASES = {

    "bombay": "mumbai",

    "mumbai city": "mumbai",

    "new delhi": "delhi",

    "ncr": "delhi",

    "bangalore city": "bangalore",

    "bengaluru city": "bengaluru"
}


# ==========================================
# GET STATION CODES
# ==========================================

def get_station_codes(city):

    """
    Convert a city name into all known railway
    station codes for that city.

    Example:

        get_station_codes("Mumbai")

    returns:

        ['ADH', 'BA', 'MSD', ..., 'VLP']
    """

    if not city:
        return []

    # Clean input
    city = city.strip().lower()

    # Check aliases
    if city in CITY_ALIASES:
        city = CITY_ALIASES[city]

    # Return station codes
    return CITY_STATIONS.get(city, [])


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("Mumbai codes:")
    print(get_station_codes("Mumbai"))

    print("\nGoa codes:")
    print(get_station_codes("Goa"))

    print("\nDelhi codes:")
    print(get_station_codes("Delhi"))

    print("\nBangalore codes:")
    print(get_station_codes("Bangalore"))