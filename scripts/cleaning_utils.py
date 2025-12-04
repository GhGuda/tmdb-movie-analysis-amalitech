import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
import matplotlib.pyplot as plt


#reading json files from raw_data folder
raw_movies_json_folder = Path('raw_data')
json_files = raw_movies_json_folder.glob('*.json')

all_movies = []

for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        movie = json.load(f)
        all_movies.append(movie)

movies_df = pd.DataFrame(all_movies)
movies_df.head()


def extract_name_from_list_of_dict(col, key="name"):
    #Function to extract names from a list of dictionaries and join them with '|'
    try:
        if isinstance(col, list):
            values = [item.get(key, "") for item in col] 
            return "|".join(values)
        return np.nan
    except Exception as e:
        logging.error(f"Error extracting names from list of dict: {e}")
        return np.nan


def extract_name_from_dict(col, key="name"):
    #Function to extract name from a dictionary
    try:
        if isinstance(col, dict):
            return col.get(key, np.nan)
        return np.nan
    except Exception as e:
        logging.error(f"Error extracting name from dict: {e}")
        return np.nan


def clean_movie_data(df):
    #dropping unwanted columns
    drop_columns = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
    df = df.drop(columns=drop_columns, errors='ignore')


    # Extracting JSON Columns
    df['belongs_to_collection'] = df['belongs_to_collection'].apply(lambda name: extract_name_from_dict(name))
    df['genres'] = df['genres'].apply(lambda name: extract_name_from_list_of_dict(name))
    df['production_countries'] = df['production_countries'].apply(lambda name: extract_name_from_list_of_dict(name))
    df['production_companies'] = df['production_companies'].apply(lambda name: extract_name_from_list_of_dict(name))
    df['spoken_languages'] = df['spoken_languages'].apply(lambda name: extract_name_from_list_of_dict(name))


    numeric_cols = ['budget', 'revenue', 'popularity', 'id', 'vote_count', 'vote_average', 'runtime']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    
    for col in ['budget', 'revenue', 'runtime']:
        df[col] = df[col].replace(0, np.nan)
    
    df['budget'] = df['budget'] / 1_000_000
    df['revenue'] = df['revenue'] / 1_000_000


    df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan

    for item in ['overview', 'tagline']:
        df[item] = df[item].replace(['No Data', 'None', ''], np.nan)

    # Remove duplicates
    df = df.drop_duplicates(subset=['id', 'title'], keep='first')

    # Drop movies with missing IDs or Titles
    df = df.dropna(subset=['id', 'title'])

    df = df.dropna(thresh=10)

    df = df[df['status'] == 'Released'].drop(columns=['status'])

    ordered_columns = ['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
                        'original_language', 'budget', 'revenue', 'production_companies',
                        'production_countries', 'vote_count', 'vote_average', 'popularity',
                        'runtime', 'overview', 'spoken_languages', 'poster_path']
    df = df.reindex(columns=ordered_columns)


    # Profit = Revenue - Budget
    # df['profit'] = df['revenue'] - df['budget']

    # df['profit'].min()




    return df



def check_anomalies(df, columns):
    #Function to check for anomalies in specified columns
    try:
        result = {}
        for col in columns:
            result[col] = df[col].value_counts()
        return result
    except Exception as e:
        logging.error(f"Error checking anomalies: {e}")
        return {}

#Checking for anomalies and correcting data types    
columuns_to_check = ['genres', 'spoken_languages', 'production_companies', 'production_countries', 'belongs_to_collection']
check_anomalies(movies_df, columuns_to_check)