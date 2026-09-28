# Palmer LTER Seabird Scripts
# Script to convert 2026 Seabird files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 5/14/2026
# Usage (from station/original):
#   python convert_station_2026.py

import pandas as pd
from common import standardize_time, convertStudy, check_output

# 87 Adelie Penguin Census
df = pd.read_excel('2026/Adelie penguin  area-wide breeding population census.xlsx');
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName'})
df.to_csv('../formatted/Adelie_Census/Adelie_Census_2026.csv', index=False)
check_output(df, 'Adelie_Census', '2026')

# 86 Adelie Penguin Chick Broods
df = pd.read_excel('2026/Adelie penguin 1_2 chick nest ratios.xlsx');
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName'})
df.to_csv('../formatted/Adelie_Chick_Broods/Adelie_Chick_Broods_2026.csv', index=False)
check_output(df, 'Adelie_Chick_Broods', '2026')

# 88 Adelie Penguin Chick Counts
df = pd.read_excel('2026/Adelie penguin colony-specific chick production.xlsx');
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName'})
df.to_csv('../formatted/Adelie_Chick_Production/Adelie_Chick_Production_2026.csv', index=False)
check_output(df, 'Adelie_Chick_Production', '2026')

# 89 Adelie Penguin Diet Composition
df = pd.read_excel('2026/Adelie penguin diet composition, preliminary analyses of whole lavaged samples.xlsx');
df['Number of T. macrura'] = df['Number of T. macrura'].fillna('Missing')
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName'})
df.to_csv('../formatted/Adelie_Diet/Adelie_Diet_2026.csv', index=False)
check_output(df, 'Adelie_Diet', '2026')

# 97 Adelie Penguin Diet Composition, Fish
df = pd.read_excel('2026/Adelie diet composition, fish species and numbers.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'SNUM': 'Sample Number',
                        'SOURCE': 'Source',
                        'PREY': 'Prey Type',
                        'SPECIES': 'Species',
                        'EVIDENCE': 'Evidence',
                        'NOTES': 'Notes'})
df.to_csv('../formatted/Adelie_Diet_Fish/Adelie_Diet_Fish_2026.csv', index=False)
check_output(df, 'Adelie_Diet_Fish', '2026', empty_ok=True)

# 96 Adelie Penguin Diet Composition, Krill
df = pd.read_excel('2026/Adelie penguin diet composition, krill size frequency distribution.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName'})
df.to_csv('../formatted/Adelie_Diet_Krill/Adelie_Diet_Krill_2026.csv', index=False)
check_output(df, 'Adelie_Diet_Krill', '2026')

# 94 Adelie Penguin Diet Metadata
df = pd.read_excel('2026/Adelie penguin diet metadata.xlsx', dtype={'Bird Weight': 'Int64'});
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName'})
df['Time'] = df['Time'].apply(standardize_time)
df['Location'] = 'BCH'
df.to_csv('../formatted/Adelie_Diet_Metadata/Adelie_Diet_Metadata_2026.csv', index=False)
check_output(df, 'Adelie_Diet_Metadata', '2026')

# 91 Adelie Penguin Fledgling Weights
df = pd.read_excel('2026/Adelie penguin chick fledging weights.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Location',
                        'WT': 'Weight'})
df.to_csv('../formatted/Adelie_Fledgling_Weights/Adelie_Fledgling_Weights_2026.csv', index=False)
check_output(df, 'Adelie_Fledgling_Weights', '2026')

# 92 Adelie Penguin Population Arrival
df = pd.read_excel('2026/Adelie penguin population arrival chronology on Humble Island.xlsx', dtype={'Adults': 'Int64'});
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName'})
df.to_csv('../formatted/Adelie_Humble_Population_Arrival/Adelie_Humble_Population_Arrival_2026.csv', index=False)
check_output(df, 'Adelie_Humble_Population_Arrival', '2026')

# 93 Adelie Penguin Reproductive Success
df = pd.read_excel('2026/Adelie penguin reproduction success.xlsx',
    dtype={'Egg 1 Lay Date': 'Int64',
      'Egg 2 Lay Date': 'Int64',
      'Egg 1 Loss Date': 'Int64',
      'Egg 2 Loss Date': 'Int64',
      'Chick 1 Hatch Date': 'Int64',
      'Chick 2 Hatch Date': 'Int64',
      'Chick 1 Loss Date': 'Int64',
      'Chick 2 Loss Date': 'Int64',
      'Chick 1 Creche Date': 'Int64',
      'Chick 2 Creche Date': 'Int64'});
df['Season'] = df['Season'].map(convertStudy)
df = df.rename(columns={'Season': 'studyName',
                        'NOTES': 'Notes'})
df.to_csv('../formatted/Adelie_Reproductive_Success/Adelie_Reproductive_Success_2026.csv', index=False)
check_output(df, 'Adelie_Reproductive_Success', '2026')
