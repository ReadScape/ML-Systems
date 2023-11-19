import string
import re
import pandas as pd
import sys

import warnings
warnings.filterwarnings('ignore')

def preprocess_post(post):
    post['user_id'] = post['user_id'].astype(int)
    post['post_id'] = post['post_id'].astype(int)
    post['post'] = post['post'].astype(str)
    post['tags'] = post['tags'].astype(str)
    return post

def preprocess_interaction(interaction):
    interaction['user_id'] = interaction['user_id'].astype(int)
    interaction['post_id'] = interaction['post_id'].astype(int)
    interaction['like'] = interaction['like'].astype(int)
    interaction['comment'] = interaction['comment'].astype(int)
    interaction['share'] = interaction['share'].astype(int)
    return interaction

def preprocess_text(text):
    text = text.split(',')
    text = [re.sub(r'\(.*?\)', '', t) for t in text]
    text = [t.translate(str.maketrans('','', string.punctuation)).lower() for t in text]
    text = [t.translate(str.maketrans('','', string.digits)) for t in text]
    return ' '.join(text)

def preprocess_tags(tags):
    tags['user_id'] = tags['user_id'].astype(int)
    tags['tags'] = tags['tags'].astype(str)
    return tags

def calculate_popularity(post, interaction):
    post_recs = interaction.groupby("post_id").agg({'like': 'sum', 'comment': 'sum', 'share': 'sum'}).reset_index()
    post_recs['popularity'] = post_recs['like'] + post_recs['comment'] + post_recs['share']
    post = pd.merge(post, post_recs, on='post_id')
    return post

def post_recommendation(user_id,post_dir, interaction_dir, tags_dir):
    user_id = int(user_id)
    post = pd.read_json(post_dir)
    interaction = pd.read_json(interaction_dir)
    tags = pd.read_json(tags_dir)

    post = preprocess_post(post)
    interaction = preprocess_interaction(interaction)
    tags = preprocess_tags(tags)

    user_tags = tags[tags['user_id'] == user_id]['tags'].values
    user_tags = [tag.split(',') for tag in user_tags]

    post = calculate_popularity(post, interaction)
    post_sorted = post.sort_values(by='popularity', ascending=False)
    filtered_data = pd.DataFrame(columns=['post_id', 'post', 'popularity'])
    for tags_list in user_tags:
        filtered_posts = post_sorted[post_sorted['tags'].apply(lambda x: any(tag.lower() in x.lower() for tag in tags_list))]
        filtered_data = filtered_data._append(filtered_posts[['post_id', 'post', 'popularity']], ignore_index=True)
    return filtered_data

data = sys.argv[1]
print(post_recommendation(data,post_dir='./json/post_dir_input.json',interaction_dir='./json/interaction_dir_input.json',tags_dir='./json/tags_dir_input.json'))