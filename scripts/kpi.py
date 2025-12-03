import pandas as pd

def rank_movies(df, column, ascending=False, n=10, condition=None):
    if condition:
        df = df.query(condition)

    return df.sort_values(by=column, ascending=ascending).head(n)


def add_profit_columns(df):
    df['profit'] = df['revenue_musd'] - df['budget_musd']
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    return df
