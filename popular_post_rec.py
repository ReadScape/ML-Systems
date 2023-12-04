"""
popular_post_rec.py: Generates post recommendations for a given user based on their tags and interactions.

Args:
    user_id (int): The user ID.
    post_dir (str): The directory path of the post data file.
    calculate_dir (str): The directory path of the calculated post popularity data file.
    tags_dir (str): The directory path of the tags data file.

Returns:
    json: The filtered post recommendations for the user.
"""

import string
import re
import pandas as pd
import sys
import requests

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
    post['user_id'] = post['user_id'].astype(str)
    post['post_id'] = post['post_id'].astype(str)
    post['post'] = post['post'].astype(str)
    post['post_tags'] = post['post_tags'].astype(str)
    return post

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
    tags['user_id'] = tags['user_id'].astype(str)
    tags['tags'] = tags['tags'].astype(str)
    return tags

def post_recommendation(user_id, post_dir="https://readscape.live/post_data", calculate_dir="https://readscape.live/calcPostPopularity", tags_dir="https://readscape.live/userTagData"):
    """
    Generates post recommendations for a given user based on their tags and interactions.

    Args:
        user_id (int): The user ID.
        post_dir (str): The directory path of the post data file.
        calculate_dir (str): The directory path of the calculated post popularity data file.
        tags_dir (str): The directory path of the tags data file.

    Returns:
        pd.DataFrame: The filtered post recommendations for the user.
    """
    post = requests.get(post_dir).json()
    calculate = requests.get(calculate_dir).json()
    tags = requests.get(tags_dir).json()

    post = pd.DataFrame(post['data'])
    calculate = pd.DataFrame(calculate['data'])
    tags = pd.DataFrame(tags['data'])

    post = preprocess_post(post)
    tags = preprocess_tags(tags)

    user_tags = tags[tags['user_id'] == user_id]['tags'].values
    user_tags = [tag.split('I') for tag in user_tags]

    post = post.merge(calculate[['post_id', 'popularity']], on='post_id', how='left')
    post_sorted = post.sort_values(by='popularity', ascending=False)
    filtered_data = pd.DataFrame(columns=['post_id', 'post', 'post_tags'])
    for tags_list in user_tags:
        filtered_posts = post_sorted[post_sorted['post_tags'].apply(lambda x: any(tag.lower() in x.lower() for tag in tags_list))]
        filtered_data = filtered_data._append(filtered_posts[['post_id', 'post', 'post_tags']], ignore_index=True)
    return filtered_data.to_json()

#test for user_id = 63088bb1-85dd-11ee-a0d6-42010ab80003
print(post_recommendation("63088bb1-85dd-11ee-a0d6-42010ab80003"))
