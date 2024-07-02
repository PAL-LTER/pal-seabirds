# Palmer LTER Seabird
# Script to convert Fraser data files to the archive format
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

# 87 Adelie Census
df = pd.read_excel('2020_Fraser/ADPE CENSUS.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                   'DATE': 'Date',
                   'ISL': 'Island',
                   'LOC': 'Colony',
                   'NESTS': 'Breeding Pairs'})
df = df.sort_values(by=['Date', 'Island', 'Colony'])
df.to_csv('out/Adelie_Census_1992_2020.csv', index=False)

# 86 Adelie Chick Broods
df = pd.read_excel('2020_Fraser/BROODS.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Colony',
                        'SAMPLETERR': 'Nests in Sample',
                        'ONE_CHICK':'Nests with One Chick',
                        'TWO_CHICK':'Nests with Two Chicks',
                        'EGGNESTS': 'Nests with Eggs'})
df = df.sort_values(by=['Date', 'Island', 'Colony'])
df.to_csv('out/Adelie_Chick_Broods_1992_2020.csv', index=False)

# 88 Adelie Chick Counts
df = pd.read_excel('2020_Fraser/CKCNTS.xls',  dtype={'ADULTS': 'Int64', 'CHICKS': 'Int64'});
df['SEASON'] = df['SEASON'].map(convertStudy)
df['TIME'] = df['TIME'].astype('Int64').astype(str).replace('<NA>','')
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'TIME': 'Time GMT',
                        'ISL': 'Island',
                        'LOC': 'Colony',
                        'ADULTS': 'Adults',
                        'CHICKS': 'Chicks'})
df = df.sort_values(by=['Date', 'Island', 'Colony'])
df = df[['studyName','Date','Time GMT','Island','Colony','Adults','Chicks']] # Sort columns
df.to_csv('out/Adelie_Chick_Production_1992_2020.csv', index=False)

# 89 Adelie Penguin Diet Composition
df = pd.read_excel('2020_Fraser/DIET.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'SNUM': 'Sample Number',
                        'FRESHWT': 'Sample Weight',
                        'EUSUWT': 'E. superba Weight',
                        'EUSUNO': 'Number of E. superba',
                        'THMAWT': 'T. macrura Weight',
                        'THMANO': 'Number of T. macrura',
                        'FISHWT': 'Fish Weight',
                        'FISHNO': 'Number of Fish'})
df.to_csv('out/Adelie_Diet_1992_2020.csv', index=False)

# # 97 Adelie Penguin Diet Composition, Fish
df = pd.read_excel('2020_Fraser/FISH.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'SNUM': 'Sample Number',
                        'SOURCE': 'Source',
                        'PREY': 'Prey Type',
                        'SPECIES': 'Species',
                        'EVIDENCE': 'Evidence',
                        'NO': 'Number of Fish',
                        'SIZE': 'Evidence Size',
                        'TRUEWT': 'Evidence Weight',
                        'ESTLENGTH': 'Estimated Fish Length',
                        'ESTWEIGHT': 'Estimated Fish Weight',
                        'NOTES': 'Notes'})
df.to_csv('out/Adelie_Diet_Fish_1992_2020.csv', index=False)

# 96 Adelie Penguin Diet Composition, Krill
df = pd.read_excel('2020_Fraser/KRILL.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'SNUM': 'Sample Number',
                        'DATE': 'Sample Collection Date',
                        'TOTALNO': 'Total Number',
                        'L16_20': '16-20',
                        'L21_25': '21-25',
                        'L26_30': '26-30',
                        'L31_35': '31-35',
                        'L36_40': '36-40',
                        'L41_45': '41-45',
                        'L46_50': '46-50',
                        'L51_55': '51-55',
                        'L56_60': '56-60	',
                        'L61_65': '61-65'})
df.to_csv('out/Adelie_Diet_Krill_1992_2020.csv', index=False)

# 94 Adelie Penguin Diet Metadata
df = pd.read_excel('2020_Fraser/HEADER.xls', dtype={'Bird Weight': 'Int64'} );
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Location',
                        'TIME': 'Time',
                        'SNUM': 'Sample Number',
                        'BIRDWT': 'Bird Weight',
                        'SEX': 'Sex',
                        'CULMENL': 'Culmen Length',
                        'CULMEND': 'Culmen Depth'})
df.to_csv('out/Adelie_Diet_Metadata_1992_2020.csv', index=False)

# 91 Adelie Penguin Fledgling Weights
df = pd.read_excel('2020_Fraser/FLWTS.xls', dtype={'BANDNO': 'Int64', 'WT': 'Int64'});
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Location',
                        'BANDNO': 'Band Number',
                        'WT': 'Weight'})
df.to_csv('out/Adelie_Fledgling_Weights_1992_2020.csv', index=False)

# 92 Adelie Penguin Population Arrival
df = pd.read_excel('2020_Fraser/HUMPOP.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'DATE': 'Date',
                        'ISL': 'Island',
                        'LOC': 'Colony',
                        'TOTADULTS': 'Adults'})
df.to_csv('out/Adelie_Humble_Population_Arrival_1992_2020.csv', index=False)

# 93 Adelie Penguin Reproductive Success
df = pd.read_excel('2020_Fraser/REPRO.xls', dtype={'C1LOS': 'Int64'});
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'ISL': 'Island',
                        'LOC': 'Colony',
                        'SITE': 'Site Number',
                        'NEST': 'Nest Number',
                        'E1LAY': 'Egg 1 Lay Date',
                        'E2LAY': 'Egg 2 Lay Date',
                        'E1LOS': 'Egg 1 Loss Date',
                        'E2LOS': 'Egg 2 Loss Date',
                        'C1HAT': 'Chick 1 Hatch Date',
                        'C2HAT': 'Chick 2 Hatch Date',
                        'C1LOS': 'Chick 1 Loss Date',
                        'C2LOS': 'Chick 2 Loss Date',
                        'C1CRE': 'Chick 1 Creche Date',
                        'C2CRE'	: 'Chick 2 Creche Date',
                        'NOTES': 'Notes'})
df.to_csv('out/Adelie_Reproductive_Success_1992_2020.csv', index=False)

# ----- The following dataset only goes to 2020 -----
# 98 Adelie Penguin Diet Composition, Other Prey
df = pd.read_excel('2020_Fraser/PREY.xls');
df['SEASON'] = df['SEASON'].map(convertStudy)
df = df.rename(columns={'SEASON': 'studyName',
                        'SNUM': 'Sample Number',
                        'DATE': 'Date',
                        'SOURCE': 'Source',
                        'PREY': 'Prey Type',
                        'SPECIES': 'Species',
                        'EVIDENCE': 'Evidence',
                        'NO': 'Prey Number',
                        'SIZE': 'Evidence Size',
                        'TRUEWT': 'Evidence Weight',
                        'ESTLENGTH': 'Estimated Prey Length',
                        'ESTWEIGHT': 'Estimated Prey Weight'})
df.to_csv('out/Adelie_Diet_Other_1992_2020.csv', index=False)
