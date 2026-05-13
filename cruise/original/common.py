# Palmer LTER Seabird Scripts
# Shared helper functions for cruise conversion scripts
# Written by Sage Lichtenwalner, Rutgers University
# Revised 4/29/2026

from datetime import datetime, timedelta


def parseYearMonth(year_month):
  """Parse Year/Month as either YYYY-MM or YYMM and return (year, month)."""
  text = str(year_month).strip()
  if "-" in text:
    parts = text.split("-", 1)
    if len(parts) != 2 or len(parts[0]) != 4 or len(parts[1]) != 2:
      raise ValueError(f"Invalid YYYY-MM value '{year_month}'")
    if not parts[0].isdigit() or not parts[1].isdigit():
      raise ValueError(f"Invalid YYYY-MM value '{year_month}'")
    return int(parts[0]), int(parts[1])

  # No-dash values must be exactly YYMM.
  if len(text) != 4 or not text.isdigit():
    raise ValueError(f"Invalid YYMM value '{year_month}'")
  yy = int(text[:2])
  month = int(text[2:])
  year = 1900 + yy if yy >= 90 else 2000 + yy
  return year, month


def convertDate(year_month, dddhhmm):
  """Convert Year/Month + DDDHHMM to datetime, returning an error string on failure."""
  try:
    # Parse the year and month.
    year, month = parseYearMonth(year_month)

    if not (1 <= month <= 12):
      return f"Error: Invalid Year/Month format '{year_month}'"

    # Parse the Julian day, hour, and minute from the end of the string.
    dddhhmm = str(dddhhmm)
    if len(dddhhmm) < 5:
      return f"Error: Invalid DDDHHMM format '{dddhhmm}'"

    minute = int(dddhhmm[-2:])
    hour = int(dddhhmm[-4:-2])
    julian_day = int(dddhhmm[:-4])

    if not (1 <= julian_day <= 366) or not (0 <= hour < 24) or not (0 <= minute < 60):
      return f"Error: Invalid values in DDDHHMM format '{dddhhmm}'"

    base_date = datetime(year, 1, 1) + timedelta(days=julian_day - 1)

    if base_date.month != month:
      return (
        f"Error: Mismatch between month in Year/Month ('{year_month}') and Julian day in "
        f"DDDHHMM ('{dddhhmm}')"
      )

    return base_date.replace(hour=hour, minute=minute)

  except Exception as e:
    return f"Error: {str(e)}"


def check_output(df, name, year, empty_ok=False):
  """Basic post-conversion summary used by cruise converter scripts."""
  if len(df) == 0:
    if empty_ok:
      print(f"  {name} {year}: 0 rows (expected empty)")
    else:
      print(f"  WARNING {name} {year}: 0 rows")
    return
  print(f"  {name} {year}: {len(df)} rows")
  if 'studyName' not in df.columns:
    print(f"  ERROR {name} {year}: missing 'studyName' column")
  elif df['studyName'].isna().any():
    print(f"  WARNING {name} {year}: {df['studyName'].isna().sum()} null(s) in 'studyName'")
  if 'DateTime' in df.columns and df['DateTime'].isna().any():
    print(f"  WARNING {name} {year}: {df['DateTime'].isna().sum()} null(s) in 'DateTime'")
