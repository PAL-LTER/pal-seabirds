# Palmer LTER Seabird Scripts
# Module: QC Rule Dispatchers
# Written by Sage Lichtenwalner, Rutgers University
# AI assistance: Substantial development support provided by GitHub Copilot (GPT-5.3-Codex).
# Final review and approval: Sage Lichtenwalner
# Revised 5/13/2026
#
# This module implements standardized rule-check functions for cruise QC validation.
# Each function follows the signature: (rule, data, params) -> {count, bad_rows, column_name, explanation}
# Functions are registered in CHECK_FUNCTIONS dict, which is dispatched by qc_cruise.py.
#
# Architecture: This layer is the application/dispatch tier; it wraps utility functions from lib_qc_utility
# in standardized rule implementations. Domain logic (masks, helpers) lives in lib_qc_utility.
#
# Usage (from cruise/):
#   imported by qc_cruise.py via: from lib_qc_checks import CHECK_FUNCTIONS

import pandas as pd
import lib_qc_utility as qc


def _get_table_df(data, table):
    if table == "header":
        return data["header"]
    if table == "obs":
        return data["obs"]
    raise ValueError(f"Unknown table '{table}'")


def _empty_result(column_name, explanation=""):
    return {
        "count": 0,
        "bad_rows": pd.DataFrame(),
        "column_name": column_name,
        "explanation": explanation,
    }


def datetime_parseable(rule, data, params):
    df = _get_table_df(data, rule["table"])
    col = rule["column_name"]
    if col not in df.columns:
        return _empty_result(col, f"Missing column: {col}")
    mask = qc.mask_datetime_unparseable(df, col)
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": col,
        "explanation": f"{col} is not parseable",
    }


def numeric_range(rule, data, params):
    df = _get_table_df(data, rule["table"])
    col = rule["column_name"]
    if col not in df.columns:
        return _empty_result(col, f"Missing column: {col}")
    minimum = float(params["min"])
    maximum = float(params["max"])
    mask = qc.mask_numeric_out_of_range(df, col, minimum, maximum)
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": col,
        "explanation": f"{col} outside range [{minimum}, {maximum}]",
    }


def numeric_parseable_nonempty(rule, data, params):
    df = _get_table_df(data, rule["table"])
    col = rule["column_name"]
    if col not in df.columns:
        return _empty_result(col, f"Missing column: {col}")
    if col == "Event Number":
        mask = qc.mask_event_number_bad(df, col)
    else:
        s = df[col].fillna("").astype(str).str.strip()
        num = pd.to_numeric(s, errors="coerce")
        mask = (s == "") | num.isna()
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": col,
        "explanation": f"{col} must be parseable and non-empty",
    }


def non_negative_integer(rule, data, params):
    df = _get_table_df(data, rule["table"])
    col = rule["column_name"]
    if col not in df.columns:
        return _empty_result(col, f"Missing column: {col}")
    allow_blank = str(params.get("allow_blank", "false")).lower() == "true"
    mask = qc.mask_non_negative_integer(df, col, allow_blank=allow_blank)
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": col,
        "explanation": f"{col} must be integer and non-negative" + (" (blank allowed)" if allow_blank else ""),
    }


def duplicate_rows_on_keys(rule, data, params):
    df = _get_table_df(data, rule["table"])
    raw_keys = params["keys"]
    sep = "|" if "|" in raw_keys else ","
    keys = [k.strip() for k in raw_keys.split(sep)]
    missing = [c for c in keys if c not in df.columns]
    if missing:
        return _empty_result(rule["column_name"], f"Missing key columns: {', '.join(missing)}")
    row_mask = df.duplicated(keys, keep=False)
    dup_count = int(df.duplicated(keys).sum())
    return {
        "count": dup_count,
        "bad_rows": df[row_mask],
        "column_name": "|".join(keys),
        "explanation": f"Duplicate rows on keys: {'|'.join(keys)}",
    }


def header_key_unique(rule, data, params):
    header = data["header"]
    raw_keys = params["keys"]
    sep = "|" if "|" in raw_keys else ","
    keys = [k.strip() for k in raw_keys.split(sep)]
    missing = [c for c in keys if c not in header.columns]
    if missing:
        return _empty_result(rule["column_name"], f"Missing key columns: {', '.join(missing)}")
    row_mask = qc.duplicate_key_mask(header, keys)
    dup_count = qc.duplicate_key_count(header, keys)
    return {
        "count": dup_count,
        "bad_rows": header[row_mask],
        "column_name": "|".join(keys),
        "explanation": "Header key is duplicated",
    }


def obs_maps_to_header(rule, data, params):
    header = data["header"]
    obs = data["obs"]
    raw_keys = params["keys"]
    sep = "|" if "|" in raw_keys else ","
    keys = [k.strip() for k in raw_keys.split(sep)]
    missing_header = [c for c in keys if c not in header.columns]
    missing_obs = [c for c in keys if c not in obs.columns]
    if missing_header or missing_obs:
        msg = []
        if missing_header:
            msg.append(f"missing header keys: {', '.join(missing_header)}")
        if missing_obs:
            msg.append(f"missing obs keys: {', '.join(missing_obs)}")
        return _empty_result(rule["column_name"], "; ".join(msg))
    bad = qc.unmatched_obs_df(obs, header, keys)
    return {
        "count": int(bad.shape[0]),
        "bad_rows": bad,
        "column_name": "|".join(keys),
        "explanation": "Observation key has no matching header key",
    }


def header_has_obs(rule, data, params):
    header = data["header"]
    obs = data["obs"]
    raw_keys = params["keys"]
    sep = "|" if "|" in raw_keys else ","
    keys = [k.strip() for k in raw_keys.split(sep)]
    missing_header = [c for c in keys if c not in header.columns]
    missing_obs = [c for c in keys if c not in obs.columns]
    if missing_header or missing_obs:
        msg = []
        if missing_header:
            msg.append(f"missing header keys: {', '.join(missing_header)}")
        if missing_obs:
            msg.append(f"missing obs keys: {', '.join(missing_obs)}")
        return _empty_result(rule["column_name"], "; ".join(msg))
    bad = qc.orphan_header_df(header, obs, keys)
    return {
        "count": int(bad.shape[0]),
        "bad_rows": bad,
        "column_name": "|".join(keys),
        "explanation": "Header key has no matching observation row",
    }


def marker_absent(rule, data, params):
    df = _get_table_df(data, rule["table"])
    raw_cols = params["columns"]
    sep = "|" if "|" in raw_cols else ","
    cols = [c.strip() for c in raw_cols.split(sep) if c.strip() in df.columns]
    if not cols:
        return _empty_result(rule["column_name"], "No scan columns available")
    marker_re = qc.marker_mask
    combined = pd.Series(False, index=df.index)
    for col in cols:
        combined = combined | marker_re(df[col], qc.MARKERS)
    return {
        "count": int(combined.sum()),
        "bad_rows": df[combined],
        "column_name": ",".join(cols),
        "explanation": "Contains conversion warning marker token",
    }


def studyname_consistent_within_cruise(rule, data, params):
    df = _get_table_df(data, rule["table"])
    required = ["studyName", "Cruise"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        return _empty_result(rule["column_name"], f"Missing columns: {', '.join(missing)}")

    bad_cruises = qc.inconsistent_studyname_cruises(df)
    if not bad_cruises:
        return _empty_result(rule["column_name"], "")

    mask = df["Cruise"].isin(bad_cruises)
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": "studyName|Cruise",
        "explanation": "studyName is inconsistent within Cruise",
    }


def required_column_present(rule, data, params):
    df = _get_table_df(data, rule["table"])
    col = rule["column_name"]
    if col in df.columns:
        return _empty_result(col, "")
    # Missing-column checks are metadata-level, not row-level.
    return {
        "count": 1,
        "bad_rows": pd.DataFrame(),
        "column_name": col,
        "explanation": f"Missing required column: {col}",
    }


def yearmonth_format(rule, data, params):
    df = _get_table_df(data, rule["table"])
    col = rule["column_name"]
    if col not in df.columns:
        return _empty_result(col, f"Missing column: {col}")
    mask = qc.mask_yearmonth_format(df, col)
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": col,
        "explanation": f"{col} must be YYYY-MM",
    }


def yearmonth_datetime_match(rule, data, params):
    df = _get_table_df(data, rule["table"])
    required = ["Year/Month", "DateTime"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        return _empty_result(rule["column_name"], f"Missing columns: {', '.join(missing)}")
    mask = qc.mask_yearmonth_datetime_mismatch(df)
    return {
        "count": int(mask.sum()),
        "bad_rows": df[mask],
        "column_name": "Year/Month|DateTime",
        "explanation": "Year/Month month does not match DateTime month",
    }


def multi_numeric_range(rule, data, params):
    df = _get_table_df(data, rule["table"])
    raw_cols = params["columns"]
    sep = "|" if "|" in raw_cols else ","
    cols = [c.strip() for c in raw_cols.split(sep)]
    minimum = float(params["min"])
    maximum = float(params["max"])

    existing = [c for c in cols if c in df.columns]
    if not existing:
        return _empty_result(rule["column_name"], f"Missing columns: {', '.join(cols)}")

    combined = pd.Series(False, index=df.index)
    for col in existing:
        combined = combined | qc.mask_numeric_out_of_range(df, col, minimum, maximum)

    return {
        "count": int(combined.sum()),
        "bad_rows": df[combined],
        "column_name": "|".join(existing),
        "explanation": f"Values outside range [{minimum}, {maximum}]",
    }


def h23_domain(rule, data, params):
    df = _get_table_df(data, rule["table"])
    combined = pd.Series(False, index=df.index)
    if "Sea State" in df.columns:
        combined = combined | qc.mask_sea_state_invalid(df, "Sea State")
    if "Ice Cover" in df.columns:
        combined = combined | qc.mask_ice_cover_invalid(df, "Ice Cover")
    if "Ice Type" in df.columns:
        combined = combined | qc.mask_token_not_allowed(df, "Ice Type", qc.ICE_TYPE_ALLOWED)
    if "Ice Color" in df.columns:
        combined = combined | qc.mask_token_not_allowed(df, "Ice Color", qc.ICE_COLOR_ALLOWED)
    return {
        "count": int(combined.sum()),
        "bad_rows": df[combined],
        "column_name": "Sea State|Ice Cover|Ice Type|Ice Color",
        "explanation": "Sea/ice values outside empirical cruise domains",
    }


CHECK_FUNCTIONS = {
    "required_column_present": required_column_present,
    "studyname_consistent_within_cruise": studyname_consistent_within_cruise,
    "datetime_parseable": datetime_parseable,
    "yearmonth_format": yearmonth_format,
    "yearmonth_datetime_match": yearmonth_datetime_match,
    "numeric_range": numeric_range,
    "multi_numeric_range": multi_numeric_range,
    "numeric_parseable_nonempty": numeric_parseable_nonempty,
    "non_negative_integer": non_negative_integer,
    "duplicate_rows_on_keys": duplicate_rows_on_keys,
    "header_key_unique": header_key_unique,
    "obs_maps_to_header": obs_maps_to_header,
    "header_has_obs": header_has_obs,
    "marker_absent": marker_absent,
    "h23_domain": h23_domain,
}
