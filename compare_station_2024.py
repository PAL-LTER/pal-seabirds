# Palmer LTER Seabird Scripts
# This script compares two versions of a dataset
# Revised 8/19/2024

import argparse
import pandas as pd

def compare(x1,x2):
  # Compare the 2 DataFrames and output the results
  x1_str = x1.fillna('').map(lambda x: str(x))
  x2_str = x2.fillna('').map(lambda x: str(x))
  xstr = x1_str + ' != ' + x2_str
  return x2.where(x1_str==x2_str,xstr)

def run_compare(df1, df2, fname):
  # Reshape DataFrames to have the same indexes
  inds = pd.concat([df1,df2]).index.unique().sort_values()
  df1b = df1.reindex(inds, fill_value='')
  df2b = df2.reindex(inds, fill_value='')

  # Run the comparison
  df_compare = compare(df1b,df2b)
  df_compare = df_compare.replace('nan != nan','')

  # Write to CSV
  df_compare.to_csv(('diff_%s.csv' % (fname)), index=False)

# PROCESS EACH DATASET
df1 = pd.read_csv('_edi/D87_AdeliePenguinCensus.csv')
df1 = df1.rename({'Date GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Census_merged.csv')
run_compare(df1, df2, 'Adelie_Census')

df1 = pd.read_csv('_edi/D86_AdeliePenguinBroods.csv')
df1 = df1.rename({'Date GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Chick_Broods_merged.csv')
run_compare(df1, df2, 'Adelie_Chick_Broods')

df1 = pd.read_csv('_edi/D88_AdeliePenguinAdultandChickCounts.csv')
df1 = df1.rename({'Date GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Chick_Production_merged.csv')
run_compare(df1, df2, 'Adelie_Chick_Production')

df1 = pd.read_csv('_edi/D89_AdeliePenguinDiet.csv')
df1['Island'] = ''
df1['Number of Otoliths'] = ''
df1 = df1[['studyName','Sample Number','Date','Sample Weight','E. superba Weight','Number of E. superba','T. macrura Weight','Number of T. macrura','Fish Weight','Number of Fish','Island','Number of Otoliths']]
df2 = pd.read_csv('merged/Adelie_Diet_merged.csv')
print([df1.dtypes,df2.dtypes])
run_compare(df1, df2, 'Adelie_Diet')

df1 = pd.read_csv('_edi/D97_AdeliePenguinDietFish.csv')
df1 = df1.rename({'Datetime GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Diet_Fish_merged.csv')
df1 = df1[['studyName','Sample Number','Date','Source','Prey Type','Species','Evidence','Number of Fish','Evidence Size','Evidence Weight','Estimated Fish Length','Estimated Fish Weight','Notes'
]]
run_compare(df1, df2, 'Adelie_Diet_Fish')

df1 = pd.read_csv('_edi/D96_AdeliePenguinDietEuphausiasuberba.csv')
df1 = df1.rename({'Date GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Diet_Krill_merged.csv')
df1 = df1[['studyName','Sample Number','Sample Collection Date','Total Number','16-20','21-25','26-30','31-35','36-40','41-45','46-50','51-55','56-60','61-65']]
print(df1.dtypes)
print(df2.dtypes)
run_compare(df1, df2, 'Adelie_Diet_Krill')

df1 = pd.read_csv('_edi/D94_AdeliePenguinDietLog.csv')
df1 = df1.rename({'Colony':'Location'},axis=1)
df2 = pd.read_csv('merged/Adelie_Diet_Metadata_merged.csv')
run_compare(df1, df2, 'Adelie_Diet_Metadata')

df1 = pd.read_csv('_edi/D91_AdeliePenguinFledglingWeights.csv')
df1 = df1.rename({'Date GMT':'Date','Colony':'Location'},axis=1)
df2 = pd.read_csv('merged/Adelie_Fledgling_Weights_merged.csv')
run_compare(df1, df2, 'Adelie_Fledgling_Weights')

df1 = pd.read_csv('_edi/D92_AdeliePenguinPopulationonHumbleIsland.csv')
df1 = df1.rename({'Date GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Humble_Population_Arrival_merged.csv')
run_compare(df1, df2, 'Adelie_Humble_Population_Arrival')

df1 = pd.read_csv('_edi/D93_AdeliePenguinReproductionSuccess.csv')
df1 = df1.rename({'Date GMT':'Date'},axis=1)
df2 = pd.read_csv('merged/Adelie_Reproductive_Success_merged.csv')
run_compare(df1, df2, 'Adelie_Reproductive_Success')
  
# The revised 'Adelie_Diet_Other' dataset only goes up to 2020.  So the only difference from the previous version is adding the last 2 years.
  

  

# # Main function for command line mode
# if __name__ == '__main__':
#   # Command Line Arguments
#   parser = argparse.ArgumentParser(description='PAL Seabird data file comparison')
#   parser.add_argument('-o','--old', type=str,
#     required = True,
#     help='Original data filename or URL')
#   parser.add_argument('-n','--new', type=str,
#     required = True,
#     help='New data filename or URL')
#   parser.add_argument('-f','--filename', type=str,
#     default = 'diff',
#     help='Ouput filename')
#   args = parser.parse_args()
#   main(args.old,args.new,args.filename)

# compare.py -n 'merged/Adelie_Census_merged.csv' -o '_edi/D87_AdeliePenguinCensus.csv' -f 'diff_Adelie_Census'
