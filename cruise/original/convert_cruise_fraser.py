# Palmer LTER Seabird Scripts
# Script to convert Fraser data files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024
# Usage (from cruise/original):
#   python convert_cruise_fraser.py

import re

import pandas as pd
from common import convertDate, check_output


def toIsoYearMonth(value):
  """Normalize source Year/Month text and return ISO format YYYY-MM."""
  match = re.search(r'\d+', str(value).strip())
  if not match:
    return ''
  yymm = match.group(0).zfill(4)[:4]
  year = int(yymm[:2])
  month = int(yymm[2:])
  year += 1900 if year >= 90 else 2000
  return f'{year:04d}-{month:02d}'


def convertCruise(n):
  """Map Cruise code to studyName (PD/LMG), defaulting to UNKNOWN."""
  match = re.search(r'\d+', str(n).strip())
  if not match:
    return 'UNKNOWN'
  # Zero-fill to 4 so 3-digit values like 901 are treated as 0901.
  yr = match.group(0).zfill(4)[:2]
  if yr in(['93','94','95','96','97']):
    return "PD%s-01" % (str(yr).zfill(2))
  elif yr in(['98','99']):
    return "LMG%s-01" % (str(yr).zfill(2))
  elif (int(yr) >= 0 and int(yr) <= 20):
    return "LMG%s-01" % (str(yr).zfill(2))
  else:
    return "UNKNOWN"

def fixLonLat(v):
  try:
      value_float = float(v)
  except ValueError:
      return 'Bad Input: %s' % v
  is_negative = value_float < 0
  value_float = abs(value_float)
  # Determine if the value is in DDM format
  if '.' in str(value_float) and len(str(int(value_float))) > 2:
      degrees = int(value_float // 100)
      minutes = value_float % 100
      # Validate minutes (should be less than 60)
      if minutes >= 60:
          return 'Bad Minutes: %s' % v
      decimal_degrees = round(degrees + minutes / 60, 5) #Truncate digits
      if is_negative:
          decimal_degrees = -decimal_degrees
  else:
    # Otherwise, assume it's already in decimal degrees
    # decimal_degrees = -abs(value_float) if value_float > 0 else value_float
    decimal_degrees = -value_float # Force negative value
  
  if decimal_degrees > 0: # Force negative degrees
    decimal_degrees = -decimal_degrees
  if abs(decimal_degrees)>180:
    return 'Bad Value: %s' % v
  else:
    return decimal_degrees

# CRUISE HEADER - DATE ISSUES
# 9401 - After and including event 452, change YM to 9402
# 9402 - Add 31 to JD
# 9502 - Add 31 to JD
# 9601 - After and including event 947, change YM to 9602
# 9701 - After and including event 959, change YM to 9702
# 9702 - Add 31 to JD
# 9801 - After and including event 105, change YM to 9802
# 9802 - Add 31 to JD
# 9902 - Add 31 to JD
# 0302 - Add 31 to JD
# 0702 - Before event 739, change YM to 0701 
# 1901 - After and including event 365, change YM to 1902

def fixYM(ym, ev):
  """Apply known Fraser month corrections, then normalize to YYYY-MM."""
  ym = re.search(r'\d+', str(ym).strip())
  ym = ym.group(0).zfill(4)[:4] if ym else ''
  try:
    ev_num = int(float(ev))
  except Exception:
    ev_num = None
  # 9401 - After and including event 452, change YM to 9402
  if (ym=='9401' and ev_num is not None and ev_num >= 452):
    return '1994-02'
  # 9601 - After and including event 947, change YM to 9602
  elif (ym=='9601' and ev_num is not None and ev_num >= 947):
    return '1996-02'
  # 9701 - After and including event 959, change YM to 9702
  elif (ym=='9701' and ev_num is not None and ev_num >= 959):
    return '1997-02'
  # 9801 - After and including event 105, change YM to 9802
  elif (ym=='9801' and ev_num is not None and ev_num >= 105):
    return '1998-02'
  # 0702 - Before event 739, change YM to 0701
  elif (ym=='0702' and ev_num is not None and ev_num < 739):
    return '2007-01'
  # 1901 - After and including event 365, change YM to 1902
  elif (ym=='1901' and ev_num is not None and ev_num >= 365):
    return '2019-02'
  else:
    return toIsoYearMonth(ym)

def fixJD(ym,jd):
  """Apply known Julian-day offsets for corrected February year-month buckets."""
  if ym in(['1994-02','1995-02','1997-02','1998-02','1999-02','2003-02']):
    return str(int(float(jd)) + 310000)
  else:
    return jd

# -------------------------
# Fraser Cruise Transect Header
# 102	Bird Census Log Moving - Summer
# -------------------------

df = pd.read_excel('2020_fraser/CRUISE HEADER.xls', dtype='str'); #Load all columns as str objects
df = df.rename(columns={
    'CRUISE': 'Cruise',
    'YRMO': 'Year/Month',
    'FROM': 'Station Start',
    'TO': 'Station End',
    'EVENT': 'Event Number',
    'GMT': 'YearDay/Hour/Minute',
    'TTIME': 'Total Time',
    'SPEED': 'Ship Speed',
    'COURSE': 'Ship Course',
    'STARTLAT': 'Latitude Start',
    'STARTLONG': 'Longitude Start',
    'ENDLAT': 'Latitude End',
    'ENDLONG': 'Longitude End',
    'WIND SPEED (START)': 'Wind Speed Start',
    'WIND DIRECTION (START)': 'Wind Direction Start',
    'WIND SPEED (END)': 'Wind Speed End',
    'WIND DIRECTION (END)': 'Wind Direction End',
    'SEA_ST': 'Sea State',
    'SALINITY': 'Salinity',
    'FLUOROMETRY': 'Fluorometry',
    'HAB': 'Habitat',
    'COVER': 'Ice Cover',
    'ICE_TY': 'Ice Type',
    'ICE_COL': 'Ice Color',
    'DEPTH': 'Depth',
    'NOTES': 'Notes'})

# Add studyName from Cruise
df.insert(0,'studyName', 'TBD')
df['studyName'] = df['Cruise'].map(convertCruise)

# Fix Lon/Lat Issues
df['OLD Latitude Start'] = df['Latitude Start']
df['OLD Longitude Start'] = df['Longitude Start']
df['OLD Latitude End'] = df['Latitude End']
df['OLD Longitude End'] = df['Longitude End']
df['Latitude Start'] = df['Latitude Start'].map(fixLonLat)
df['Longitude Start'] = df['Longitude Start'].map(fixLonLat)
df['Latitude End'] = df['Latitude End'].map(fixLonLat)
df['Longitude End'] = df['Longitude End'].map(fixLonLat)

# Fix Date Issues
df['OLD YearDay/Hour/Minute'] = df['YearDay/Hour/Minute']
df['Year/Month'] = df.apply(lambda row: fixYM(row['Year/Month'], row['Event Number']), axis=1)
df['YearDay/Hour/Minute'] = df.apply(lambda row: fixJD(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

# Export to CSV
df.to_csv('../formatted/Cruise_Transect_Header/Cruise_Transect_Header_1993_2020.csv', index=False)
check_output(df, 'Cruise_Transect_Header', '1993_2020')

# -------------------------
# Fraser Cruise Transect Observations
# 100 Bird Census Moving - Summer
# -------------------------

df = pd.read_excel('2020_fraser/CRUISE TRANSECT.xls', dtype={'CRUISE':'str'});
df = df.rename(columns={
  'CRUISE': 'Cruise',
  'EVENT': 'Event Number',
  'TIME': 'Count Minute',
  'TAXA': 'Species',
  'NUMBER': 'Number',
  'LINK': 'Linkages',
  'BEH': 'Behavior',
  'DIR': 'Direction',
  'NOTES': 'Notes'
})

# Add studyName from Cruise
df.insert(0,'studyName', 'TBD')
df['studyName'] = df['Cruise'].map(convertCruise)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
if 'YearDay/Hour/Minute' in df.columns:
  df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

# Export to CSV
df.to_csv('../formatted/Cruise_Transect_Observations/Cruise_Transect_Observations_1993_2020.csv', index=False)
check_output(df, 'Cruise_Transect_Observations', '1993_2020')


# -------------------------
# Fraser Cruise Stationary Header and Observations - combined file, split into header + obs
# 98 Cruise Stationary (Bird Census Log Stationary - Summer)
# Fraser combined file has one row per observation; split into header + obs.
# -------------------------

df = pd.read_excel('2020_fraser/CRUISE STATIONARY.xls', dtype='str')
df = df.rename(columns={
    'CRUISE': 'Cruise',
    'YRMO': 'Year/Month',
    'STATION': 'Station',
    'EVENT': 'Event Number',
    'DEPTH': 'Depth',
    'LAT': 'Latitude',
    'LONG': 'Longitude',
    'GMT': 'YearDay/Hour/Minute',
    'SEA_ST': 'Sea State',
    'SALINITY': 'Salinity',
    'FLUOROMETRY': 'Fluorometry',
    'WIND SPEED': 'Wind Speed',
    'WIND DIRECTION': 'Wind Direction',
    'HAB': 'Habitat',
    'COVER': 'Ice Cover',
    'ICE_TY': 'Ice Type',
    'ICE_COL': 'Ice Color',
    'TIME': 'Count Minute',
    'TAXA': 'Species',
    'NUMBER': 'Number',
    'LINK': 'Linkages',
    'BEH': 'Behavior',
    'DIR': 'Direction',
    'NOTES': 'Notes'
})
df.insert(0, 'studyName', df['Cruise'].map(convertCruise))

# Fix Lon/Lat Issues for stationary records using same converter as transect header.
df['OLD Latitude'] = df['Latitude']
df['OLD Longitude'] = df['Longitude']
df['Latitude'] = df['Latitude'].map(fixLonLat)
df['Longitude'] = df['Longitude'].map(fixLonLat)

# Apply the same Year/Month + Julian-day cleanup used for transect header.
df['OLD YearDay/Hour/Minute'] = df['YearDay/Hour/Minute']
df['Year/Month'] = df.apply(lambda row: fixYM(row['Year/Month'], row['Event Number']), axis=1)
df['YearDay/Hour/Minute'] = df.apply(lambda row: fixJD(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Header: one row per event (station)
HEADER_COLS = [
    'studyName', 'Cruise', 'Year/Month', 'Station', 'Event Number',
    'Latitude', 'Longitude', 'YearDay/Hour/Minute',
    'Sea State', 'Salinity', 'Fluorometry', 'Wind Speed', 'Wind Direction',
    'Habitat', 'Ice Cover', 'Ice Type', 'Ice Color', 'Depth', 'Notes'
]
hdr = df[HEADER_COLS].drop_duplicates(subset=['Cruise', 'Event Number'])
hdr['DateTime'] = hdr.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
hdr['YearDay/Hour/Minute'] = hdr['YearDay/Hour/Minute'].astype(str)

hdr.to_csv('../formatted/Cruise_Stationary_Header/Cruise_Stationary_Header_1993_2020.csv', index=False)
check_output(hdr, 'Cruise_Stationary_Header', '1993_2020')

# Observations: one row per bird count
OBS_COLS = [
    'studyName', 'Cruise', 'Event Number',
    'Count Minute', 'Species', 'Number', 'Linkages', 'Behavior', 'Direction', 'Notes'
]
obs = df[OBS_COLS]
obs.to_csv('../formatted/Cruise_Stationary_Observations/Cruise_Stationary_Observations_1993_2020.csv', index=False)
check_output(obs, 'Cruise_Stationary_Observations', '1993_2020')
