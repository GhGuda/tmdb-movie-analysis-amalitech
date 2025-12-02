from dotenv import load_dotenv
import os

load_dotenv()


TMDB_API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.themoviedb.org/3/movie/"


RAW_DATA_DIR = "raw_data"
