from scripts.extraction.fetch_api_data import run_extraction
# from scripts.processing.clean_data import load_movies_from_raw_data
from scripts.processing.clean_data import (
    load_movies_from_raw_data,
    drop_irrelevant_columns,
    extracting_name_from_columns,
    convert_column_datatypes,
    replacing_unrealistic_values,
    clean_movies,
    extract_cast_and_crew,
    reorder_columns
)

def run_pipeline():
    """
    Run the full TMDB movie data pipeline:
    extraction -> cleaning -> analysis-ready dataset
    """
    print("Starting TMDB movie data pipeline...")

    # Step 1: Extract raw data from TMDB API
    run_extraction()

    # Step 2: Load raw JSON files into DataFrame
    movies_df = load_movies_from_raw_data()
    if movies_df.empty:
        print("No data extracted. Pipeline terminated.")
        return movies_df
    else:
        # Step 3: Data cleaning and preparation
        movies_df = drop_irrelevant_columns(movies_df)
        movies_df = extracting_name_from_columns(movies_df)
        movies_df = convert_column_datatypes(movies_df)
        movies_df = replacing_unrealistic_values(movies_df)
        movies_df = clean_movies(movies_df)
        movies_df = extract_cast_and_crew(movies_df)
        movies_df = reorder_columns(movies_df)

        print("Pipeline completed successfully.")

        # Step 4: Return analysis-ready dataset
        return movies_df