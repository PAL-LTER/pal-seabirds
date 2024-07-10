# Palmer LTER Seabird Scripts
# Script to combine Cruise data files for archiving
# Written by Sage Lichtenwalner, Rutgers University
# Revised 7/9/2024

import argparse
import pandas as pd

# Primary function
def main():
  print('Processing dataset: %s' % args.dataset)
  years = ['1993_2020','2021','2023','2024']
  files = ['formatted/%s/%s_%s.csv' % (args.dataset, args.dataset, year) for year in years]
  dtypes = dtype_fixes(args.dataset)
  df = pd.concat( [pd.read_csv(f, dtype=dtypes) for f in files], ignore_index=True)
  
  # Move notes to end
  if args.dataset =='Cruise_Transect_Header':
    df.insert(len(df.columns)-1, 'Notes', df.pop('Notes'))
  
  # Write to CSV
  df.to_csv(('merged/%s_%s.csv' % (args.dataset, args.suffix)), index=False)
  
  # Output file sizes for verification
  print('Output size: {} {}'.format(df.shape[0], df.shape[1]))
  for f in files:
    df = pd.read_csv(f);
    print('%s %s' % (f,df.shape))


def dtype_fixes(dataset):
    return {}


# Main function for command line mode
if __name__ == '__main__':
  # Command Line Arguments
  parser = argparse.ArgumentParser(description='PAL Seabird Cruise data concatenation script')
  parser.add_argument('-d','--dataset', type=str,
    required = True,
    help='Dataset Name')
  parser.add_argument('-s','--suffix', type=str,
    default = 'merged',
    help='Ouput file suffix')
  args = parser.parse_args()
  main()
