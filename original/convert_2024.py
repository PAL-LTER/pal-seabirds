# Palmer LTER Seabird
# Script to convert 2024 Seabird files to the archive format
# Written by Sage Lichtenwalner, Rutgers University
# Revised 6/18/2024

import pandas as pd

def convertStudy(n):
  sy = n % 100;
  if sy == 99:
    ey = 0
  else:
    ey = sy+1
  return "PAL%s%s" % (str(sy).zfill(2),str(ey).zfill(2))

# 87 Adelie Penguin Census
df = pd.read_excel('2024/station/Adelie penguin  area-wide breeding population census.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date'})
df.to_csv('out/Adelie_Census_2024.csv', index=False)

# 86 Adelie Penguin Chick Broods
df = pd.read_excel('2024/station/Adelie penguin 1_2 chick nest ratios.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date'})
df.to_csv('out/Adelie_Chick_Broods_2024.csv', index=False)

# 88 Adelie Penguin Chick Counts
df = pd.read_excel('2024/station/Adelie penguin colony-specific chick production.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISLAND': 'Island',
                        'COLONY': 'Colony',
                        'ADULTS': 'Adults',
                        'CHICKS': 'Chicks'})
df.to_csv('out/Adelie_Chick_Production_2024.csv', index=False)

# 89 Adelie Penguin Diet Composition
df = pd.read_excel('2024/station/Adelie penguin diet composition, preliminary analyses of whole lavaged samples.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISLAND': 'Island'})
df.to_csv('out/Adelie_Diet_2024.csv', index=False)

# 97 Adelie Penguin Diet Composition, Fish
# ----- This file has no data for 2024 -----
df = pd.read_excel('2024/station/Adelie diet composition, fish species and numbers.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'SNUM': 'Sample Number',
                        'SOURCE': 'Source',
                        'PREY': 'Prey Type',
                        'SPECIES': 'Species',
                        'EVIDENCE': 'Evidence',
                        'NOTES': 'Notes'})
df.to_csv('out/Adelie_Diet_Fish_2024.csv', index=False)

# 96 Adelie Penguin Diet Composition, Krill
df = pd.read_excel('2024/station/Adelie penguin diet composition, krill size frequency distribution.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName'})
df.to_csv('out/Adelie_Diet_Krill_2024.csv', index=False)

# 94 Adelie Penguin Diet Metadata
df = pd.read_excel('2024/station/Adelie penguin diet metadata.xlsx', dtype={'Bird Weight': 'Int64'});
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISLAND': 'Island',
                        'TIME': 'Time',
                        'SEX': 'Sex'})
df.to_csv('out/Adelie_Diet_Metadata_2024.csv', index=False)

# 91 Adelie Penguin Fledgling Weights
df = pd.read_excel('2024/station/Adelie penguin chick fledging weights.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Location',
                        'WT': 'Weight'})
df.to_csv('out/Adelie_Fledgling_Weights_2024.csv', index=False)

# 92 Adelie Penguin Population Arrival
df = pd.read_excel('2024/station/Adelie penguin population arrival chronology on Humble Island.xlsx', dtype={'Adults': 'Int64'});
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date'})
df.to_csv('out/Adelie_Humble_Population_Arrival_2024.csv', index=False)

# 93 Adelie Penguin Reproductive Success
df = pd.read_excel('2024/station/Adelie penguin reproduction success.xlsx',
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
df.to_csv('out/Adelie_Reproductive_Success_2024.csv', index=False)
