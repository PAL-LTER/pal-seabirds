# Palmer LTER Seabirds: 2025 Workflow Improvement Spec

## Scope

- This spec tracks 2025 workflow goals for station and cruise processing.

## Station Task List

- [x] Reorganize station into its own workflow directory
    -  Keep clear raw -> formatted -> merged workflow locations
	-  Store data in  station/original, station/formatted, and station/merged location

- [x] Refactor station conversion scripts
	- Keep explicit convert_<year>.py scripts.
	- Use a shared helper module for repeated logic: time/date parsing, dtype coercion, and basic value cleanup.
	- Add post-convert checks for each dataset: required columns, key null checks, and row count checks.

- [x] Refactor and cleanup station merge workflow
	- Preserve merge behavior while making runs more repeatable.
	- Add file-existence checks before concat.
	- Improve run logging clarity.

- [x] Station validation workflow
	- Add validation schema for key fields, and core format/range checks before release.
	- Provide short validation summaries on formatted and merged outputs for review.

- [x] Station data updates
	- [x] Complete 2025 conversion, merge, and validation.
	- [x] Complete 2025 diff review with prior data.

## Cruise Task List

- [x] Reorganize cruise into its own workflow directory
	- Keep clear raw -> formatted -> merged -> QC workflow locations.
	- Store data in cruise/original, cruise/formatted, and cruise/merged.
	- Move legacy scripts to cruise/old.

- [x] Refactor cruise conversion scripts
	- Keep explicit convert_<year>.py scripts.
	- Focus first on Fraser-era cruise files, then confirm newer years validate cleanly.
	- Use shared helper logic for repeated cleaning steps where appropriate.
	- Document major QC edits in script comments and companion notes when useful.

- [x] Refactor and cleanup cruise merge workflow
	- Preserve merge behavior while making runs more repeatable.
	- Standardize merged output structure to header/observation pairs.
	- Keep transect and stationary merge outputs aligned.

- [x] Cruise validation workflow
	- Consolidate QC into qc_cruise.py with rule-driven checks and issue exports.
	- Use process_cruise.py as the single workflow runner.
	- Validate cross-file relationship checks:
		- Dataset header key is unique.
		- Each observation row maps to exactly one dataset header row.
		- Unmatched rows are reported for review.

- [x] Cruise data quality cleanup
	- Use existing cleaning scripts as the baseline issue catalog.
	- Prioritize time/location checks first.
	- Then review event number, coordinates, and obvious impossible values.
	- Track newly found issues and classify as blocking vs non-blocking.
	- Complete essential cleanup needed for 2025 processing.

- [x] Cruise data updates
	- [x] Complete 2025 framework and run path.
	- [x] Complete 2025 conversion, merge, and QC review.

## Deferred for Next Version

- Additional cruise data review and edits beyond essential 2025 cleanup.
- Follow-up on flagged records that may require row-level fixes or SME review.
- Current deferred focus:
	- H11 DateTime parseability
	- X01 duplicate header keys (Cruise + Event Number)
	- X02 observation keys without matching header key
	- H13-H18 and marker cleanup (H03/H12/H19/H20)

## 2025 Validation Checklist

- [x] All expected files were produced for each dataset.
- [x] Column sets match master schema.
- [x] Expected-empty files are on allowlist only.
- [x] Header/observation mapping checks pass.
- [x] Critical date/time/location checks pass.
- [x] Diff review against prior EDI version is complete.
- [x] Validation summary saved with release artifacts.

