# Palmer LTER Seabird Scripts
# Generate station_schema.csv from existing formatted files and merge dtype fixes
# Intended as a quick schema refresh before validation/release checks
# Revised 4/22/2026
# Usage (from station/):
#   python generate_schema.py > station_schema.csv

import pandas as pd
import os
import sys

# Dtype fixes from merge_station.py
DTYPE_FIXES = {
    'Adelie_Chick_Broods': {'Nests with Eggs': 'Int64'},
    'Adelie_Chick_Production': {'Adults': 'Int64', 'Chicks': 'Int64', 'Time GMT': 'Int64'},
    'Adelie_Diet': {'Number of Otoliths': 'Int64'},
    'Adelie_Diet_Metadata': {'Bird Weight': 'str'},
    'Adelie_Fledgling_Weights': {'Weight': 'Int64', 'Band Number': 'Int64'},
    'Adelie_Humble_Population_Arrival': {'Adults': 'Int64'},
    'Adelie_Reproductive_Success': {
        'Egg 1 Lay Date': 'Int64',
        'Egg 2 Lay Date': 'Int64',
        'Egg 1 Loss Date': 'Int64',
        'Egg 2 Loss Date': 'Int64',
        'Chick 1 Hatch Date': 'Int64',
        'Chick 2 Hatch Date': 'Int64',
        'Chick 1 Loss Date': 'Int64',
        'Chick 2 Loss Date': 'Int64',
        'Chick 1 Creche Date': 'Int64',
        'Chick 2 Creche Date': 'Int64'
    }
}

# Expected empty (by dataset/year)
EXPECTED_EMPTY = {
    ('Adelie_Chick_Broods', '2022'),
    ('Adelie_Chick_Production', '2022'),
    ('Adelie_Diet', '2022'),
    ('Adelie_Diet_Fish', '2022'),
    ('Adelie_Diet_Fish', '2024'),
}

# Schema header
print('dataset,column,expected_dtype,nullable,notes')

# Inspect all formatted files
for dataset_dir in sorted(os.listdir('formatted')):
    path = os.path.join('formatted', dataset_dir)
    if not os.path.isdir(path):
        continue
    files = sorted([f for f in os.listdir(path) if f.endswith('.csv')])
    if not files:
        continue
    
    # Read first file to get columns
    first_file = os.path.join(path, files[0])
    df = pd.read_csv(first_file)
    
    # Gather stats across all years
    for col in df.columns:
        null_count = 0
        total_rows = 0
        for f in files:
            fpath = os.path.join(path, f)
            year_df = pd.read_csv(fpath)
            if col in year_df.columns:
                null_count += year_df[col].isna().sum()
                total_rows += len(year_df)
        
        null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0
        inferred_type = str(df[col].dtype)
        
        # Check if dtype is overridden in merge script
        if dataset_dir in DTYPE_FIXES and col in DTYPE_FIXES[dataset_dir]:
            expected_dtype = DTYPE_FIXES[dataset_dir][col]
        else:
            expected_dtype = inferred_type
        
        # Determine if nullable
        nullable = null_pct > 0 or col in ['Time GMT', 'Location', 'Culmen Length', 'Culmen Depth']  # known optional fields
        
        notes = ''
        if null_pct > 50:
            notes = 'mostly_null'
        
        print('%s,%s,%s,%s,%s' % (dataset_dir, col, expected_dtype, nullable, notes))
