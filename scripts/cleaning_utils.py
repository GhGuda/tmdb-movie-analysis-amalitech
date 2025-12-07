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
    f.close()

movies_df = pd.DataFrame(all_movies)
movies_df


def drop_irrelevant_columns(movies_df):
    try:
        #dropping unwanted columns
        drop_columns = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
        movies_df = movies_df.drop(columns=drop_columns, errors='ignore')
        return movies_df
    except Exception as e:
        logging.error(f"Error: {e}")
        return ""

drop_irrelevant_columns(movies_df)



def extract_name(value, key="name"):
    try:
        # Already processed (string)
        if isinstance(value, str):
            return value

        # Case 1: List of dicts
        if isinstance(value, list):
            values = [item.get(key, "") for item in value if isinstance(item, dict)]
            return "|".join(values)

        # Case 2: Single dict
        if isinstance(value, dict):
            return value.get(key, "")

        # Anything else → treat as empty
        return np.nan
    except Exception as e:
        logging.error(f"Error extracting names: {e}")
        return ""




def extracting_name_from_columns(movies_df):
    try:
        columns = [
            'belongs_to_collection',
            'genres', 
            'production_countries', 
            'production_companies', 
            'spoken_languages'
        ]

        for column in columns:
            movies_df[column] = movies_df[column].apply(
                lambda value: extract_name(value)
            )

        return movies_df
    except Exception as e:
        logging.error(f"Error extracting names: {e}")
        return ""

extracting_name_from_columns(movies_df)




def check_anomalies(movies_df):
    try:
        columns = ['genres', 'spoken_languages', 
                'production_companies', 
                'production_countries', 
                'belongs_to_collection']
        
        result = {}
        for col in columns:
            # value_counts shows the top values including NaN
            result[col] = [movies_df[col].value_counts()]
        return result
    except Exception as e:
        logging.error(f"Error checking anomalies: {e}")
        return ""
        

check_anomalies(movies_df)




def convert_column_datatypes(movies_df):
    try:
        numeric_cols = ['budget', 'revenue', 'popularity', 'id', 'vote_count', 'vote_average', 'runtime']
        for col in numeric_cols:
            movies_df[col] = pd.to_numeric(movies_df[col], errors='coerce')
        
        movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')
        return movies_df
    except Exception as e:
        logging.error(f"Error: {e}")
        return ""
        
convert_column_datatypes(movies_df).head()





def replacing_unrealistic_values(movies_df):
    try:
        for col in ['budget', 'revenue', 'runtime']:
            movies_df[col] = movies_df[col].replace(0, np.nan)
        
        movies_df.loc[movies_df['vote_count'] == 0, 'vote_average'] = np.nan

        for item in ['overview', 'tagline']:
            movies_df[item] = movies_df[item].replace(['No Data', 'None', ''], np.nan)
            
        return movies_df
    except Exception as e:
        logging.error(f"Error: {e}")
        return ""
replacing_unrealistic_values(movies_df).tail()





def clean_movies(movies_df):
    # Remove duplicates based on 'id' and 'title' 
    # Drop rows with unknown 'id' or 'title'
    # Keep rows with at least 10 non-NaN columns
    try:
        movies_df = movies_df.drop_duplicates(subset=['id', 'title'], keep='first')\
                    .dropna(subset=['id', 'title'])\
                    .dropna(thresh=10)
        
        # Keep only 'Released' movies and drop the 'status' column
        movies_df = movies_df[movies_df['status'] == 'Released'].drop(columns=['status'])
        
        return movies_df
    except Exception as e:
        logging.error(f"Error: {e}")
        return ""
clean_movies(movies_df).tail()




def reorder_columns(movie_df):
    ordered_columns = ['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
                        'original_language', 'budget', 'revenue', 'production_companies',
                        'production_countries', 'vote_count', 'vote_average', 'popularity',
                        'runtime', 'overview', 'spoken_languages', 'poster_path']
    movie_df = movies_df.reindex(columns=ordered_columns)
    return movie_df
reorder_columns(movies_df).tail()





def rank_movies(df, by, top=True, n=10, condition=None, new_col_name=None):
    """
    Rank movies based on a column.
    
    Parameters:
        df (DataFrame): Movies dataframe
        by (str or list): Column(s) to sort by
        top (bool): True → highest values, False → lowest
        n (int): Number of rows to return
        condition (callable, optional): Function to filter df before ranking
        new_col_name (str, optional): Add a column to label KPI
    
    Returns:
        DataFrame: Top/bottom ranked movies
    """
    try:
        df_filtered = df if condition is None else df[condition(df)]
        ranked = df_filtered.sort_values(by=by, ascending=not top).head(n)
        if new_col_name:
            ranked = ranked.assign(KPI=new_col_name).round(2)
        return ranked
    except Exception as e:
        logging.error(f"Error: {e}")
        return ""






# Highest/Lowest Revenue
highest_revenue = rank_movies(movies_df, by='revenue', top=True, new_col_name='Highest Revenue')
lowest_revenue  = rank_movies(movies_df, by='revenue', top=False, new_col_name='Lowest Revenue')
highest_revenue[['title', 'revenue']]

# Highest/Lowest Budget
highest_budget = rank_movies(movies_df, by='budget', top=True, new_col_name='Highest Budget')
lowest_budget  = rank_movies(movies_df, by='budget', top=False, new_col_name='Lowest Budget')

# Profit = Revenue - Budget
movies_df['profit'] = movies_df['revenue'] - movies_df['budget']
highest_profit = rank_movies(movies_df, by='profit', top=True, new_col_name='Highest Profit')
lowest_profit  = rank_movies(movies_df, by='profit', top=False, new_col_name='Lowest Profit')

# ROI = Revenue / Budget, only for Budget ≥ 10M
roi_condition = lambda df: df['budget'] >= 10_000_000
movies_df['roi'] = movies_df['revenue'] / movies_df['budget']
highest_roi = rank_movies(movies_df, by='roi', top=True, condition=roi_condition, new_col_name='Highest ROI')
lowest_roi  = rank_movies(movies_df, by='roi', top=False, condition=roi_condition, new_col_name='Lowest ROI')

# Most Voted Movies
most_voted = rank_movies(movies_df, by='vote_count', top=True, new_col_name='Most Voted')

# Highest/Lowest Rated Movies (only movies with ≥ 10 votes)
rating_condition = lambda df: df['vote_count'] >= 10
highest_rated = rank_movies(movies_df, by='vote_average', top=True, condition=rating_condition, new_col_name='Highest Rated')
lowest_rated  = rank_movies(movies_df, by='vote_average', top=False, condition=rating_condition, new_col_name='Lowest Rated')

# Most Popular Movies
most_popular = rank_movies(movies_df, by='popularity', top=True, new_col_name='Most Popular')





all_kpis = pd.concat([
    highest_revenue, lowest_revenue, 
    highest_budget, lowest_budget,
    highest_profit, lowest_profit,
    highest_roi, lowest_roi,
    most_voted, highest_rated, lowest_rated,
    most_popular
], ignore_index=True)

all_kpis




def search_movies(df, title_contains=None, genre=None, year=None, director=None):
    try:
        query = df

        if title_contains:
            query = query[query['title'].str.contains(title_contains, case=False, na=False)]

        if genre:
            query = query[query['genres'].apply(lambda g: genre in g if isinstance(g, list) else False)]

        if year:
            query = query[query['release_date'].dt.year == year]

        if director:
            query = query[query['director'] == director]

        if query.empty:
            return "No matching query"

        return query

    except Exception as e:
        logging.error(f"Error: {e}")
        return ""
    

search_movies(movies_df, title_contains="Avengers", genre="Action", year=2019)






#Searching for best rated sci-fi action movies starring B.willis
def best_rated_sci_fi_movies(movies_df):
    try:
        filtered_df = movies_df[
            movies_df['genres'].str.contains("Science Fiction", case=False, na=False) &
            movies_df['genres'].str.contains("Action", case=False, na=False) &
            movies_df['cast'].str.contains("Bruce Willis", case=False, na=False)
        ].sort_values(by='vote_average', ascending=False)

        return filtered_df

    except Exception as e:
        logging.error(f"Error: {e}")
        return ""

best_rated_sci_fi_movies(movies_df)




#Searching miovies with starring Uma Thurman directed by Quentin Tarantino
def uma_thurman_tarantino_movies(movies_df):
    try:
        filtered_df = movies_df[
            movies_df['cast'].str.contains("Uma Thurman", case=False, na=False) &
            movies_df['director'].str.contains("Quentin Tarantino", case=False, na=False)
        ].sort_values(by='runtime', ascending=True)

        return filtered_df

    except Exception as e:
        logging.error(f"Error: {e}")
        return ""

uma_thurman_tarantino_movies(movies_df)





def franchise_vs_standalone_performance(df, decimals=2):
    try:
        pd.options.display.float_format = '{:,.2f}'.format
        # Create franchise vs standalone indicator
        df['franchise_type'] = df['belongs_to_collection'].notna().map({
            True: 'Franchise',
            False: 'Standalone'
        })

        # Group and aggregate
        summary = (
            df.groupby('franchise_type')
              .agg(
                  mean_revenue=('revenue', 'mean'),
                  median_roi=('roi', 'median'),
                  mean_budget=('budget', 'mean'),
                  mean_popularity=('popularity', 'mean'),
                  mean_rating=('vote_average', 'mean')
              )
        )

        # Sort (Franchise usually higher but just in case)
        summary = summary.sort_values(by='mean_revenue', ascending=False)

        return summary

    except Exception as e:
        logging.error(f"Error: {e}")
        return ""

franchise_vs_standalone_performance(movies_df)





def most_successful_franchises(df):
    try:
        df['collection_name'] = df['belongs_to_collection']
        franchise_df = df[df['collection_name'].notna()]

        franchise_stats = franchise_df.groupby('collection_name').agg(
            total_movies=('id', 'count'),
            total_budget=('budget', 'sum'),
            mean_budget=('budget', 'mean'),
            total_revenue=('revenue', 'sum'),
            mean_revenue=('revenue', 'mean'),
            mean_rating=('vote_average', 'mean')
        ).sort_values(by='mean_revenue', ascending=False)

        return franchise_stats

    except Exception as e:
        logging.error(f"Error: {e}")
        return ""
most_successful_franchises(movies_df)




def most_successful_directors(df):
    try:
        director_stats = df.groupby('director').agg(
            total_movies=('id', 'count'),
            total_revenue=('revenue', 'sum'),
            mean_rating=('vote_average', 'mean')
        ).sort_values(by='total_revenue', ascending=False)

        return director_stats

    except Exception as e:
        logging.error(f"Error: {e}")
        return ""
most_successful_directors(movies_df)




#Revenue vs Budget Trends
plt.figure(figsize=(10,6))
plt.scatter(movies_df['budget'], movies_df['revenue'], alpha=0.7)
plt.title('Revenue vs Budget')
plt.xlabel('Budget (USD)')
plt.ylabel('Revenue (USD)')
plt.grid(True)
plt.show()



# ROI Distribution by Genere
# explode genres first
df_genres = movies_df.copy()
df_genres['genres'] = df_genres['genres'].str.split('|')
df_genres = df_genres.explode('genres')

# plot ROI distribution
plt.figure(figsize=(12,6))
df_genres.boxplot(column='roi', by='genres', rot=90)
plt.title("ROI Distribution by Genre")
plt.suptitle("")
plt.xlabel("Genre")
plt.ylabel("ROI")
plt.show()



# Popularity vs Rating 
plt.figure(figsize=(10,6))
plt.scatter(movies_df['popularity'], movies_df['vote_average'])
plt.xlabel("Popularity")
plt.ylabel("Rating (vote_average)")
plt.title("Popularity vs Rating")
plt.grid(True)
plt.show()



# Yearly Trends in Box Office Performance

#Create a year column

movies_df['year'] = movies_df['release_date'].dt.year
yearly = movies_df.groupby('year')['revenue'].sum().reset_index()


#Plot

plt.figure(figsize=(12,6))
plt.plot(yearly['year'], yearly['revenue'])
plt.xlabel("Year")
plt.ylabel("Total Revenue")
plt.title("Yearly Box Office Revenue Trends")
plt.grid(True)
plt.show()




# Franchise vs Standalone Success
franchise_stats = movies_df.groupby('franchise_type')[['revenue', 'roi', 'budget']].mean()

plt.figure(figsize=(8,5))
franchise_stats['roi'].plot(kind='bar')
plt.title("ROI: Franchise vs Standalone")
plt.ylabel("ROI")
plt.grid(True)
plt.show()


