# Palmer LTER Seabird Processing Scripts
# Common functions for processing data
# Written by Sage Lichtenwalner, Rutgers University
# Revised 8/21/2024

import pandas as pd
from datetime import datetime

def standardize_time(time_value):
  """
  Convert various time formats to 'hh:mm'.
  Handles 'hhmm', 'hh:mm', and 'hh:mm:ss' formats.
  """
  if pd.isna(time_value):
      return None
  
  # Convert to string if it's not already
  time_str = str(time_value)
  
  # Define possible formats
  formats = [
      "%H%M",   # hhmm
      "%H:%M",  # hh:mm
      "%H:%M:%S" # hh:mm:ss
  ]
  
  # Try each format until one matches
  for fmt in formats:
      try:
          # Parse the time string
          dt = datetime.strptime(time_str, fmt)
          # Return the standardized format
          return dt.strftime("%H:%M")
      except ValueError:
          continue
  
  # If no format matched, return the original time_str
  return time_str


def convertStudy(n):
  """Convert a SEASON integer (e.g. 9899) to a PAL study name (e.g. PAL9899)."""
  sy = n % 100
  if sy == 99:
    ey = 0
  else:
    ey = sy + 1
  return "PAL%s%s" % (str(sy).zfill(2), str(ey).zfill(2))


def check_output(df, name, year, empty_ok=False):
  """Basic post-conversion validation: row count, studyName present, Date nulls."""
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
  if 'Date' in df.columns and df['Date'].isna().any():
    print(f"  WARNING {name} {year}: {df['Date'].isna().sum()} null(s) in 'Date'")
