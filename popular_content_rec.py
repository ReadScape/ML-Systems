import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def preprocess_rating(rating):
    rating['user_id'] = rating['user_id'].astype(int)
    rating['fiction_id'] = rating['fiction_id'].astype(int)
    rating['click'] = rating['click'].astype(int)
    rating['like'] = rating['like'].astype(int)
    rating['rating'] = rating['rating'].astype(int)
    return rating

def preprocess_fiction(fiction):
    fiction['fiction_id'] = fiction['fiction_id'].astype(int)
    fiction['overview'] = fiction['overview'].astype(str)
    fiction['language'] = fiction['language'].astype(str)
    fiction['tags'] = fiction['tags'].astype(str)
    fiction['genres'] = fiction['genres'].astype(str)
    fiction['chapter'] = fiction['chapter'].astype(str)
    return fiction

def calculate_rating(rating):
    fiction_recs = rating.groupby("fiction_id").rating.agg(['count','mean'])
    fiction_recs['click'] = rating.groupby("fiction_id").click.agg(['count'])
    fiction_recs['like'] = rating.groupby("fiction_id").like.agg(['count'])
    fiction_recs['popularity'] = fiction_recs['click'] + fiction_recs['like']
    return fiction_recs

def request_popular_content(rating_dir='./json/rating.json', fiction_dir='./json/fiction.json'):
    rating = pd.read_json(rating_dir)
    fiction_metadata = pd.read_json(fiction_dir)


    fiction = fiction_metadata[['fiction_id', 'title', 'overview', 'language', 'tags', 'genres', 'chapter']]
    fiction['title_mod'] = fiction["title"].str.replace("[^a-zA-Z0-9 ]", "").str.lower().str.replace("\s+", " ", regex=True)
    

    rating = preprocess_rating(rating)
    fiction = preprocess_fiction(fiction)

    fiction_recs = calculate_rating(rating)
    fiction = fiction.merge(fiction_recs, how='inner', on='fiction_id')
    fiction_sorted = fiction.sort_values(by='popularity', ascending=False)
    return fiction_sorted[['fiction_id']].head(20).to_json()

request_popular_content()
