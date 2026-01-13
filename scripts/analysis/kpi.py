from unittest import result
import pandas as pd
import logging


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
        data = df.copy()
        df_filtered = data if condition is None else data[condition(data)]
        ranked = df_filtered.sort_values(by=by, ascending=not top).head(n)
        if new_col_name:
            ranked["KPI"] = new_col_name
        return ranked
    except Exception as e:
        logging.error(f"rank_movies failed: {e}")
        return pd.DataFrame()




# Highest/Lowest Revenue
# highest_revenue = rank_movies(movies_df, by='revenue_musd', top=True, new_col_name='Highest Revenue')
# lowest_revenue  = rank_movies(movies_df, by='revenue_musd', top=False, new_col_name='Lowest Revenue')
# highest_revenue[['title', 'revenue']]

# Highest/Lowest Budget
# highest_budget = rank_movies(movies_df, by='budget_musd', top=True, new_col_name='Highest Budget')
# lowest_budget  = rank_movies(movies_df, by='budget_musd', top=False, new_col_name='Lowest Budget')

# Profit = Revenue - Budget
# movies_df['profit'] = movies_df['revenue_musd'] - movies_df['budget_musd']
# highest_profit = rank_movies(movies_df, by='profit', top=True, new_col_name='Highest Profit')
# lowest_profit  = rank_movies(movies_df, by='profit', top=False, new_col_name='Lowest Profit')

# ROI = Revenue / Budget, only for Budget ≥ 10M
# roi_condition = lambda df: df['budget_musd'] >= 10
# movies_df['roi'] = movies_df['revenue_musd'] / movies_df['budget_musd']
# highest_roi = rank_movies(movies_df, by='roi', top=True, condition=roi_condition, new_col_name='Highest ROI')
# lowest_roi  = rank_movies(movies_df, by='roi', top=False, condition=roi_condition, new_col_name='Lowest ROI')

# Most Voted Movies
# most_voted = rank_movies(movies_df, by='vote_count', top=True, new_col_name='Most Voted')

# Highest/Lowest Rated Movies (only movies with ≥ 10 votes)
# rating_condition = lambda df: df['vote_count'] >= 10
# highest_rated = rank_movies(movies_df, by='vote_average', top=True, condition=rating_condition, new_col_name='Highest Rated')
# lowest_rated  = rank_movies(movies_df, by='vote_average', top=False, condition=rating_condition, new_col_name='Lowest Rated')

# Most Popular Movies
# most_popular = rank_movies(movies_df, by='popularity', top=True, new_col_name='Most Popular')





# all_kpis = pd.concat([
#     highest_revenue, lowest_revenue, 
#     highest_budget, lowest_budget,
#     highest_profit, lowest_profit,
#     highest_roi, lowest_roi,
#     most_voted, highest_rated, lowest_rated,
#     most_popular
# ], ignore_index=True)

# all_kpis




def search_movies(df, title_contains=None, genre=None, year=None, director=None):
    """
        Search movies using multiple optional filters.

        Args:
            df (pd.DataFrame): Analysis-ready dataset.
            title_contains (str, optional): Partial title match.
            genre (str, optional): Genre keyword.
            year (int, optional): Release year.
            director (str, optional): Director name.

        Returns:
            pd.DataFrame: Filtered movies.
    """

    try:
        query = df.copy()

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
        logging.error(f"search_movies failed: {e}")
        return pd.DataFrame()
    



def franchise_vs_standalone_performance(df):
    """
        Compare performance between franchise and standalone movies.

        Args:
            df (pd.DataFrame): Analysis-ready dataset.

        Returns:
            pd.DataFrame: Aggregated performance metrics.
    """

    try:
        data = df.copy()

        pd.options.display.float_format = '{:,.2f}'.format
        data['franchise_type'] = data['belongs_to_collection'].notna().map({
            True: 'Franchise',
            False: 'Standalone'
        })

        summary = (
            data.groupby('franchise_type')
              .agg(
                  mean_revenue=('revenue_musd', 'mean'),
                  median_roi=('roi', 'median'),
                  mean_budget=('budget_musd', 'mean'),
                  mean_popularity=('popularity', 'mean'),
                  mean_rating=('vote_average', 'mean')
              ).sort_values(by='mean_revenue', ascending=False)

        )

        return summary

    except Exception as e:
        logging.error(f"franchise_vs_standalone_performance failed: {e}")
        return pd.DataFrame()




def most_successful_directors(df):
    """
        Identify directors with highest total revenue.

        Args:
            df (pd.DataFrame): Analysis-ready dataset.

        Returns:
            pd.DataFrame: Director-level performance metrics.
    """
    try:
        return (
            df.groupby("director")
              .agg(
                  total_movies=("id", "count"),
                  total_revenue=("revenue_musd", "sum"),
                  mean_rating=("vote_average", "mean")
              )
              .sort_values("total_revenue", ascending=False)
        )

    except Exception as e:
        logging.error(f"most_successful_directors failed: {e}")
        return pd.DataFrame()
    




#Searching for best rated sci-fi action movies starring B.willis
def best_rated_sci_fi_movies(df):
    """
    Retrieve best-rated Sci-Fi Action movies starring Bruce Willis.

    Args:
        df (pd.DataFrame): Analysis-ready movie dataset.

    Returns:
        pd.DataFrame: Filtered and sorted movies.
    """

    try:
        filtered_df = df[
            df['genres'].str.contains("Science Fiction", case=False, na=False) &
            df['genres'].str.contains("Action", case=False, na=False) &
            df['cast'].str.contains("Bruce Willis", case=False, na=False)
        ].sort_values(by='vote_average', ascending=False)

        return filtered_df

    except Exception as e:
        logging.error(f"best_rated_sci_fi_movies failed: {e}")
        return pd.DataFrame()




#Searching miovies with starring Uma Thurman directed by Quentin Tarantino
def uma_thurman_tarantino_movies(df):
    """
    Retrieve movies starring Uma Thurman directed by Quentin Tarantino.

    Args:
        df (pd.DataFrame): Analysis-ready movie dataset.

    Returns:
        pd.DataFrame: Filtered movies sorted by runtime.
    """

    try:
        filtered_df = df[
            df['cast'].str.contains("Uma Thurman", case=False, na=False) &
            df['director'].str.contains("Quentin Tarantino", case=False, na=False)
        ].sort_values(by='runtime', ascending=True)

        return filtered_df

    except Exception as e:
        logging.error(f"uma_thurman_tarantino_movies failed: {e}")
        return pd.DataFrame()



def most_successful_franchises(df):
    """
    Compute performance metrics for movie franchises.

    Args:
        df (pd.DataFrame): Analysis-ready movie dataset.

    Returns:
        pd.DataFrame: Franchise-level aggregated statistics.
    """
    try:
        data = df.copy()
        data['collection_name'] = data['belongs_to_collection']
        franchise_df = data[data['collection_name'].notna()]

        franchise_stats = franchise_df.groupby('collection_name').agg(
            total_movies=('id', 'count'),
            total_budget=('budget_musd', 'sum'),
            mean_budget=('budget_musd', 'mean'),
            total_revenue=('revenue_musd', 'sum'),
            mean_revenue=('revenue_musd', 'mean'),
            mean_rating=('vote_average', 'mean')
        ).sort_values(by='mean_revenue', ascending=False)

        return franchise_stats

    except Exception as e:
        logging.error(f"most_successful_franchises failed: {e}")
        return pd.DataFrame()
