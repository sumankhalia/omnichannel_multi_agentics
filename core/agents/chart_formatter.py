import numpy as np


def normalize_chart_data(df):

    if df is None or len(df) == 0:
        return []

    numeric_cols = df.select_dtypes(include=np.number).columns
    all_cols = df.columns.tolist()

    if len(all_cols) < 2:
        return []

    # PRIORITY → categorical + numeric pairing
    if len(numeric_cols) >= 1:

        value_key = numeric_cols[0]

        label_candidates = [c for c in all_cols if c != value_key]

        label_key = label_candidates[0]

    else:
        # Fallback → first two columns
        label_key = all_cols[0]
        value_key = all_cols[1]

    records = df.to_dict(orient="records")

    normalized = []

    for row in records:

        try:
            normalized.append({
                "label": str(row[label_key]),
                "value": float(row[value_key])
            })
        except Exception:
            continue

    return normalized