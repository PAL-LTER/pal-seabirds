# Palmer LTER Seabird Scripts
# Module: QC Utility Functions & Constants
# Written by Sage Lichtenwalner, Rutgers University
# AI assistance: Substantial development support provided by GitHub Copilot (GPT-5.3-Codex).
# Final review and approval: Sage Lichtenwalner
# Revised 5/13/2026
#
# This module provides reusable utilities for cruise QC validation:
# - Constants: domains, markers, file references for transect/stationary data
# - Data Loading: load_inputs() for reading merged cruise data
# - Mask Functions: boolean Series for identifying invalid values (yearmonth format, datetime parsing, etc.)
# - Helper Functions: duplicate/orphan detection, study name consistency checks
#
# Used by: lib_qc_checks.py (validation dispatcher) and qc_cruise.py (rule runner)
# Architecture: This layer is the data/utility tier; lib_qc_checks wraps these in standardized rule functions.
#
# Usage (from cruise/):
#   imported by qc_cruise.py and lib_qc_checks.py

import os
import re
import pandas as pd

REQUIRED_FILES = {
    "transect_header": "Cruise_Transect_Header_merged.csv",
    "transect_obs": "Cruise_Transect_Observations_merged.csv",
    "stationary_header": "Cruise_Stationary_Header_merged.csv",
    "stationary_obs": "Cruise_Stationary_Observations_merged.csv",
}

# Shared regional bounds used by both validator and exporter.
WAP_LAT_MIN = -75.0
WAP_LAT_MAX = -60.0
WAP_LON_MIN = -85.0
WAP_LON_MAX = -50.0

MARKERS = ["Bad Input", "Bad Minutes", "Bad Value", "UNKNOWN"]

# Empirical domains observed in merged cruise header data.
SEA_STATE_ALLOWED_TEXT = {"0-7 KNOTS", "17-21 KNOTS"}
ICE_TYPE_ALLOWED = {"", "0", "1", "2", "3", "4", "FLOES"}
ICE_COLOR_ALLOWED = {"", "0", "1", "2", "3", "BROWN"}


def load_inputs(merged_dir, dtype_str=False, add_source_rows=False):
    paths = {k: os.path.join(merged_dir, v) for k, v in REQUIRED_FILES.items()}
    missing = [p for p in paths.values() if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError("Missing required merged file(s):\n%s" % "\n".join(missing))

    data = {}
    for key, path in paths.items():
        df = pd.read_csv(path, dtype=str if dtype_str else None)
        if add_source_rows:
            df["_source_index"] = df.index
            df["_source_row_number"] = df.index + 2
        data[key] = df
    return data


def mask_yearmonth_format(df, col="Year/Month"):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    values = df[col].fillna("").astype(str)
    return ~values.str.fullmatch(r"\d{4}-\d{2}")


def mask_datetime_unparseable(df, col="DateTime"):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    parsed = pd.to_datetime(df[col], errors="coerce")
    return parsed.isna()


def mask_yearmonth_datetime_mismatch(df):
    if "Year/Month" not in df.columns or "DateTime" not in df.columns:
        return pd.Series(False, index=df.index)

    ym = df["Year/Month"].fillna("").astype(str)
    ym_valid = ym.str.fullmatch(r"\d{4}-\d{2}")
    ym_month = pd.to_numeric(ym.str[-2:], errors="coerce")

    dt = pd.to_datetime(df["DateTime"], errors="coerce")
    dt_valid = dt.notna()
    dt_month = dt.dt.month

    comparable = ym_valid & dt_valid
    mismatch = comparable & (ym_month != dt_month)
    return mismatch.fillna(False)


def mask_nonempty_non_numeric(df, col):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    s = df[col].fillna("").astype(str).str.strip()
    numeric = pd.to_numeric(s, errors="coerce")
    return (s != "") & numeric.isna()


def mask_event_number_bad(df, col="Event Number"):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    s = df[col].fillna("").astype(str).str.strip()
    num = pd.to_numeric(s, errors="coerce")
    return (s == "") | num.isna()


def mask_non_negative_integer(df, col, allow_blank=False):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    s = df[col].fillna("").astype(str).str.strip()
    num = pd.to_numeric(s, errors="coerce")
    integer_like = (num % 1 == 0)
    if allow_blank:
        bad = ((s != "") & (num.isna() | (num < 0) | (~integer_like)))
    else:
        bad = (s == "") | num.isna() | (num < 0) | (~integer_like)
    return bad.fillna(True)


def mask_numeric_out_of_range(df, col, minimum, maximum):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    numeric = pd.to_numeric(df[col], errors="coerce")
    return ((numeric < minimum) | (numeric > maximum)).fillna(False)


def mask_sea_state_invalid(df, col="Sea State"):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    s = df[col].fillna("").astype(str).str.strip().str.upper()
    nonblank = s != ""
    num = pd.to_numeric(s, errors="coerce")
    valid_numeric = num.between(0, 9, inclusive="both")
    valid_text = s.isin(SEA_STATE_ALLOWED_TEXT)
    return (nonblank & ~(valid_numeric | valid_text)).fillna(False)


def mask_ice_cover_invalid(df, col="Ice Cover"):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    s = df[col].fillna("").astype(str).str.strip()
    nonblank = s != ""
    num = pd.to_numeric(s, errors="coerce")
    valid_numeric = num.between(0, 8, inclusive="both")
    return (nonblank & ~valid_numeric).fillna(False)


def mask_token_not_allowed(df, col, allowed_values):
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    vals = df[col].fillna("").astype(str).str.strip().str.upper()
    return (~vals.isin(allowed_values)).fillna(False)


def marker_mask(series, markers):
    marker_re = re.compile("|".join(re.escape(m) for m in markers), re.IGNORECASE)
    s = series.fillna("").astype(str)
    return s.str.contains(marker_re, na=False)


def duplicate_key_count(df, key_cols):
    return int(df.duplicated(key_cols).sum())


def duplicate_key_mask(df, key_cols):
    return df.duplicated(key_cols, keep=False)


def unmatched_obs_df(obs_df, header_df, key_cols):
    h = header_df[key_cols].drop_duplicates().assign(_matched=1)
    merged = obs_df.merge(h, on=key_cols, how="left")
    return merged[merged["_matched"].isna()]


def orphan_header_df(header_df, obs_df, key_cols):
    o = obs_df[key_cols].drop_duplicates().assign(_matched=1)
    merged = header_df[key_cols].drop_duplicates().merge(o, on=key_cols, how="left")
    return merged[merged["_matched"].isna()]


def inconsistent_studyname_cruises(df):
    grouped = df[["studyName", "Cruise"]].drop_duplicates().groupby("Cruise")["studyName"].nunique()
    return set(grouped[grouped > 1].index)
