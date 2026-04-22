# Palmer LTER Seabird
# Script to convert 2023 Seabird files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024

import pandas as pd
from datetime import datetime, timedelta

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


df = pd.read_excel('2023/Cruise/TRANSECT_HEADER_22-23FINAL.xlsx', dtype='str');
df = df.rename(columns={
  'FROM':'Station Start',
  'TO':'Station End',
  'EVENT':'Event Number',
  'GMT':'YearDay/Hour/Minute',
  'TTIME':'Total Time',
  'SPEED':'Ship Speed',
  'COURSE':'Ship Course',
  'STARTLAT':'Latitude Start',
  'STARTLONG':'Longitude Start',
  'ENDLAT':'Latitude End',
  'ENDLONG':'Longitude End',
  'WIND SPEED (START)':'Wind Speed Start',
  'WIND DIRECTION (START)':'Wind Direction Start',
  'WIND SPEED (END)':'Wind Speed End',
  'WIND DIRECTION (END)':'Wind Direction End',
  'SEA_ST':'Sea State',
  'SALINITY':'Salinity',
  'FLUOROMETRY':'Fluorometry',
  'HAB':'Habitat',
  'COVER':'Ice Cover',
  'ICE_TY':'Ice Type',
  'ICE_COL':'Ice Color',
  'DEPTH':'Depth',
  'SST':'SST',
  'notes':'Notes'})

# Add missing columns
df.insert(0,'studyName', 'LMG23-01')
df.insert(1,'Cruise', '2301')
df.insert(2,'Year/Month', '2301')

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

df.to_csv('out/Cruise_Transect_Header_2023.csv', index=False)
print(df.dtypes)


# -------------------------
df = pd.read_excel('2023/Cruise/TRANSECT_OBS_22-23FINAL.xlsx');
df = df.rename(columns={
  'EVENT':'Event Number',
  'MINUTES':'Count Minute',
  'TAXON':'Species',
  'NUM':'Number',
  'BEH':'Behavior',
  'DIR':'Direction',
  'LINK':'Linkages',
  'NOTES':'Notes',
  'Stern Count Start':'Stern Count Start',
  'Stern Count End':'Stern Count End'})

# Add missing columns
df.insert(0,'studyName', 'LMG23-01')
df.insert(1,'Cruise', '2301')

# Delete suprious column
df.drop(['Unnamed: 10'], axis=1, inplace=True)

df.to_csv('out/Cruise_Transect_Observations_2023.csv', index=False)
print(df.dtypes)
