"""
calculateRating.py: Calculates the interaction score for each fiction based on the rating data.

Args:
    rating_dir (str): The URL or file path of the rating data.

Returns:
    pd.DataFrame: The calculated interaction scores.
"""

import pandas as pd
import io
import requests

from sklearn.preprocessing import MinMaxScaler

def preprocess_rating(rating):
    """
    Preprocesses the rating data.

    Args:
        rating (pd.DataFrame): The rating data.

    Returns:
        pd.DataFrame: The preprocessed rating data.
    """
    rating['user_id'] = rating['user_id'].astype(int)
    rating['fiction_id'] = rating['fiction_id'].astype(int)
    rating['click'] = rating['click'].astype(int)
    rating['like'] = rating['like'].astype(int)
    rating['rating'] = rating['rating'].astype(int)
    return rating

def calculate_rating(rating):
    """
    Calculates the count_rating, mean_rating, like, click, and popularity based on fiction_id.

    Args:
        rating (pd.DataFrame): The rating data.

    Returns:
        pd.DataFrame: The calculated ratings.
    """
    fiction_recs = rating.groupby("fiction_id").rating.agg(['count','mean'])
    fiction_recs['fiction_id'] = fiction_recs.index
    fiction_recs['click'] = rating.groupby("fiction_id").click.agg(['count'])
    fiction_recs['like'] = rating.groupby("fiction_id").like.agg(['count'])
    fiction_recs['popularity'] = fiction_recs['click'] + fiction_recs['like']
    return fiction_recs

def calculate_weighted_mean(fiction_recs):
    """
    Calculates the weighted mean based on the count_rating, mean_rating, and popularity.

    Args:
        fiction_recs (pd.DataFrame): The calculated ratings.

    Returns:
        pd.Series: The weighted mean values.
    """
    r = fiction_recs['mean']
    v = fiction_recs['count']
    m = fiction_recs['count'].quantile(0.8)
    C = fiction_recs['mean'].mean()
    fiction_recs['weighted_mean'] = (r * v + C * m) / (v + m)
    return fiction_recs['weighted_mean']

def calculate_interaction(rating_dir ='https://docs.google.com/spreadsheets/d/e/2PACX-1vQwAbiu8ldvpGWuIZtrx_QFzFZ_SvXAxLdbhmNg5lyxiflfNmzm94Ie3mJioEumkslTXOP_d-WuwNfX/pub?output=csv'):
    """
    Calculates the interaction score for each fiction based on the rating data.

    Args:
        rating_dir (str): The URL or file path of the rating data.

    Returns:
        pd.DataFrame: The calculated interaction.
    """
    rating_dir = requests.get(rating_dir).content
    rating = pd.read_csv(io.StringIO(rating_dir.decode('utf-8')))

    rating = preprocess_rating(rating)
    fiction_recs = calculate_rating(rating)
    fiction_recs['weighted_mean'] = calculate_weighted_mean(fiction_recs)
    return fiction_recs[['fiction_id','count','mean','click','like','popularity','weighted_mean']].to_json()

calculate_interaction()