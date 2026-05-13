# Palmer LTER Seabird Scripts
# Script to convert 2024 Seabird files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024
# Usage (from cruise/original):
#   python convert_cruise_2024.py

import pandas as pd
import numpy as np
from common import convertDate, check_output

# -------------------------
# 2024 Cruise Transect Header
# -------------------------

df = pd.read_excel('2024/TRANSECT_HEADER_23-24FINAL.xlsx', dtype='str');
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
df.insert(0,'studyName', 'LMG24-01')
df.insert(1,'Cruise', '2401')
df.insert(2,'Year/Month', 'TBD')
df['Year/Month'] = np.where(df['Event Number'].astype('int')>=114, '2024-01', '2023-12')

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

df.to_csv('../formatted/Cruise_Transect_Header/Cruise_Transect_Header_2024.csv', index=False)
check_output(df, 'Cruise_Transect_Header', '2024')


# -------------------------
# 2024 Cruise Transect Observations
# -------------------------

df = pd.read_excel('2024/TRANSECT_OBS_23-24FINAL.xlsx');
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
df.insert(0,'studyName', 'LMG24-01')
df.insert(1,'Cruise', '2401')

df.to_csv('../formatted/Cruise_Transect_Observations/Cruise_Transect_Observations_2024.csv', index=False)
check_output(df, 'Cruise_Transect_Observations', '2024')


# -------------------------
# 2024 Cruise Stationary Header
# -------------------------
df = pd.read_excel('2024/STATIONARY_HEADER_23-24FINAL.xlsx', dtype='str')
df = df.rename(columns={
  'STATION': 'Station',
  'EVENT': 'Event Number',
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
  'DEPTH': 'Depth',
  'SST': 'SST',
  'Notes': 'Notes'
})
df.insert(0, 'studyName', 'LMG24-01')
df.insert(1, 'Cruise', '2401')
df.insert(2, 'Year/Month', 'TBD')
df['Year/Month'] = np.where(df['Event Number'].astype(int) >= 103, '2024-01', '2023-12')
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

df.to_csv('../formatted/Cruise_Stationary_Header/Cruise_Stationary_Header_2024.csv', index=False)
check_output(df, 'Cruise_Stationary_Header', '2024')

# -------------------------
# 2024 Cruise Stationary Observations
# -------------------------
df = pd.read_excel('2024/STATIONARY_OBS_23-24FINAL.xlsx')
df = df.rename(columns={
  'Event': 'Event Number',
  'Minutes': 'Count Minute',
  'Taxon': 'Species',
  'Number': 'Number',
  'Link': 'Linkages',
  'Behavior': 'Behavior',
  'Direction': 'Direction',
  'Notes': 'Notes',
  'Stern Count Start': 'Stern Count Start',
  'Stern Count End': 'Stern Count End'
})
df.insert(0, 'studyName', 'LMG24-01')
df.insert(1, 'Cruise', '2401')
df.to_csv('../formatted/Cruise_Stationary_Observations/Cruise_Stationary_Observations_2024.csv', index=False)
check_output(df, 'Cruise_Stationary_Observations', '2024')
