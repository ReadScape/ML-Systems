"""
search_recommendation_content.py: Recommends fiction based on content similarity with the input title and sorted by popularity.

Args:
    title (str): The title of the fanfiction to be recommended.
    rating_dir (str): The directory for rating data. Default is 'https://readscape.live/calculatedrating'.
    fiction_dir (str): The directory of the fiction data.

Returns:
    json: The top 10 recommended fanfiction titles.
"""

import string
import re
import pandas as pd
import numpy as np
import requests

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
    rating['fiction_id'] = rating['fiction_id'].astype(str)
    rating['count'] = rating['count'].astype(int)
    rating['mean'] = rating['mean'].astype(float)
    rating['click'] = rating['click'].astype(int)
    rating['love'] = rating['love'].astype(int)
    rating['popularity'] = rating['popularity'].astype(int)
    rating['weighted_mean'] = rating['weighted_mean'].astype(float)
    return rating

def preprocess_fiction(fiction):
    """
    Preprocesses the fiction data.

    Args:
        fiction (pd.DataFrame): The fiction data.

    Returns:
        pd.DataFrame: The preprocessed fiction data.
    """
    fiction['fiction_id'] = fiction['fiction_id'].astype(str)
    fiction['synopsis'] = fiction['synopsis'].astype(str)
    fiction['tags'] = fiction['tags'].astype(str)
    fiction['chapters'] = fiction['chapters'].astype(str)
    return fiction

def preprocess_rating_pred(fiction):
    """
    Preprocesses the rating predictions by scaling and calculating the score.

    Args:
        fiction (pd.DataFrame): The fiction data.

    Returns:
        pd.DataFrame: The preprocessed rating predictions.
    """
    mm_scaler = MinMaxScaler()
    scaled = mm_scaler.fit_transform(fiction[['popularity', 'weighted_mean']])
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
    content_df['synopsis'] = content_df['synopsis'].apply(preprocess_text)
    content_df['tags'] = content_df['tags'].apply(preprocess_text)
    content_df['atribute'] = ''
    content_df['atribute'] = content_df[content_df.columns[1:]].apply(lambda x: ' '.join(map(str, x)), axis=1)
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
    
    return merged_df[['fiction_id','title','tags','synopsis', 'final_score']]

def search_recommendation_content(title, rating_dir='https://readscape.live/calculatedrating', fiction_dir='https://readscape.live/fiction'):
    """
    Searches for book recommendations based on content similarity.

    Args:
        title (str): The input title.
        rating_dir (str): The directory for rating data. Default is 'https://readscape.live/calculatedrating'.
        fiction_dir (str): The directory for fiction data. Default is 'https://readscape.live/fiction'.

    Returns:
        pd.DataFrame: The top recommended fiction.
    """
    rating_dir = requests.get(rating_dir).json()
    fiction_dir = requests.get(fiction_dir).json()

    rating = pd.DataFrame(rating_dir['data'])
    fiction = pd.DataFrame(fiction_dir['data'])

    fiction['title_mod'] = fiction["title"].str.replace("[^a-zA-Z0-9 ]", "").str.lower().str.replace("\s+", " ", regex=True)

    rating = preprocess_rating(rating)
    fiction = preprocess_fiction(fiction)

    fiction = fiction.merge(rating, how='inner', on='fiction_id')
    rating_pred_sorted = preprocess_rating_pred(fiction)

    content_df = fiction[['fiction_id', 'title', 'synopsis', 'tags', 'chapters']]
    content_df = preprocess_content(content_df)   
    content_df = rating_pred_sorted[:10000].merge(content_df, left_index=True, right_index=True, how='left')
    content_df = content_df.reset_index()

    title = similar_title(title, fiction)
    recommendation = predict(title, fiction, content_df, 0.9, 10)
    
    return recommendation.to_json()

#test for title 'golden'
search_recommendation_content('golden')
