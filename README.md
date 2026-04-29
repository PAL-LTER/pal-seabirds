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

## Environment Setup
Scripts require Python 3.12 and the packages listed in [environment.yml](environment.yml).  To create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate seabirds
```

## Processing Steps
This dataset is typically updated every year, after the austral summer field season.  Use these steps to update the datasets.

1. Add raw station files to [station/original](station/original) (or raw cruise files to [cruise/original](cruise/original)).
2. Create or update year-specific conversion scripts as needed (`convert_station_<year>.py` or cruise equivalent).
3. Run conversion scripts from their script directory to produce updated files in `formatted`.

    ```bash
    cd station/original
    python convert_station_2025.py
    ```

4. Run the merge script from the `station/` directory.

    ```bash
    cd station
    python merge_station.py -d all -s 1991_2025
    ```

    You can specify `--dataset all` to process all datasets, or a single dataset name.  Use `--suffix` to set the year range in the output filenames.

5. Run station validation before release:

    ```bash
    cd station
    python validate_station.py --all-formatted
    python validate_station.py --merged
    ```

6. Optional: run [station/compare_merged.py](station/compare_merged.py) to compare merged outputs against a reference directory.

    ```bash
    cd station
    python compare_merged.py
    ```
7. Optional: update the `compare_station` script for EDI-specific diff review.
8. If desired, move the new files into a YEAR subdirectory.
9. Use ezEML to update the metadata for the new datasets for archiving.

### Cruise Data

Cruise data covers transect and stationary seabird surveys conducted during each austral summer cruise.

1. Add raw cruise files to [cruise/original](cruise/original) under a year-specific subfolder.
2. Create or update the year-specific conversion script (`convert_cruise_<year>.py`).
3. Run conversion scripts from the `cruise/original/` directory.

    ```bash
    cd cruise/original
    python convert_cruise_2024.py
    ```

4. Run the merge script from the `cruise/` directory.

    ```bash
    cd cruise
    python merge_cruise.py -d all -s 1993_2024
    ```

    You can specify `--dataset all` to process all four datasets, or a single dataset name.  Use `--suffix` to set the year range in the output filenames.
