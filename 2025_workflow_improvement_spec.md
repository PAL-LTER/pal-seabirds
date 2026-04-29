# Palmer LTER Seabirds: 2025 Workflow Improvement Spec

## Scope

- One-time improvement work: Tasks 1-3 and 6-8.
- Annual run work: Task 4 (with Task 5 validation/signoff).

## 2025 Update Task List

1. Reorganize repo into station and cruise areas. (Completed)
- Keep current top-level merge scripts for now.
- Each area should keep original and formatted subdirectories.
- Use git mv so moved files are tracked as moves (not delete/add).

2. Station conversion workflow cleanup (keep year scripts explicit). (Completed)
- Keep convert_<year>.py scripts explicit.
- Add one shared helper module for repeated logic only: time/date parsing, dtype coercion, and basic value cleanup.
- Add post-convert checks per dataset: required columns, key null checks, and row count checks.
- Support expected-empty dataset/year combinations through an allowlist.

3. Station merge workflow cleanup (minimal changes). (Completed)
- Keep merge logic mostly unchanged.
- Add file existence checks before concat.
- Add concise run logging (not verbose): input files used, row counts, output file path.

4. Add 2025 station data and produce archive-ready outputs (annual run step). (Completed)
- Produce cleaned 2025 station files in formatted folders.
- Produce merged station outputs with final suffix/year range.
- Run diff review against prior EDI tables.

5. Validation check (required before release). (Completed)
- Create and maintain one master schema reference (columns + dtype expectations + exceptions).
- Keep dtype overrides needed by merge/export behavior.
- Validate column set, key field nulls, and simple format/range checks.
- Write a short validation summary (CSV or text) for release signoff.

6. Cruise conversion review and targeted improvements. (Completed)
- Focus first on Fraser-era cruise files, then confirm newer years still validate cleanly.
- Keep year-specific scripts explicit.
- Use shared helper logic for repeated cleaning steps (same approach as station scripts).
- Document major QC edits clearly in script comments and, if useful, a companion notes file.

7. Cruise dataset header/observation consistency refactor. (Completed)
- Standardize both stationary and moving transect outputs to two files per dataset: dataset header and observations.
- For Fraser and 2021 sources, split combined/partial formats into this same two-file structure.

8. Cruise data quality review for additional issues.
- Use existing cleaning scripts as the baseline issue catalog.
- Prioritize time and location checks first.
- Then review event number, coordinates, and obvious impossible values.
- Track newly found issues as cleanup items and decide blocking vs non-blocking before release.
- Validate cross-file relationship checks:
	- Dataset header key is unique.
	- Each observation row maps to exactly one dataset header row.
	- Unmatched rows are reported for review.

## Annual Validation Checklist (Reusable)

- All expected files were produced for each dataset.
- Column sets match master schema.
- Expected-empty files are on allowlist only.
- Header/observation mapping checks pass.
- Critical date/time/location checks pass.
- Diff review against prior EDI version is complete.
- Validation summary saved with release artifacts.

