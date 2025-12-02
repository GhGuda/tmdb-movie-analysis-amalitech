import requests
import pandas as pd
from configs import settings
from scripts.helpers import save_json



movie_ids = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]

def fetch_movie_data(movie_id):
    url = f"{settings.BASE_URL}{movie_id}?api_key={settings.TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Movie with ID {movie_id} not found: {response.status_code}")
        return None
    



def run_extraction():
    all_data = []

    for movie_id in movie_ids:
        data = fetch_movie_data(movie_id)

        if data:
            all_data.append(data)
            save_json(data, f"{settings.RAW_DATA_DIR}/movie_{movie_id}.json")

    return pd.DataFrame(all_data)


if __name__ == "__main__":
    df = run_extraction()
    print(df.head())