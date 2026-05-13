#!/usr/bin/env python3
# Palmer LTER Seabird Scripts
# Script to run full cruise conversion, merge, and QC workflow
# Written by Sage Lichtenwalner, Rutgers University
# AI assistance: Substantial development support provided by GitHub Copilot (GPT-5.3-Codex).
# Final review and approval: Sage Lichtenwalner
# Revised 5/13/2026
# Usage (from cruise/):
#   python process_cruise.py

import argparse
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Run full cruise conversion + QC workflow")
parser.add_argument(
    "--env-name",
    default="seabirds",
    help="Conda environment name. Set to empty string to use current interpreter.",
)
args = parser.parse_args()

root = Path(__file__).resolve().parent
original = root / "original"
py = ["conda", "run", "-n", args.env_name, "python"] if args.env_name else [sys.executable]

try:
    print("== Convert Fraser ==")
    subprocess.run([*py, str(original / "convert_cruise_fraser.py")], cwd=str(original), check=True)
    print("== Convert 2021 ==")
    subprocess.run([*py, str(original / "convert_cruise_2021.py")], cwd=str(original), check=True)
    print("== Convert 2023 ==")
    subprocess.run([*py, str(original / "convert_cruise_2023.py")], cwd=str(original), check=True)
    print("== Convert 2024 ==")
    subprocess.run([*py, str(original / "convert_cruise_2024.py")], cwd=str(original), check=True)
    print("== Merge all ==")
    subprocess.run([*py, str(root / "merge_cruise.py"), "-d", "all"], cwd=str(root), check=True)
    print("== Cruise QC (failures only) ==")
    subprocess.run([*py, str(root / "qc_cruise.py"), "--dataset", "both", "--only-failures"], cwd=str(root), check=True)
except subprocess.CalledProcessError as exc:
    raise SystemExit(exc.returncode)

print("Cruise workflow complete.")