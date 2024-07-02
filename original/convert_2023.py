# Palmer LTER Seabird
# Script to convert 2023 Seabird files to the archive format
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
df = pd.read_excel('2023/Palmer/Adelie penguin  area-wide breeding population census.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date'})
df.to_csv('out/Adelie_Census_2023.csv', index=False)

# 86 Adelie Penguin Chick Broods
df = pd.read_excel('2023/Palmer/Adelie penguin 1:2 chick nest ratios.xlsx', dtype={'Nests with Eggs': 'Int64'});
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date'})
df.to_csv('out/Adelie_Chick_Broods_2023.csv', index=False)

# 88 Adelie Penguin Chick Counts
df = pd.read_excel('2023/Palmer/Adelie penguin colony-specific chick production.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISLAND': 'Island',
                        'COLONY': 'Colony',
                        'ADULTS': 'Adults',
                        'CHICKS': 'Chicks'})
df.to_csv('out/Adelie_Chick_Production_2023.csv', index=False)

# 89 Adelie Penguin Diet Composition
df = pd.read_excel('2023/Palmer/Adelie penguin diet composition, preliminary analyses of whole lavaged samples.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISLAND': 'Island'})
df.to_csv('out/Adelie_Diet_2023.csv', index=False)

# 97 Adelie Penguin Diet Composition, Fish
df = pd.read_excel('2023/Palmer/Adelie diet composition, fish species and numbers.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'SNUM': 'Sample Number',
                        'SOURCE': 'Source',
                        'PREY': 'Prey Type',
                        'SPECIES': 'Species',
                        'EVIDENCE': 'Evidence',
                        'NOTES': 'Notes'})
df.to_csv('out/Adelie_Diet_Fish_2023.csv', index=False)

# 96 Adelie Penguin Diet Composition, Krill
df = pd.read_excel('2023/Palmer/Adelie penguin diet composition, krill size frequency distribution.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName'})
df.to_csv('out/Adelie_Diet_Krill_2023.csv', index=False)

# 94 Adelie Penguin Diet Metadata
df = pd.read_excel('2023/Palmer/Adelie penguin diet metadata.xlsx', dtype={'Bird Weight': 'Int64'} );
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISLAND': 'Island',
                        'TIME': 'Time',
                        'SEX': 'Sex'})
df.to_csv('out/Adelie_Diet_Metadata_2023.csv', index=False)

# 91 Adelie Penguin Fledgling Weights
df = pd.read_excel('2023/Palmer/Adelie penguin chick fledging weights.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Location',
                        'WT': 'Weight'})
df.to_csv('out/Adelie_Fledgling_Weights_2023.csv', index=False)

# 92 Adelie Penguin Population Arrival
df = pd.read_excel('2023/Palmer/Adelie penguin population arrival chronology on Humble Island.xlsx');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date'})
df.to_csv('out/Adelie_Humble_Population_Arrival_2023.csv', index=False)

# 93 Adelie Penguin Reproductive Success
df = pd.read_excel('2023/Palmer/Adelie penguin reproduction success.xlsx',
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
df.to_csv('out/Adelie_Reproductive_Success_2023.csv', index=False)
