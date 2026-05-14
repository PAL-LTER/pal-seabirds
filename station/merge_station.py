# Palmer LTER Seabird Scripts
# Script to combine Station data files for archiving
# Written by Sage Lichtenwalner, Rutgers University
# Revised 4/22/2026
# Added 'all' option 8/19/2024
# Updated for station/ structure and concise merge logging 4/22/2026

import argparse
import os
import pandas as pd

# Primary function
def main():
  if (args.dataset)=='all':
    for d in ['Adelie_Census',
              'Adelie_Chick_Broods',
              'Adelie_Chick_Production',
              'Adelie_Diet',
              'Adelie_Diet_Fish',
              'Adelie_Diet_Krill',
              'Adelie_Diet_Metadata',
              # 'Adelie_Diet_Other',
              'Adelie_Fledgling_Weights',
              'Adelie_Humble_Population_Arrival',
              'Adelie_Reproductive_Success']:
      process_dataset(d)
  else:
    process_dataset(args.dataset)

def process_dataset(dataset):
  print('Processing dataset: %s' % dataset)
  years = ['1992_2020','2021','2022','2023','2024','2025','2026']
  files = ['formatted/%s/%s_%s.csv' % (dataset, dataset, year) for year in years]
  output_dir = 'merged'
  os.makedirs(output_dir, exist_ok=True)

  missing_files = [f for f in files if not os.path.exists(f)]
  if missing_files:
    raise FileNotFoundError(
      'Missing input file(s) for %s:\n%s' % (dataset, '\n'.join(missing_files))
    )

  dtypes = dtype_fixes(dataset)
  frames = []
  input_rows = []
  for f in files:
    input_df = pd.read_csv(f, dtype=dtypes)
    frames.append(input_df)
    input_rows.append((f, input_df.shape[0]))

  df = pd.concat(frames, ignore_index=True)
  
  # Write to CSV
  output_path = '%s/%s_%s.csv' % (output_dir, dataset, args.suffix)
  df.to_csv(output_path, index=False)
  
  # Concise run logging for verification
  total_input_rows = sum(r for _, r in input_rows)
  print('Inputs used:')
  for f, row_count in input_rows:
    print('  %s: %s rows' % (f, row_count))
  print('Output: %s (%s rows, %s columns)' % (output_path, df.shape[0], df.shape[1]))
  if df.shape[0] != total_input_rows:
    print('  WARNING: output row count (%s) does not match sum of inputs (%s)' % (df.shape[0], total_input_rows))


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
