# TMDB Movie Analysis

Small ETL + analysis project that fetches movie details from TMDB, stores raw JSON, and provides KPI helpers + an analysis notebook.

## Contents
- [Project structure](#project-structure)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Key files & helpers](#key-files--helpers)
- [Notes](#notes)

## Project structure
- [configs/settings.py](configs/settings.py) — environment-backed config
- [scripts/fetch_api_data.py](scripts/fetch_api_data.py) — extraction script
- [scripts/helpers.py](scripts/helpers.py) — JSON save/load helpers
- [scripts/kpi.py](scripts/kpi.py) — KPI utility functions
- [notebooks/01_api_extraction.ipynb](notebooks/01_api_extraction.ipynb) — exploratory notebook
- raw_data/ — raw JSON responses (examples: [raw_data/movie_299534.json](raw_data/movie_299534.json), [raw_data/movie_19995.json](raw_data/movie_19995.json))
- [requirements.txt](requirements.txt)
- .env — local environment (API key)

## Quickstart
1. Create / activate a virtual environment (or use the provided `env/`).
2. Install dependencies:
```sh
pip install -r 

3. Add your TMDB API key to .env as API_KEY (or set env var).
4. Run extraction:
python

This will call the functions in scripts/fetch_api_data.py and save JSON to the raw_data/ folder.

Usage
Open notebooks/01_api_extraction.ipynb to reproduce cleaning, merging and KPI calculations.
Use KPI helpers in scripts/kpi.py to rank movies and compute profit/ROI.
Example:

Load raw JSON into a DataFrame (notebook shows this).
Call add_profit_columns to compute profit and roi.
Call rank_movies to get top-N by a metric.
Key files & helpers
configs/settings.py exposes:
TMDB_API_KEY
BASE_URL
RAW_DATA_DIR
scripts/fetch_api_data.py contains:
fetch_movie_data
run_extraction
scripts/helpers.py contains:
save_json
load_json
scripts/kpi.py contains:
rank_movies
add_profit_columns
Exploratory analysis available in notebooks/01_api_extraction.ipynb.
Notes
Raw JSON files are in raw_data/. Examples: raw_data/movie_299534.json, raw_data/movie_140607.json.
Helpers write readable JSON. See save_json.
Config reads .env via python-dotenv. See requirements.txt.

References (open files / symbols)
-  — [`TMDB_API_KEYBASE_URLRAW_DATA_DIR`](configs/settings.py)  
-  — [`fetch_movie_datarun_extraction`](scripts/fetch_api_data.py)  
-  — [`save_jsonload_json`](scripts/helpers.py)  
-  — [`rank_moviesadd_profit_columns`](scripts/kpi.py)  
-   
-   
-   
- , , 