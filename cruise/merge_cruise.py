# Palmer LTER Seabird Scripts
# Script to combine Cruise data files for archiving
# Written by Sage Lichtenwalner, Rutgers University
# Revised 4/29/2026
# Usage (from cruise/):
#   python merge_cruise.py -d all

import argparse
import os
import pandas as pd

# Primary function
def main():
  if args.dataset == 'all':
    for d in ['Cruise_Transect_Header',
              'Cruise_Transect_Observations',
              'Cruise_Stationary_Header',
              'Cruise_Stationary_Observations']:
      process_dataset(d)
  else:
    process_dataset(args.dataset)

def process_dataset(dataset):
  print('Processing dataset: %s' % dataset)
  years = ['1993_2020','2021','2023','2024','2026']
  files = ['formatted/%s/%s_%s.csv' % (dataset, dataset, year) for year in years]
  output_dir = 'merged'
  os.makedirs(output_dir, exist_ok=True)

  missing_files = [f for f in files if not os.path.exists(f)]
  if missing_files:
    raise FileNotFoundError(
      'Missing input file(s) for %s:\n%s' % (dataset, '\n'.join(missing_files))
    )

  frames = []
  input_rows = []
  for f in files:
    # Read all columns as strings to preserve source formatting (e.g., no .0 coercion).
    input_df = pd.read_csv(f, dtype='str')
    frames.append(input_df)
    input_rows.append((f, input_df.shape[0]))

  df = pd.concat(frames, ignore_index=True)

  # Drop QC-only columns by default for release-facing merged outputs.
  if not args.include_qc_columns:
    df = drop_qc_columns(df)

  # Reorder columns: DateTime after Event Number, Notes last
  df = reorder_columns(df, dataset)

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


def reorder_columns(df, dataset):
  cols = df.columns.tolist()
  if dataset in ('Cruise_Transect_Header', 'Cruise_Stationary_Header'):
    # Move DateTime to immediately after Event Number
    cols.remove('DateTime')
    cols.insert(cols.index('Event Number') + 1, 'DateTime')
  # Move Notes to last for all datasets
  cols.remove('Notes')
  cols.append('Notes')
  return df[cols]


def drop_qc_columns(df):
  qc_cols = [
    'OLD Latitude Start',
    'OLD Longitude Start',
    'OLD Latitude End',
    'OLD Longitude End',
    'OLD YearDay/Hour/Minute',
  ]
  drop_cols = [c for c in qc_cols if c in df.columns]
  if drop_cols:
    return df.drop(columns=drop_cols)
  return df


# Main function for command line mode
if __name__ == '__main__':
  # Command Line Arguments
  parser = argparse.ArgumentParser(description='PAL Seabird Cruise data concatenation script')
  parser.add_argument('-d','--dataset', type=str,
    required = True,
    help='Dataset Name')
  parser.add_argument('-s','--suffix', type=str,
    default = 'merged',
    help='Output file suffix')
  parser.add_argument('--include-qc-columns', action='store_true',
    help='Include QC-only columns (e.g., OLD coordinate fields) in merged outputs')
  args = parser.parse_args()
  main()
