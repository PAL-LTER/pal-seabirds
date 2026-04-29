# Palmer LTER Seabird
# Script to convert 2021 Seabird Cruise files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024

import pandas as pd
from common import convertDate

df = pd.read_csv('2021/Cruise_Transect_Header_2021.csv', dtype='str');

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

df.to_csv('../formatted/Cruise_Transect_Header/Cruise_Transect_Header_2021.csv', index=False)

# -------------------------
df = pd.read_csv('2021/Cruise_Transect_Observations_2021.csv', dtype='str');
df.to_csv('../formatted/Cruise_Transect_Observations/Cruise_Transect_Observations_2021.csv', index=False)

# -------------------------
# 2021 Cruise Stationary — combined file, split into header + obs
df = pd.read_csv('2021/Cruise_Stationary_2021.csv', dtype='str')
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

HEADER_COLS = [
    'studyName', 'Cruise', 'Year/Month', 'Station', 'Event Number',
    'Latitude', 'Longitude', 'YearDay/Hour/Minute',
    'Sea State', 'Salinity', 'Fluorometry', 'Wind Speed', 'Wind Direction',
    'Habitat', 'Ice Cover', 'Ice Type', 'Ice Color', 'Depth', 'DateTime'
]
hdr = df[HEADER_COLS].drop_duplicates(subset=['Cruise', 'Event Number'])
hdr.to_csv('../formatted/Cruise_Stationary_Header/Cruise_Stationary_Header_2021.csv', index=False)

OBS_COLS = [
    'studyName', 'Cruise', 'Event Number',
    'Count Minute', 'Species', 'Number', 'Linkages', 'Behavior', 'Direction', 'Notes'
]
obs = df[OBS_COLS]
obs.to_csv('../formatted/Cruise_Stationary_Observations/Cruise_Stationary_Observations_2021.csv', index=False)

