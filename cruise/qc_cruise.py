# Palmer LTER Seabird Scripts
# Script to run rule-driven cruise QC validation and issue export
# Written by Sage Lichtenwalner, Rutgers University
# AI assistance: Substantial development support provided by GitHub Copilot (GPT-5.3-Codex).
# Final review and approval: Sage Lichtenwalner
# Revised 5/13/2026
# Usage (from cruise/):
#   python qc_cruise.py --dataset both --only-failures

import argparse
import os
import pandas as pd

import lib_qc_utility as qc
from lib_qc_checks import CHECK_FUNCTIONS


def parse_params(param_text):
    if not isinstance(param_text, str) or not param_text.strip():
        return {}
    out = {}
    parts = [p.strip() for p in param_text.split(";") if p.strip()]
    for part in parts:
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def load_rules(path):
    rules = pd.read_csv(path, dtype=str).fillna("")
    rules = rules[rules["enabled"].str.lower().isin(["true", "1", "yes", "y", ""])].copy()
    rules["params_dict"] = rules["params"].apply(parse_params)
    return rules.to_dict("records")


def row_issue_record(dataset, table_name, rule, row, current_value, explanation):
    source_index = row["_source_index"] if "_source_index" in row else row.name
    source_row_number = row["_source_row_number"] if "_source_row_number" in row else int(source_index) + 2
    return {
        "dataset": dataset,
        "table": table_name,
        "source_row_index": int(source_index),
        "source_row_number": int(source_row_number),
        "Cruise": row["Cruise"] if "Cruise" in row else "",
        "Event Number": row["Event Number"] if "Event Number" in row else "",
        "column_name": rule["column_name"],
        "current_value": current_value,
        "error_code": rule["rule_code"],
        "severity": rule["severity"],
        "explanation": explanation,
    }


def run_rule(rule, dataset_name, data):
    if rule["dataset"] not in ("both", dataset_name):
        return None
    check_fn = rule["check_fn"]
    if check_fn not in CHECK_FUNCTIONS:
        raise KeyError(f"Unknown check function: {check_fn} for rule {rule['rule_code']}")
    result = CHECK_FUNCTIONS[check_fn](rule, data, rule["params_dict"])
    count = int(result["count"])
    passed = count == 0
    status = "PASSED" if passed else ("WARNING" if rule["severity"] == "warn" else "FAILED")
    return {
        "rule": rule,
        "count": count,
        "status": status,
        "passed": passed,
        "bad_rows": result["bad_rows"],
        "explanation": result["explanation"],
        "column_name": result["column_name"],
    }


def build_dataset_outputs(dataset_name, data, rules):
    results = []
    issues = []
    for rule in rules:
        out = run_rule(rule, dataset_name, data)
        if out is None:
            continue
        results.append(out)

        if out["count"] == 0:
            continue

        table_name = f"{dataset_name}_{rule['table']}"
        bad_rows = out["bad_rows"]
        if bad_rows is None or bad_rows.empty:
            continue

        if rule["table"] == "cross":
            table_name = f"{dataset_name}_obs" if rule["rule_code"] == "X02" else f"{dataset_name}_header"

        for _, row in bad_rows.iterrows():
            col = rule["column_name"]
            if col in row:
                current_value = row[col]
            elif "|" in col:
                bits = [k.strip() for k in col.split("|") if k.strip() in row]
                current_value = "|".join(str(row[k]) for k in bits)
            else:
                current_value = ""
            issues.append(row_issue_record(dataset_name, table_name, rule, row, current_value, out["explanation"]))

    return results, pd.DataFrame(issues)


def print_summary(dataset_name, results, only_failures=False):
    print(f"\nCRUISE QC TEST RESULTS: {dataset_name.capitalize()}")
    passed = warnings = failed = 0
    for out in results:
        rule = out["rule"]
        status = out["status"]
        if only_failures and status == "PASSED":
            passed += 1
            continue
        icon = {"PASSED": "✅", "FAILED": "❌", "WARNING": "⚠️"}[status]
        print(f"{icon} {rule['rule_code']} {rule['check_name']} ... {status}")
        if status != "PASSED":
            print(f"    notes: count={out['count']}")
        if status == "FAILED":
            failed += 1
        elif status == "WARNING":
            warnings += 1
        else:
            passed += 1

    print("\nSummary:")
    print(f"  passed={passed}")
    print(f"  warnings={warnings}")
    print(f"  failed={failed}")
    print(f"  total_tests={len(results)}")


def write_issues(df, outdir, dataset_name):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"qc_issues_{dataset_name}.csv")
    df.to_csv(path, index=False)
    return path


def main():
    parser = argparse.ArgumentParser(description="Rule-driven Cruise QC")
    parser.add_argument("--merged-dir", default="merged")
    parser.add_argument("--rules-file", default="qc_rules.csv")
    parser.add_argument("--outdir", default="qc_reports")
    parser.add_argument("--dataset", choices=["transect", "stationary", "both"], default="both")
    parser.add_argument("--only-failures", action="store_true")
    args = parser.parse_args()

    data_all = qc.load_inputs(args.merged_dir, dtype_str=True, add_source_rows=True)
    rules = load_rules(args.rules_file)

    datasets = []
    if args.dataset in ("transect", "both"):
        datasets.append(("transect", {"header": data_all["transect_header"], "obs": data_all["transect_obs"]}))
    if args.dataset in ("stationary", "both"):
        datasets.append(("stationary", {"header": data_all["stationary_header"], "obs": data_all["stationary_obs"]}))

    for dataset_name, data in datasets:
        results, issues = build_dataset_outputs(dataset_name, data, rules)
        print_summary(dataset_name, results, only_failures=args.only_failures)
        out_path = write_issues(issues, args.outdir, dataset_name)
        print(f"\nQC ISSUE EXPORT SUMMARY: {dataset_name}")
        print(f"  issue_rows={len(issues)}")
        print(f"  csv={out_path}")


if __name__ == "__main__":
    main()
