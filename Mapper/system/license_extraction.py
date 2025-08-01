# license_extraction.py (Allied version)

def extract_state_license_blocks_and_notes(text: str, skip_expired=True):
    """
    Allied does not require license block extraction; always return empty results.
    This keeps code compatible with RN pipeline structure.
    """
    return [], {}
