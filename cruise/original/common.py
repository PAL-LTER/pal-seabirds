# Palmer LTER Seabird Scripts
# Shared helper functions for cruise conversion scripts
# Written by Sage Lichtenwalner, Rutgers University
# Revised 4/29/2026

from datetime import datetime, timedelta


def convertDate(yymm, dddhhmm):
  try:
    # Parse the year and month.
    year = int(str(yymm)[:2])
    month = int(str(yymm)[2:])

    if not (0 <= year <= 99) or not (1 <= month <= 12):
      return f"Error: Invalid YYMM format '{yymm}'"

    year += 1900 if year >= 90 else 2000

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
        f"Error: Mismatch between month in YYMM ('{yymm}') and Julian day in "
        f"DDDHHMM ('{dddhhmm}')"
      )

    return base_date.replace(hour=hour, minute=minute)

  except Exception as e:
    return f"Error: {str(e)}"
