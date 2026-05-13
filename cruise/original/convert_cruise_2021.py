# Palmer LTER Seabird Scripts
# Script to convert 2021 Seabird Cruise files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024
# Usage (from cruise/original):
#   python convert_cruise_2021.py

import pandas as pd
from common import convertDate, check_output, parseYearMonth


def fixYM(ym, ev):
    # 2111 - After and including event 170, change YM to 2112.
    try:
        ev_num = int(float(ev))
    except Exception:
        ev_num = None
    ym_text = str(ym).strip()
    if ym_text == '2111' and ev_num is not None and ev_num >= 170:
        return '2112'
    return ym_text

# -------------------------
# 2021 Cruise Transect Header
# -------------------------

df = pd.read_csv('2021/Cruise_Transect_Header_2021.csv', dtype='str');
df['Year/Month'] = df.apply(lambda row: fixYM(row['Year/Month'], row['Event Number']), axis=1)
df['Year/Month'] = df['Year/Month'].apply(lambda v: f"{parseYearMonth(v)[0]:04d}-{parseYearMonth(v)[1]:02d}")

# Recalculate date
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
df['YearDay/Hour/Minute'] = df['YearDay/Hour/Minute'].astype(str)

df.to_csv('../formatted/Cruise_Transect_Header/Cruise_Transect_Header_2021.csv', index=False)
check_output(df, 'Cruise_Transect_Header', '2021')

# -------------------------
# 2021 Cruise Transect Observations
# -------------------------

df = pd.read_csv('2021/Cruise_Transect_Observations_2021.csv', dtype='str');
df.to_csv('../formatted/Cruise_Transect_Observations/Cruise_Transect_Observations_2021.csv', index=False)
check_output(df, 'Cruise_Transect_Observations', '2021')

# -------------------------
# 2021 Cruise Stationary — combined file, split into header + obs
# -------------------------
df = pd.read_csv('2021/Cruise_Stationary_2021.csv', dtype='str')
df['Year/Month'] = df.apply(lambda row: fixYM(row['Year/Month'], row['Event Number']), axis=1)
df['Year/Month'] = df['Year/Month'].apply(lambda v: f"{parseYearMonth(v)[0]:04d}-{parseYearMonth(v)[1]:02d}")
df['DateTime'] = df.apply(lambda row: convertDate(row['Year/Month'], row['YearDay/Hour/Minute']), axis=1)

HEADER_COLS = [
    'studyName', 'Cruise', 'Year/Month', 'Station', 'Event Number',
    'Latitude', 'Longitude', 'YearDay/Hour/Minute',
    'Sea State', 'Salinity', 'Fluorometry', 'Wind Speed', 'Wind Direction',
    'Habitat', 'Ice Cover', 'Ice Type', 'Ice Color', 'Depth', 'DateTime'
]
hdr = df[HEADER_COLS].drop_duplicates(subset=['Cruise', 'Event Number'])

# Convert YearDay/Hour/Minute to string to preserve as-is in CSV (prevent .0 artifacts)
hdr['YearDay/Hour/Minute'] = hdr['YearDay/Hour/Minute'].astype(str)

hdr.to_csv('../formatted/Cruise_Stationary_Header/Cruise_Stationary_Header_2021.csv', index=False)
check_output(hdr, 'Cruise_Stationary_Header', '2021')

OBS_COLS = [
    'studyName', 'Cruise', 'Event Number',
    'Count Minute', 'Species', 'Number', 'Linkages', 'Behavior', 'Direction', 'Notes'
]
obs = df[OBS_COLS]
obs.to_csv('../formatted/Cruise_Stationary_Observations/Cruise_Stationary_Observations_2021.csv', index=False)
check_output(obs, 'Cruise_Stationary_Observations', '2021')

