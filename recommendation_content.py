"""
recommendation_content.py: Recommends fiction based on content similarity with the input title and sorted by popularity.

Args:
    title (str): The title of the fanfiction to be recommended.
    rating_dir (str): The directory of the rating data.
    fiction_dir (str): The directory of the fiction data.

Returns:
    json: The top 10 recommended fanfiction titles.
"""

import string
import re
import pandas as pd
import numpy as np
import sys
import requests
import io

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore')

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

def preprocess_fiction(fiction):
    """
    Preprocesses the fiction data.

    Args:
        fiction (pd.DataFrame): The fiction data.

    Returns:
        pd.DataFrame: The preprocessed fiction data.
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
    Calculates the count_rating, mean_rating, like, click, and popularity based on fiction_id.

    Args:
        rating (pd.DataFrame): The rating data.

    Returns:
        pd.DataFrame: The calculated ratings.
    """
    fiction_recs = rating.groupby("fiction_id").rating.agg(['count','mean'])
    fiction_recs['click'] = rating.groupby("fiction_id").click.agg(['count'])
    fiction_recs['like'] = rating.groupby("fiction_id").like.agg(['count'])
    fiction_recs['popularity'] = fiction_recs['click'] + fiction_recs['like']
    return fiction_recs

def calculate_weighted_mean(fiction, fiction_recs):
    """
    Calculates the weighted mean based on the count_rating, mean_rating, and popularity.

    Args:
        fiction (pd.DataFrame): The fiction data.
        fiction_recs (pd.DataFrame): The calculated ratings.

    Returns:
        pd.Series: The weighted mean values.
    """
    r = fiction['mean']
    v = fiction['count']
    m = fiction['count'].quantile(0.8)
    C = fiction['mean'].mean()
    fiction_recs['weighted_mean'] = (r * v + C * m) / (v + m)
    return fiction_recs['weighted_mean']

def preprocess_rating_pred(fiction, fiction_recs):
    """
    Preprocesses the rating predictions by scaling and calculating the score.

    Args:
        fiction (pd.DataFrame): The fiction data.
        fiction_recs (pd.DataFrame): The calculated ratings.

    Returns:
        pd.DataFrame: The preprocessed rating predictions.
    """
    mm_scaler = MinMaxScaler()
    scaled = mm_scaler.fit_transform(fiction_recs[['popularity', 'weighted_mean']])
    rating_pred = pd.DataFrame(scaled, columns=['popularity', 'weighted_mean'])
    rating_pred.index = fiction['fiction_id']
    rating_pred['score'] = rating_pred['weighted_mean'] * 0.4 + rating_pred['popularity'].astype('float64') * 0.6
    rating_pred_sorted = rating_pred.sort_values(by='score', ascending=False)
    return rating_pred_sorted

def preprocess_text(text):
    """
    Preprocesses the text by removing punctuation, digits, and converting to lowercase.

    Args:
        text (str): The text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """
    text = text.split(',')
    text = [re.sub('\(.*\)', '', t) for t in text]
    text = [t.translate(str.maketrans('','', string.punctuation)).lower() for t in text]
    text = [t.translate(str.maketrans('','', string.digits)) for t in text]
    return ' '.join(text)

def preprocess_content(content_df):
    """
    Preprocesses the content dataframe by applying text preprocessing and merging columns.

    Args:
        content_df (pd.DataFrame): The content dataframe.

    Returns:
        pd.DataFrame: The preprocessed content dataframe.
    """
    content_df['overview'] = content_df['overview'].apply(preprocess_text)
    content_df['language'] = content_df['language'].apply(preprocess_text)
    content_df['tags'] = content_df['tags'].apply(preprocess_text)
    content_df['genres'] = content_df['genres'].apply(preprocess_text)
    content_df['atribute'] = ''
    content_df['atribute'] = content_df[content_df.columns[1:]].apply(lambda x: ' '.join(x), axis=1)
    content_df.set_index(['fiction_id','title'], inplace=True)
    content_df = content_df[['atribute']]
    return content_df

def similar_title(title, fiction):
    """
    Finds the most similar title based on content similarity.

    Args:
        title (str): The input title.
        fiction (pd.DataFrame): The fiction data.

    Returns:
        str: The most similar title.
    """
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(fiction['title_mod'])
    vector_title = vectorizer.transform([title])
    similarity = cosine_similarity(vector_title, tfidf).flatten()
    index = np.argmax(similarity)
    return fiction['title'].iloc[index]

def predict(title, fiction, content_df, similarity_weight, top_n):
    """
    Predicts the top recommended fiction based on content similarity and popularity.

    Args:
        title (str): The input title.
        fiction (pd.DataFrame): The fiction data.
        content_df (pd.DataFrame): The preprocessed content dataframe.
        similarity_weight (float): The weight for content similarity.
        top_n (int): The number of recommendations to return.

    Returns:
        pd.DataFrame: The top recommended fiction.
    """
    data = content_df.reset_index()
    index_movie = data[data['title'] == title].index

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(content_df['atribute'])
    cos_sim = cosine_similarity(tfidf_matrix)
    similarity = cos_sim[index_movie].T

    content_df['similarity'] = pd.DataFrame(similarity, columns=['similarity'])
    content_df['final_score'] = content_df['score']*(1-similarity_weight) + content_df['similarity']*similarity_weight
    content_df_sorted = content_df.sort_values(by='final_score', ascending=False).head(top_n)
    content_df_sorted.set_index('title', inplace=True)
    merged_df = content_df_sorted.merge(fiction, on='fiction_id', how='left')
    
    return merged_df[['fiction_id']]

def cbf_recommendation_with_prediction(title, rating_dir='https://docs.google.com/spreadsheets/d/e/2PACX-1vQwAbiu8ldvpGWuIZtrx_QFzFZ_SvXAxLdbhmNg5lyxiflfNmzm94Ie3mJioEumkslTXOP_d-WuwNfX/pub?output=csv', fiction_dir='https://docs.google.com/spreadsheets/d/e/2PACX-1vT2u8napMK0lNviIL48m4jUiqtLezC2KlI61HWr5ekunHYVYYbNJKfP_4PptUgr7ZYwz_z1ozC9mfzh/pub?output=csv'):
    """
    Generates content-based recommendations with prediction.

    Args:
        title (str): The title of the fanfiction to be recommended.
        rating_dir (str): The directory of the rating data.
        fiction_dir (str): The directory of the fiction data.

    Returns:
        json: The top 10 recommended fanfiction titles.
    """
    rating_dir = requests.get(rating_dir).content
    fiction_dir = requests.get(fiction_dir).content

    rating = pd.read_csv(io.StringIO(rating_dir.decode('utf-8'))) #need adjustment --> change to json
    fiction_metadata = pd.read_csv(io.StringIO(fiction_dir.decode('utf-8'))) #need adjustment --> change to json

    fiction = fiction_metadata[['fiction_id', 'title', 'overview', 'language', 'tags', 'genres', 'chapter']]
    fiction['title_mod'] = fiction["title"].str.replace("[^a-zA-Z0-9 ]", "").str.lower().str.replace("\s+", " ", regex=True)

    rating = preprocess_rating(rating)
    fiction = preprocess_fiction(fiction)

    fiction_recs = calculate_rating(rating)
    fiction = fiction.merge(fiction_recs, how='inner', on='fiction_id')
    fiction['weighted_mean'] = calculate_weighted_mean(fiction, fiction_recs)
    rating_pred_sorted = preprocess_rating_pred(fiction,fiction_recs)

    content_df = fiction[['fiction_id', 'title', 'overview', 'language', 'tags', 'genres', 'chapter']]
    content_df = preprocess_content(content_df)   
    content_df = rating_pred_sorted[:10000].merge(content_df, left_index=True, right_index=True, how='left')
    content_df = content_df.reset_index()

    title = similar_title(title, fiction)
    recommendation = predict(title, fiction, content_df, 0.9, 10)
    return recommendation.to_json()

data = sys.argv[1]
cbf_recommendation_with_prediction(data)
