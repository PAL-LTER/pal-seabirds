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
