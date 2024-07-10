# Palmer LTER Seabird Scripts
# Script to combine Station data files for archiving
# Written by Sage Lichtenwalner, Rutgers University
# Revised 7/9/2024

import argparse
import pandas as pd

# Primary function
def main():
  print('Processing dataset: %s' % args.dataset)
  years = ['1992_2020','2021','2022','2023','2024']
  files = ['formatted/%s/%s_%s.csv' % (args.dataset, args.dataset, year) for year in years]
  dtypes = dtype_fixes(args.dataset)
  df = pd.concat( [pd.read_csv(f, dtype=dtypes) for f in files], ignore_index=True)
  
  # Write to CSV
  df.to_csv(('merged/%s_%s.csv' % (args.dataset, args.suffix)), index=False)
  
  # Output file sizes for verification
  print('Output size: {} {}'.format(df.shape[0], df.shape[1]))
  for f in files:
    df = pd.read_csv(f);
    print('%s %s' % (f,df.shape))


def dtype_fixes(dataset):
  if dataset == "Adelie_Chick_Broods":
      return {'Nests with Eggs': 'Int64'}
  elif dataset == "Adelie_Chick_Production":
      return {'Adults': 'Int64', 'Chicks': 'Int64', 'Time GMT': 'Int64'}
  elif dataset == "Adelie_Diet":
      return {'Number of Otoliths': 'Int64'}
  elif dataset == "Adelie_Diet_Metadata":
      return {'Bird Weight': 'str'}
  elif dataset == "Adelie_Fledgling_Weights":
      return {'Weight': 'Int64', 'Band Number': 'Int64'}
  elif dataset == "Adelie_Humble_Population_Arrival":
      return {'Adults': 'Int64'}
  elif dataset == "Adelie_Reproductive_Success":
      return {'Egg 1 Lay Date': 'Int64',
      'Egg 2 Lay Date': 'Int64',
      'Egg 1 Loss Date': 'Int64',
      'Egg 2 Loss Date': 'Int64',
      'Chick 1 Hatch Date': 'Int64',
      'Chick 2 Hatch Date': 'Int64',
      'Chick 1 Loss Date': 'Int64',
      'Chick 2 Loss Date': 'Int64',
      'Chick 1 Creche Date': 'Int64',
      'Chick 2 Creche Date': 'Int64'}
  else:
    return {}


# Main function for command line mode
if __name__ == '__main__':
  # Command Line Arguments
  parser = argparse.ArgumentParser(description='PAL Seabird Station data concatenation script')
  parser.add_argument('-d','--dataset', type=str,
    required = True,
    help='Dataset Name')
  parser.add_argument('-s','--suffix', type=str,
    default = 'merged',
    help='Ouput file suffix')
  args = parser.parse_args()
  main()
