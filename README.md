# Palmer LTER Seabirds Archive

This repository includes the raw datafiles and code needed to aggregate the long-term Seabird datasets for the [Palmer LTER](http://pallter.marine.rutgers.edu) project. This repository includes both the cruise and Palmer Station area datafiles.  Following the 2020 field season, data is collected and managed by Megan Cimino (University of California at Santa Cruz and NOAA).  Before that, seabird data was collected by William Fraser (Polar Oceans Research Group).

The processed datasets are archived in Environmental Data Initiative’s data repository (see this link to search for [PAL penguin datasets](http://portal.edirepository.org:80/nis/simpleSearch?defType=edismax&q=subject:%22penguin%22&fq=-scope:ecotrends&fq=-scope:lter-landsat*&fq=scope:(knb-lter-pal)&fl=id,packageid,title,author,organization,pubdate,coordinates&debug=false)).

This repo is currently managed by Sage Lichtenwalner, PAL Information Manager, Rutgers University

## Repository Contents

### Directories
| Directory | Description |
|-----------|-------------|
| [station/](station) | Station-area data and scripts |
| [station/original/](station/original) | Raw station files |
| [station/formatted/](station/formatted) | Standardized station CSVs by dataset and year |
| [station/merged/](station/merged) | Merged station outputs |
| [cruise/](cruise) | Cruise data and scripts |
| [cruise/original/](cruise/original) | Raw cruise files |
| [cruise/formatted/](cruise/formatted) | Standardized cruise CSV outputs |
| [cruise/merged/](cruise/merged) | Merged cruise outputs |


## Environment Setup
Scripts use the conda environment `seabirds` with packages listed in [environment.yml](environment.yml). Create it once, then activate it for routine use.

```bash
conda env create -f environment.yml
conda activate seabirds
```

## Processing Steps
This dataset is typically updated every year, after the austral summer field season.  Use these steps to update the datasets.

### Station Data

1. Add new raw files to [station/original](station/original).
2. Create or update the needed year-specific conversion script, such as `convert_station_<year>.py`.
3. Run the conversion script from [station/original/](station/original):

    ```bash
    cd station/original
    python convert_station_2025.py
    ```

4. Merge the formatted outputs from [station/](station):

    ```bash
    cd station
    python merge_station.py -d all -s 1991_2025
    ```

    Use `--dataset` to run one dataset or `all`, and `--suffix` to control the output year range.

5. Run station validation before release:

    ```bash
    cd station
    python validate_station.py --all-formatted
    python validate_station.py --merged
    ```

6. Optional: compare the merged outputs against a reference directory (this will need manual tweaking).

    ```bash
    cd station
    python compare_merged.py
    ```

7. Use ezEML to update the metadata for the new datasets for archiving.  You can also move the new files into a YEAR subdirectory for comparing across years.


### Cruise Data

Cruise data includes transect and stationary seabird surveys collected during each austral summer cruise.

1. Add new raw files to [cruise/original](cruise/original), usually in a year-specific subfolder.
2. Create or update a year-specific conversion script only when a new source format requires it.
3. Run the full cruise workflow from [cruise/](cruise):

    ```bash
    cd cruise
    conda run -n seabirds python process_cruise.py
    ```

    This runs the all of the cruise conversion scripts, merges the output into combined stationary/transect and header/observation files, and then runs a series of QC checks.

4. Optional: If you need to run the merge/qc steps separately:

    ```bash
    cd cruise
    conda run -n seabirds python merge_cruise.py -d all
    conda run -n seabirds python qc_cruise.py --dataset both --only-failures
    ```

5. Review QC outputs in [cruise/qc_reports/](cruise/qc_reports).
6. Update [cruise/qc_rules.csv](cruise/qc_rules.csv) only when adding or changing QC rules.


### Scripts
| Script | Description |
|--------|-------------|
| [station/original/convert_station_fraser.py](station/original/convert_station_fraser.py) | Converts pre-2021 Fraser-era `.xls` files to formatted CSVs |
| [station/original/convert_station_2023.py](station/original/convert_station_2023.py) | Converts 2023 Excel files to formatted CSVs |
| [station/original/convert_station_2024.py](station/original/convert_station_2024.py) | Converts 2024 Excel files to formatted CSVs |
| [station/original/convert_station_2025.py](station/original/convert_station_2025.py) | Converts 2025 Excel files to formatted CSVs |
| [station/original/common.py](station/original/common.py) | Shared helpers used by conversion scripts |
| [station/merge_station.py](station/merge_station.py) | Merges all formatted station CSVs into combined outputs |
| [station/validate_station.py](station/validate_station.py) | Validates formatted and merged files against `station_schema.csv` |
| [station/generate_schema.py](station/generate_schema.py) | Regenerates `station_schema.csv` by inspecting formatted files |
| [station/compare_merged.py](station/compare_merged.py) | Compares merged outputs against a reference directory |
| [cruise/original/convert_cruise_fraser.py](cruise/original/convert_cruise_fraser.py) | Converts Fraser-era (1993–2020) cruise `.xls` files to formatted CSVs |
| [cruise/original/convert_cruise_2021.py](cruise/original/convert_cruise_2021.py) | Converts 2021 cruise files to formatted CSVs |
| [cruise/original/convert_cruise_2023.py](cruise/original/convert_cruise_2023.py) | Converts 2022–23 cruise Excel files to formatted CSVs |
| [cruise/original/convert_cruise_2024.py](cruise/original/convert_cruise_2024.py) | Converts 2023–24 cruise Excel files to formatted CSVs |
| [cruise/original/common.py](cruise/original/common.py) | Shared helpers used by cruise conversion scripts |
| [cruise/merge_cruise.py](cruise/merge_cruise.py) | Merges all formatted cruise CSVs into combined outputs |
| [cruise/process_cruise.py](cruise/process_cruise.py) | Runs the full cruise workflow: convert, merge, and QC |
| [cruise/qc_cruise.py](cruise/qc_cruise.py) | Runs rule-based QC checks and writes issue reports |
| [cruise/lib_qc_checks.py](cruise/lib_qc_checks.py) | Rule-dispatch functions used by the cruise QC runner |
| [cruise/lib_qc_utility.py](cruise/lib_qc_utility.py) | Shared masks, constants, and helper functions for cruise QC |