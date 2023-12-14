import pandas as pd
from load_data import load_data
from prep_data import preprocess_data
import tensorflow as tf

def request_fanfic_CF(url_rating, url_fiction, model_path, user_id, genre=None):
    """
    Recommends fanfiction based on collaborative filtering.

    Args:
        url_rating (str): The URL or file path of the rating data.
        url_fiction (str): The URL or file path of the fiction data.
        model_path (str): The file path of the trained model.
        user_id (int): The ID of the user for whom recommendations are generated.
        genre (str, optional): The genre to filter the recommendations. Defaults to None.

    Returns:
        str: JSON string containing the top recommended fiction IDs.
    """
    # Load data
    rating_CF, fiction_CF = load_data(url_rating, url_fiction)

    # Preprocess data
    rating_CF, fiction_CF = preprocess_data(rating_CF, fiction_CF)

    # Merger & Fill rating NaN with 0
    fanfic_CF = pd.merge(fiction_CF, rating_CF, on='fiction_id', how='outer')
    fanfic_CF[['click', 'rating']] = fanfic_CF[['click', 'rating']].fillna(0)

    # Map user and item ids
    unique_user_ids = fanfic_CF['user_id'].unique()
    user_id_map = {old_id: new_id for new_id, old_id in enumerate(unique_user_ids)}

    unique_item_ids = fanfic_CF['fiction_id'].unique()
    item_id_map = {old_id: new_id for new_id, old_id in enumerate(unique_item_ids)}

    # Load Model
    loaded_model = tf.keras.models.load_model(model_path)

    # Collaborative Filtering Model Predict
    predicted_ratings = loaded_model.predict([fanfic_CF['user_id'].map(user_id_map), fanfic_CF['fiction_id'].map(item_id_map)])

    #print(predicted_ratings)
    #print(fanfic_CF[['fiction_id', 'rating']])

    # Add predicted ratings to the dataframe
    fanfic_CF['predicted_rating'] = predicted_ratings.round().astype(int)
    #print(fanfic_CF[['fiction_id', 'rating', 'predicted_rating']])

    # Filter by genre and sort by Total
    if genre:
        filtered_data = fanfic_CF[fanfic_CF['tags'].str.contains(genre, case=False, na=False)]
        filtered_data = filtered_data.sort_values(by='predicted_rating', ascending=False)
    else:
        filtered_data = fanfic_CF.sort_values(by='predicted_rating', ascending=False)

    # Filter recommendations with click = NaN
    not_clicked_recommendations = filtered_data[filtered_data['click'] == 0]

    # Display the top recommendations with click = NaN
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', None)
    #pd.set_option('display.max_colwidth', None)

    #print("Top Recommendations for User ID:", user_id)
    #print(not_clicked_recommendations[['user_id', 'fiction_id', 'click', 'rating', 'predicted_rating']].head(20))

    return print(not_clicked_recommendations[['fiction_id']].head(20).to_json())

# Example of calling the function
# for checking
#url_rating = "https://readscape.live/fiction_ratings"
#url_fiction = 'https://readscape.live/fiction'
#model_path = 'CF_DL_model_V0.1.h5'
#user_id = '7bdba0b4-8aeb-11ee-8ba1-42010ab80003'  # Set the desired user_id for recommendations
#genre = None  # set the desired genre: 'fantasy', 'romance', 'adventure', etc.
#request_fanfic_CF(url_rating, url_fiction, model_path, user_id, genre)