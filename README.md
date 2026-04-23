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
| [cruise/merge_cruise.py](cruise/merge_cruise.py) | Merges cruise datasets |

## Environment Setup
Scripts require Python 3.12 and the packages listed in [environment.yml](environment.yml).  To create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate seabirds
```

## Processing Steps
This dataset is typically updated every year, after the austral summer field season.  Use these steps to update the datasets.

1. Add the original data files (provided by the field team) to the `original` directory, into a new directory for that year.
2. If necessary, create a new script to reformat the original files into the common CSV format for each datasets.  (See the formatted directory for the format to match for each dataset.)
3. Move the reformatted files to the appropriate subdirectory in the `formatted` directory.
4. Run the appropriate merge script.
  * You can specify `--dataset all` to process all datasets handled by the script, or you can specify a single dataset to process.
  * You can also use the `--suffix` to customize the file suffix.  By default *_merged.csv* will be used.  We recommend specifying the year range, e.g. `--suffix 1991-2024` for the final files. 
5. Optional: Update the `compare_station` script to compare the latest datasets with the previously archived versions on EDI.  (Make sure the input and output filenames are correct.)  Review the output to make sure the updates are correct.
6. If desired, move the new files into a YEAR subdirectory.
7. Use ezEML to update the metadata for the new datasets for archiving.
