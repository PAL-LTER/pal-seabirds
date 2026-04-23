# Palmer LTER Seabird Scripts
# Validate formatted and merged station files against station_schema.csv
# Revised 4/22/2026
# Usage (from station/):
#   python validate_station.py --all-formatted
#   python validate_station.py --formatted formatted/Adelie_Census
#   python validate_station.py --merged

import argparse
import pandas as pd
import os
import sys

# Known/accepted schema differences. These are warnings, not failures.
ALLOWED_MISSING_COLUMNS = {
    'Adelie_Chick_Production': {'Time GMT'},
    'Adelie_Diet_Fish': {'Evidence Size'},
}

ALLOWED_EXTRA_COLUMNS = {
    'Adelie_Diet': {'Island', 'Number of Otoliths'},
}

def load_schema(schema_path='station_schema.csv'):
    """Load schema from CSV file."""
    schema = pd.read_csv(schema_path)
    # Group by dataset
    by_dataset = {}
    for _, row in schema.iterrows():
        dataset = row['dataset']
        if dataset not in by_dataset:
            by_dataset[dataset] = []
        by_dataset[dataset].append({
            'column': row['column'],
            'expected_dtype': row['expected_dtype'],
            'nullable': row['nullable'] == 'True' or row['nullable'] == True,
            'notes': row['notes'] if pd.notna(row['notes']) else ''
        })
    return by_dataset

def validate_file(filepath, dataset_name, schema_by_dataset):
    """Validate a single file against the schema."""
    df = pd.read_csv(filepath)
    schema = schema_by_dataset.get(dataset_name, [])
    
    if not schema:
        print(f"  WARNING: No schema found for {dataset_name}")
        return True
    
    all_ok = True
    expected_cols = set(col['column'] for col in schema)
    actual_cols = set(df.columns)
    
    # Check for missing columns
    missing = expected_cols - actual_cols
    allowed_missing = ALLOWED_MISSING_COLUMNS.get(dataset_name, set())
    expected_missing = missing & allowed_missing
    unexpected_missing = missing - allowed_missing
    if expected_missing:
        print(f"  WARNING: Allowed missing columns: {sorted(expected_missing)}")
    if unexpected_missing:
        print(f"  ERROR: Missing columns: {sorted(unexpected_missing)}")
        all_ok = False
    
    # Check for extra columns
    extra = actual_cols - expected_cols
    allowed_extra = ALLOWED_EXTRA_COLUMNS.get(dataset_name, set())
    expected_extra = extra & allowed_extra
    unexpected_extra = extra - allowed_extra
    if expected_extra:
        print(f"  WARNING: Allowed extra columns: {sorted(expected_extra)}")
    if unexpected_extra:
        print(f"  ERROR: Extra columns: {sorted(unexpected_extra)}")
        all_ok = False
    
    # Check nullability
    for col_schema in schema:
        col = col_schema['column']
        if col not in actual_cols:
            continue
        
        null_count = df[col].isna().sum()
        if null_count > 0 and not col_schema['nullable']:
            print(f"  ERROR: Non-nullable column '{col}' has {null_count} null(s)")
            all_ok = False
    
    return all_ok

def validate_formatted(formatted_dir, schema_by_dataset):
    """Validate all formatted files in a dataset directory."""
    results = {}
    dataset_name = os.path.basename(formatted_dir)
    
    print(f"Validating {dataset_name}...")
    files = sorted([f for f in os.listdir(formatted_dir) if f.endswith('.csv')])
    
    if not files:
        print(f"  SKIP: No CSV files found")
        return results
    
    for filename in files:
        filepath = os.path.join(formatted_dir, filename)
        ok = validate_file(filepath, dataset_name, schema_by_dataset)
        results[filename] = 'OK' if ok else 'FAIL'
        status = '✓' if ok else '✗'
        print(f"  {status} {filename}")
    
    return results

def validate_merged(merged_dir, schema_by_dataset):
    """Validate all merged files in a directory."""
    results = {}
    
    print(f"Validating merged files...")
    files = sorted([f for f in os.listdir(merged_dir) if f.endswith('.csv')])
    
    if not files:
        print(f"  SKIP: No CSV files found")
        return results
    
    for filename in files:
        # Extract dataset name from filename (e.g., Adelie_Census_1991_2024.csv -> Adelie_Census)
        parts = filename.replace('.csv', '').split('_')
        # Handle multi-word datasets
        if 'Diet' in filename:
            if 'Fish' in filename:
                dataset_name = 'Adelie_Diet_Fish'
            elif 'Krill' in filename:
                dataset_name = 'Adelie_Diet_Krill'
            elif 'Metadata' in filename:
                dataset_name = 'Adelie_Diet_Metadata'
            else:
                dataset_name = 'Adelie_Diet'
        elif 'Fledgling' in filename:
            dataset_name = 'Adelie_Fledgling_Weights'
        elif 'Humble' in filename:
            dataset_name = 'Adelie_Humble_Population_Arrival'
        elif 'Reproductive' in filename:
            dataset_name = 'Adelie_Reproductive_Success'
        elif 'Chick' in filename:
            if 'Broods' in filename:
                dataset_name = 'Adelie_Chick_Broods'
            else:
                dataset_name = 'Adelie_Chick_Production'
        elif 'Census' in filename:
            dataset_name = 'Adelie_Census'
        else:
            dataset_name = '_'.join(parts[:-2])  # Strip off year range
        
        filepath = os.path.join(merged_dir, filename)
        ok = validate_file(filepath, dataset_name, schema_by_dataset)
        results[filename] = 'OK' if ok else 'FAIL'
        status = '✓' if ok else '✗'
        print(f"  {status} {filename} ({dataset_name})")
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate station files against station_schema.csv')
    parser.add_argument('--formatted', type=str, 
        help='Validate a single formatted dataset directory (e.g., formatted/Adelie_Census)')
    parser.add_argument('--all-formatted', action='store_true',
        help='Validate all formatted dataset directories')
    parser.add_argument('--merged', nargs='?', const='merged', type=str,
        help='Validate merged files (default directory: merged)')
    parser.add_argument('--schema', type=str, default='station_schema.csv',
        help='Path to station_schema.csv (default: station_schema.csv)')
    args = parser.parse_args()
    
    if not args.formatted and not args.all_formatted and not args.merged:
        parser.print_help()
        sys.exit(1)
    
    schema = load_schema(args.schema)
    
    if args.all_formatted:
        if not os.path.isdir('formatted'):
            print('ERROR: formatted/ directory not found')
            sys.exit(1)
        all_results = {}
        for dataset_dir in sorted(os.listdir('formatted')):
            path = os.path.join('formatted', dataset_dir)
            if os.path.isdir(path):
                results = validate_formatted(path, schema)
                all_results.update(results)
        print()
        passed = sum(1 for v in all_results.values() if v == 'OK')
        total = len(all_results)
        print(f"All formatted: {passed}/{total} passed")
    elif args.formatted:
        results = validate_formatted(args.formatted, schema)
        print()
        passed = sum(1 for v in results.values() if v == 'OK')
        total = len(results)
        print(f"Formatted: {passed}/{total} passed")
    
    if args.merged:
        results = validate_merged(args.merged, schema)
        print()
        passed = sum(1 for v in results.values() if v == 'OK')
        total = len(results)
        print(f"Merged: {passed}/{total} passed")
