"""
popular_post_rec.py: Generates post recommendations for a given user based on their tags and interactions.

Args:
    user_id (int): The user ID.
    post_dir (str): The directory path of the post data file.
    interaction_dir (str): The directory path of the interaction data file.
    tags_dir (str): The directory path of the tags data file.

Returns:
    json: The filtered post recommendations for the user.
"""

import string
import re
import pandas as pd
import sys

import warnings
warnings.filterwarnings('ignore')

def preprocess_post(post):
    """
    Preprocesses the post data by converting data types.

    Args:
        post (pd.DataFrame): The post data.

    Returns:
        pd.DataFrame: The preprocessed post data.
    """
    post['user_id'] = post['user_id'].astype(int)
    post['post_id'] = post['post_id'].astype(int)
    post['post'] = post['post'].astype(str)
    post['post_tags'] = post['post_tags'].astype(str)
    return post

def preprocess_interaction(interaction):
    """
    Preprocesses the interaction data by converting data types.

    Args:
        interaction (pd.DataFrame): The interaction data.

    Returns:
        pd.DataFrame: The preprocessed interaction data.
    """
    interaction['user_id'] = interaction['user_id'].astype(int)
    interaction['post_id'] = interaction['post_id'].astype(int)
    interaction['like'] = interaction['like'].astype(int)
    interaction['comment'] = interaction['comment'].astype(int)
    interaction['share'] = interaction['share'].astype(int)
    return interaction

def preprocess_text(text):
    """
    Preprocesses the text by removing punctuation, digits, and converting to lowercase.

    Args:
        text (str): The text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """
    text = text.split(',')
    text = [re.sub(r'\(.*?\)', '', t) for t in text]
    text = [t.translate(str.maketrans('','', string.punctuation)).lower() for t in text]
    text = [t.translate(str.maketrans('','', string.digits)) for t in text]
    return ' '.join(text)

def preprocess_tags(tags):
    """
    Preprocesses the tags data by converting data types.

    Args:
        tags (pd.DataFrame): The tags data.

    Returns:
        pd.DataFrame: The preprocessed tags data.
    """
    tags['user_id'] = tags['user_id'].astype(int)
    tags['tags'] = tags['tags'].astype(str)
    return tags

def calculate_popularity(post, interaction):
    """
    Calculates the popularity of each post based on interactions.

    Args:
        post (pd.DataFrame): The post data.
        interaction (pd.DataFrame): The interaction data.

    Returns:
        pd.DataFrame: The post data with popularity scores.
    """
    post_recs = interaction.groupby("post_id").agg({'like': 'sum', 'comment': 'sum', 'share': 'sum'}).reset_index()
    post_recs['popularity'] = post_recs['like'] + post_recs['comment'] + post_recs['share']
    post = pd.merge(post, post_recs, on='post_id')
    return post

def post_recommendation(user_id, post_dir, interaction_dir, tags_dir):
    """
    Generates post recommendations for a given user based on their tags and interactions.

    Args:
        user_id (int): The user ID.
        post_dir (str): The directory path of the post data file.
        interaction_dir (str): The directory path of the interaction data file.
        tags_dir (str): The directory path of the tags data file.

    Returns:
        pd.DataFrame: The filtered post recommendations for the user.
    """
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
    filtered_data = pd.DataFrame(columns=['post_id'])
    for tags_list in user_tags:
        filtered_posts = post_sorted[post_sorted['post_tags'].apply(lambda x: any(tag.lower() in x.lower() for tag in tags_list))]
        filtered_data = filtered_data._append(filtered_posts[['post_id']], ignore_index=True)
    return filtered_data.to_json()

data = sys.argv[1]
print(post_recommendation(data, post_dir='./json/post_data.json', interaction_dir='./json/interaction_data.json', tags_dir='./json/user_tags_data.json'))
