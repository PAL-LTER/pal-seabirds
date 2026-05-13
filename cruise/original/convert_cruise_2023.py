# Palmer LTER Seabird Scripts
# Script to convert 2023 Seabird files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024
# Usage (from cruise/original):
#   python convert_cruise_2023.py

import pandas as pd
from common import convertDate, check_output

# -------------------------
# 2023 Cruise Transect Header
# -------------------------
df = pd.read_excel('2023/TRANSECT_HEADER_22-23FINAL.xlsx', dtype='str');
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
df.insert(2,'Year/Month', '2023-01')

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

df.to_csv('../formatted/Cruise_Transect_Header/Cruise_Transect_Header_2023.csv', index=False)
check_output(df, 'Cruise_Transect_Header', '2023')


# -------------------------
# 2023 Cruise Transect Observations
# -------------------------
df = pd.read_excel('2023/TRANSECT_OBS_22-23FINAL.xlsx');
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

df.to_csv('../formatted/Cruise_Transect_Observations/Cruise_Transect_Observations_2023.csv', index=False)
check_output(df, 'Cruise_Transect_Observations', '2023')


# -------------------------
# 2023 Cruise Stationary Header
# -------------------------
df = pd.read_excel('2023/STATIONARY_HEADER_22-23FINAL.xlsx', dtype='str')
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
df.insert(0, 'studyName', 'LMG23-01')
df.insert(1, 'Cruise', '2301')
df.insert(2, 'Year/Month', '2023-01')
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

df.to_csv('../formatted/Cruise_Stationary_Header/Cruise_Stationary_Header_2023.csv', index=False)
check_output(df, 'Cruise_Stationary_Header', '2023')

# -------------------------
# 2023 Cruise Stationary Observations
# -------------------------
df = pd.read_excel('2023/STATIONARY_OBS_22-23FINAL.xlsx')
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
df.insert(0, 'studyName', 'LMG23-01')
df.insert(1, 'Cruise', '2301')
df.to_csv('../formatted/Cruise_Stationary_Observations/Cruise_Stationary_Observations_2023.csv', index=False)
check_output(df, 'Cruise_Stationary_Observations', '2023')
