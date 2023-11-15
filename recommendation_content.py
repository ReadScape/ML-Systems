#import library
import string
import re
import pandas as pd
import numpy as np
import sys

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore')

#Preprocessing rating data
def preprocess_rating(rating):
    rating['user_id'] = rating['user_id'].astype(int)
    rating['fiction_id'] = rating['fiction_id'].astype(int)
    rating['click'] = rating['click'].astype(int)
    rating['like'] = rating['like'].astype(int)
    rating['rating'] = rating['rating'].astype(int)
    return rating

#Preprocessing rating data
def preprocess_fiction(fiction):
    fiction['fiction_id'] = fiction['fiction_id'].astype(int)
    fiction['overview'] = fiction['overview'].astype(str)
    fiction['language'] = fiction['language'].astype(str)
    fiction['tags'] = fiction['tags'].astype(str)
    fiction['genres'] = fiction['genres'].astype(str)
    fiction['chapter'] = fiction['chapter'].astype(str)
    return fiction

#menghitung count_rating, mean_rating, like, click, dan popularitas berdasarkan fiction_id
def calculate_rating(rating):
    fiction_recs = rating.groupby("fiction_id").rating.agg(['count','mean'])
    fiction_recs['click'] = rating.groupby("fiction_id").click.agg(['count'])
    fiction_recs['like'] = rating.groupby("fiction_id").like.agg(['count'])
    fiction_recs['popularity'] = fiction_recs['click'] + fiction_recs['like']
    return fiction_recs

def calculate_weighted_mean(fiction, fiction_recs):
    r = fiction['mean']
    v = fiction['count']
    m = fiction['count'].quantile(0.8)
    C = fiction['mean'].mean()
    fiction_recs['weighted_mean'] = (r * v + C * m) / (v + m)
    return fiction_recs['weighted_mean']

def preprocess_rating_pred(fiction,fiction_recs):
    mm_scaler = MinMaxScaler()
    scaled = mm_scaler.fit_transform(fiction_recs[['popularity', 'weighted_mean']])
    rating_pred = pd.DataFrame(scaled, columns=['popularity', 'weighted_mean'])
    rating_pred.index = fiction['fiction_id']
    rating_pred['score'] = rating_pred['weighted_mean'] * 0.4 + rating_pred['popularity'].astype('float64') * 0.6
    rating_pred_sorted = rating_pred.sort_values(by='score', ascending=False)
    return rating_pred_sorted

def preprocess_text(text):
    text = text.split(',')
    text = [re.sub('\(.*\)', '', t) for t in text]
    text = [t.translate(str.maketrans('','', string.punctuation)).lower() for t in text]
    text = [t.translate(str.maketrans('','', string.digits)) for t in text]
    return ' '.join(text)

def preprocess_content(content_df):
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
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(fiction['title_mod'])
    vector_title = vectorizer.transform([title])
    similarity = cosine_similarity(vector_title, tfidf).flatten()
    index = np.argmax(similarity)
    return fiction['title'].iloc[index]

def predict(title, fiction, content_df, similarity_weight, top_n):
    
    data = content_df.reset_index()
    index_movie = data[data['title'] == title].index

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(content_df['atribute'])
    tfidf_matrix.shape
    cos_sim = cosine_similarity(tfidf_matrix)
    similarity = cos_sim[index_movie].T

    content_df['similarity'] = pd.DataFrame(similarity, columns=['similarity'])
    content_df['final_score'] = content_df['score']*(1-similarity_weight) + content_df['similarity']*similarity_weight
    content_df_sorted = content_df.sort_values(by='final_score', ascending=False).head(top_n)
    content_df_sorted.set_index('title', inplace=True)
    merged_df = content_df_sorted.merge(fiction, on='fiction_id', how='left')
    
    return merged_df[['fiction_id']]

data = sys.argv[1]

def cbf_recommendation_with_prediction(title, rating_dir='./json/rating.json', fiction_dir='./json/fiction.json'):

    #memuat data rating dan fiction_metadata
    fiction_metadata = pd.read_json(fiction_dir)
    rating = pd.read_json(rating_dir)

    #membuat dataframe fiction
    fiction = fiction_metadata[['fiction_id', 'title', 'overview', 'language', 'tags', 'genres', 'chapter']]
    fiction['title_mod'] = fiction["title"].str.replace("[^a-zA-Z0-9 ]", "").str.lower().str.replace("\s+", " ", regex=True)
    
    #preprocessing data rating dan fiction_metadata
    rating = preprocess_rating(rating)
    fiction = preprocess_fiction(fiction)

    #membuat dataframe fiction_recs untuk menghitung rating count, rating mean, click, like, dan popularity
    fiction_recs = calculate_rating(rating)

    #merge dataframe fiction dengan fiction_recs
    fiction = fiction.merge(fiction_recs, how='inner', on='fiction_id')

    #menghitung weighted_mean dari algoritma hybrid
    fiction['weighted_mean'] = calculate_weighted_mean(fiction, fiction_recs)

    #membuat dataframe rating_pred untuk mengurutkan konten paling populer
    rating_pred_sorted = preprocess_rating_pred(fiction,fiction_recs)

    # Create a content_df
    content_df = fiction[['fiction_id', 'title', 'overview', 'language', 'tags', 'genres', 'chapter']]

    #melakukan preprocess pada content_df
    content_df = preprocess_content(content_df)

    #merge rating_pred dengan content_df
    content_df = rating_pred_sorted[:10000].merge(content_df, left_index=True, right_index=True, how='left')

    #rekomendasi fancition yang paling mirip dan populer
    content_df = content_df.reset_index()

    title = similar_title(title, fiction)
    
    recommendation = predict(title, fiction, content_df, 0.9, 10)

    return recommendation.to_json()

print(cbf_recommendation_with_prediction(data))