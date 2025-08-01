# processing.py (Allied version)
import pandas as pd
from helpers import ensure_str_columns

def process_general_info(allied_df, general_template):
    """Map Allied fields to BlueSky General Info template columns."""
    # Only keep columns found in template
    output = allied_df.copy()
    output = output[[c for c in general_template.columns if c in output.columns]]
    output = output.fillna("")
    return ensure_str_columns(output)

def process_required_docs(allied_df, reqdoc_template):
    """Explode Allied Certifications into individual required docs rows (no blanks if none)."""
    reqdoc_rows = []
    for _, row in allied_df.iterrows():
        pid = row.get("Id")
        certs_raw = row.get("Allied Certifications", None)
        if (
            certs_raw is not None
            and str(certs_raw).strip()
            and str(certs_raw).strip().lower() != "nan"
        ):
            certs = str(certs_raw).split(',')
            for cert in certs:
                cert = cert.strip()
                if cert:
                    reqdoc_rows.append({
                        "Person_key": pid,
                        "CertificationCredentialName": cert,
                        "IssueComment": "",
                        "Expiration Date": "",
                        "Note": "",
                        "Verified": ""
                    })
    if not reqdoc_rows:
        return pd.DataFrame(columns=reqdoc_template.columns)
    return ensure_str_columns(pd.DataFrame(reqdoc_rows, columns=reqdoc_template.columns))

def process_specialties(allied_df, specialty_template):
    """Explode Allied/Ancillary Specialty 1/2/3 into individual specialty rows with deduplication."""
    specialty_rows = []
    
    for _, row in allied_df.iterrows():
        pid = row.get("Id")
        
        # Step 1: Collect all specialties from all 3 columns
        all_specialties = []
        for idx in range(1, 4):
            col = f"Allied/Ancillary Specialty {idx}"
            val = row.get(col, "")
            if pd.notna(val) and val:
                # Split comma-separated values and clean them
                for part in str(val).split(','):
                    part = part.strip()
                    if part:
                        all_specialties.append(part)
        
        # Step 2: Remove duplicates while preserving order (first occurrence)
        unique_specialties = []
        seen = set()
        for specialty in all_specialties:
            # Case-insensitive comparison for deduplication
            specialty_lower = specialty.lower()
            if specialty_lower not in seen:
                unique_specialties.append(specialty)
                seen.add(specialty_lower)
        
        # Step 3: Create rows for each unique specialty
        for specialty in unique_specialties:
            specialty_rows.append({
                "Person_key": pid,
                "Specialty": specialty,
                "Complete": "",
                "Complete Date": "",
                "Expiration Date": "",
                "UploadedFile": ""
            })
    
    if not specialty_rows:
        return pd.DataFrame(columns=specialty_template.columns)
    return ensure_str_columns(pd.DataFrame(specialty_rows, columns=specialty_template.columns))
