"""
popular_content_rec.py: generating popular content recommendations based on user ratings and fiction metadata.

Args:
    rating_dir (str): The directory path of the rating data file.
    fiction_dir (str): The directory path of the fiction metadata file.

Returns:
    json: The top 20 popular fiction IDs.
"""

import pandas as pd
import requests
import io

import warnings
warnings.filterwarnings('ignore')

def preprocess_rating(rating):
    """
    Preprocesses the rating data by converting data types to int.

    Args:
        rating (DataFrame): The rating data.

    Returns:
        DataFrame: The preprocessed rating data.
    """
    rating['user_id'] = rating['user_id'].astype(int)
    rating['fiction_id'] = rating['fiction_id'].astype(int)
    rating['click'] = rating['click'].astype(int)
    rating['like'] = rating['like'].astype(int)
    rating['rating'] = rating['rating'].astype(int)
    return rating

def preprocess_fiction(fiction):
    """
    Preprocesses the fiction metadata by converting data types to int and str.

    Args:
        fiction (DataFrame): The fiction metadata.

    Returns:
        DataFrame: The preprocessed fiction metadata.
    """
    fiction['fiction_id'] = fiction['fiction_id'].astype(int)
    fiction['overview'] = fiction['overview'].astype(str)
    fiction['language'] = fiction['language'].astype(str)
    fiction['tags'] = fiction['tags'].astype(str)
    fiction['genres'] = fiction['genres'].astype(str)
    fiction['chapter'] = fiction['chapter'].astype(str)
    return fiction

def calculate_rating(rating):
    """
    Calculates the rating count, rating mean, click count, like count, and popularity based on fiction_id.

    Args:
        rating (DataFrame): The rating data.

    Returns:
        DataFrame: The calculated rating metrics.
    """
    fiction_recs = rating.groupby("fiction_id").rating.agg(['count','mean'])
    fiction_recs['click'] = rating.groupby("fiction_id").click.agg(['count'])
    fiction_recs['like'] = rating.groupby("fiction_id").like.agg(['count'])
    fiction_recs['popularity'] = fiction_recs['click'] + fiction_recs['like']
    return fiction_recs

def request_popular_content(rating_dir='https://docs.google.com/spreadsheets/d/e/2PACX-1vQwAbiu8ldvpGWuIZtrx_QFzFZ_SvXAxLdbhmNg5lyxiflfNmzm94Ie3mJioEumkslTXOP_d-WuwNfX/pub?output=csv', fiction_dir='https://docs.google.com/spreadsheets/d/e/2PACX-1vT2u8napMK0lNviIL48m4jUiqtLezC2KlI61HWr5ekunHYVYYbNJKfP_4PptUgr7ZYwz_z1ozC9mfzh/pub?output=csv'):
    """
    Generates popular content recommendations based on user ratings and fiction metadata.

    Args:
        rating_dir (str, optional): The directory of the rating data file.
        fiction_dir (str, optional): The directory of the fiction metadata file.

    Returns:
        str: The JSON representation of the top 20 popular fiction IDs.
    """
    rating_dir = requests.get(rating_dir).content
    fiction_dir = requests.get(fiction_dir).content

    rating = pd.read_csv(io.StringIO(rating_dir.decode('utf-8')))
    fiction_metadata = pd.read_csv(io.StringIO(fiction_dir.decode('utf-8')))

    fiction = fiction_metadata[['fiction_id', 'title', 'overview', 'language', 'tags', 'genres', 'chapter']]
    fiction['title_mod'] = fiction["title"].str.replace("[^a-zA-Z0-9 ]", "").str.lower().str.replace("\s+", " ", regex=True)

    rating = preprocess_rating(rating)
    fiction = preprocess_fiction(fiction)

    fiction_recs = calculate_rating(rating)

    fiction = fiction.merge(fiction_recs, how='inner', on='fiction_id')
    fiction_sorted = fiction.sort_values(by='popularity', ascending=False)
    return fiction_sorted[['fiction_id']].head(20).to_json()

request_popular_content()
