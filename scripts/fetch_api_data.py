import requests
import pandas as pd
from configs import settings
from scripts.helpers import save_json
import logging



movie_ids = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]

def fetch_movie_data(movie_id):
    url = f"{settings.BASE_URL}{movie_id}?api_key={settings.TMDB_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        logging.info(f"Successfully fetched data for movie ID {movie_id}")
        return response.json()
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for movie ID {movie_id}: {e}")
        return None


def run_extraction():
    all_data = []

    try:
        for movie_id in movie_ids:
            data = fetch_movie_data(movie_id)

            if data:
                all_data.append(data)
                save_json(data, f"{settings.RAW_DATA_DIR}/movie_{movie_id}.json")
                logging.info(f"Data for movie ID {movie_id} saved successfully.")

        return pd.DataFrame(all_data)
    except Exception as e:
        logging.critical(f"Critical error during data extraction: {e}")
        return pd.DataFrame()
