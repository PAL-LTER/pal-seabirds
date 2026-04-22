# Palmer LTER Seabird
# Script to convert Fraser data files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024

import pandas as pd
from datetime import datetime, timedelta

def convertCruise(n):
  yr = str(n)[:2]
  if yr in(['93','94','95','96','97']):
    return "PD%s-01" % (str(yr).zfill(2))
  elif yr in(['98','99']):
    return "LMG%s-01" % (str(yr).zfill(2))
  elif (int(yr)>=0 & int(yr)<=20):
    return "LMG%s-01" % (str(yr).zfill(2))
  else:
    return "UNKNOWN"

def convertDate(yymm, dddhhmm):
  try:
      # Parse the year and month
      year = int(yymm[:2])
      month = int(yymm[2:])
      
      if not (0 <= year <= 99) or not (1 <= month <= 12):
          return f"Error: Invalid YYMM format '{yymm}'"
      
      year += 1900 if year >= 90 else 2000
      
      # Parse the Julian day, hour, and minute from the end of the string
      if len(dddhhmm) < 5:
          return f"Error: Invalid DDDHHMM format '{dddhhmm}'"
      
      minute = int(dddhhmm[-2:])
      hour = int(dddhhmm[-4:-2])
      julian_day = int(dddhhmm[:-4])
      
      if not (1 <= julian_day <= 366) or not (0 <= hour < 24) or not (0 <= minute < 60):
          return f"Error: Invalid values in DDDHHMM format '{dddhhmm}'"
      
      # Construct the base date from January 1st of the given year
      base_date = datetime(year, 1, 1) + timedelta(days=julian_day - 1)
      
      # Check if the month of the base date matches the given month
      if base_date.month != month:
          return f"Error: Mismatch between month in YYMM ('{yymm}') and Julian day in DDDHHMM ('{dddhhmm}')"
      
      # Combine the base date with the hour and minute
      final_datetime = base_date.replace(hour=hour, minute=minute)
      
      return final_datetime
      
  except Exception as e:
      return f"Error: {str(e)}"

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
  
def fixYM(ym, ev):
  #9401 after and including event 452 - Change month to 9402, Add 31 to JD
  if (ym=='9401' and int(ev)>=452):
    return '9402'
  #9601 976,977 - Change YM to 9602
  elif (ym=='9601' and ev in(['976','977'])):
    return '9602'
  #9701 Event 959 - Change YM to 9702, Add 31 to JD
  elif (ym=='9701' and ev=='959'):
    return '9702'
  #1901 - YM needs to be changed to 1902 after event 380
  elif (ym=='1901' and ev>='380'):
    return '9402'
  else:
    return ym

def fixJD(ym,jd):
  if ym in(['9402','9502','9702','9902']):
    return str(int(jd)+310000)
  else:
    return jd

# 102	Bird Census Log Moving - Summer
df = pd.read_excel('2020_Fraser/CRUISE HEADER.xls', dtype='str'); #Load all columns as str objects
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
df['Year/Month'] = df.apply(lambda row: fixYM(row['Year/Month'], row['Event Number']), axis=1)
df['YearDay/Hour/Minute'] = df.apply(lambda row: fixJD(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Export to CSV
df.to_csv('out/Cruise_Transect_Header_1993_2020.csv', index=False)
print(df.dtypes)

# -------------------------
# 100 Bird Census Moving - Summer
df = pd.read_excel('2020_Fraser/CRUISE TRANSECT.xls', dtype={'CRUISE':'str'});
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

# Export to CSV
df.to_csv('out/Cruise_Transect_Observations_1993_2020.csv', index=False)
print(df.dtypes)



# CRUISE HEADER - DATE ISSUES
# 9401 after and including event 452 - Change month to 9402, Add 31 to JD
# 9502 - Add 31 to JD
# 9601 976,977 - Change YM to 9602
# 9701 Event 959 - Change YM to 9702, Add 31 to JD
# 9702 - Add 31 to JD
# 98 is a mess
# 9902 - Add 31 to JD
# 1901 - YM needs to be changed to 1902 after event 380
