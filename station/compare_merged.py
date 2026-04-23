# Palmer LTER Seabird Scripts
# Quick comparison of station merged outputs against a reference directory
# Compares row/column shape and column names by matching filenames
# Revised 4/22/2026
# Usage (from station/):
#   python compare_merged.py
#   python compare_merged.py --ref ../dev/2024/Data --merged merged

import argparse
import os
import pandas as pd

def compare(filename, new_path, ref_path):
    new = pd.read_csv(new_path, dtype=str)
    ref = pd.read_csv(ref_path, dtype=str)

    row_ok = new.shape[0] == ref.shape[0]
    col_ok = list(new.columns) == list(ref.columns)
    extra = sorted(set(new.columns) - set(ref.columns))
    missing = sorted(set(ref.columns) - set(new.columns))

    status = 'OK' if row_ok and col_ok else 'DIFF'
    print('[%s] %s' % (status, filename))
    print('  rows: %s new vs %s ref%s' % (
        new.shape[0], ref.shape[0], '' if row_ok else ' *** MISMATCH'))
    print('  cols: %s new vs %s ref%s' % (
        new.shape[1], ref.shape[1], '' if col_ok else ' *** MISMATCH'))
    if extra:
        print('  extra cols in new:    %s' % extra)
    if missing:
        print('  missing cols vs ref:  %s' % missing)
    if not col_ok and not extra and not missing:
        print('  col order differs')
        for i, (n, r) in enumerate(zip(new.columns, ref.columns)):
            if n != r:
                print('    pos %s: new=%s  ref=%s' % (i, n, r))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare merged station outputs against a reference directory')
    parser.add_argument('--ref', type=str, default='../dev/2024/Data',
        help='Path to reference directory (default: ../dev/2024/Data)')
    parser.add_argument('--merged', type=str, default='merged',
        help='Path to merged output directory (default: merged)')
    args = parser.parse_args()

    print('Comparing %s  vs  %s\n' % (args.merged, args.ref))

    # Compare all CSV files that exist in the merged directory
    for filename in sorted(os.listdir(args.merged)):
        if not filename.endswith('.csv'):
            continue
        new_path = os.path.join(args.merged, filename)
        ref_path = os.path.join(args.ref, filename)
        if not os.path.exists(ref_path):
            print('[NEW]  %s — no matching file in ref' % filename)
            continue
        compare(filename, new_path, ref_path)
        print()

    # Flag any ref files not present in merged
    for filename in sorted(os.listdir(args.ref)):
        if not filename.endswith('.csv'):
            continue
        if not os.path.exists(os.path.join(args.merged, filename)):
            print('[REF ONLY] %s — not in merged output' % filename)
