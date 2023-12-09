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

    # Map user and item ids
    unique_user_ids = rating_CF['user_id'].unique()
    user_id_map = {old_id: new_id for new_id, old_id in enumerate(unique_user_ids)}

    unique_item_ids = rating_CF['fiction_id'].unique()
    item_id_map = {old_id: new_id for new_id, old_id in enumerate(unique_item_ids)}

    # Load Model
    loaded_model = tf.keras.models.load_model(model_path)

    # Collaborative Filtering Model Predict
    predicted_ratings = loaded_model.predict([rating_CF['user_id'].map(user_id_map), rating_CF['fiction_id'].map(item_id_map)])

    # Merge dataframes based on 'fiction_id'
    fanfic_CF = pd.merge(fiction_CF, rating_CF, on='fiction_id', how='inner')

    # Add predicted ratings to the dataframe
    fanfic_CF['predicted_rating'] = predicted_ratings.round().astype(int)

    # Filter by genre and sort by Total
    if genre:
        filtered_data = fanfic_CF[fanfic_CF['genres'].str.contains(genre, case=False, na=False)]
        filtered_data = filtered_data.sort_values(by='predicted_rating', ascending=False)
    else:
        filtered_data = fanfic_CF.sort_values(by='predicted_rating', ascending=False)

    # Filter by user ID and genre, then sort by predicted rating
    recommendations = filtered_data[(fanfic_CF['user_id'] == user_id)]
    recommendations = recommendations.sort_values(by='predicted_rating', ascending=False)

    # Display the top recommendations
    #print("Top Recommendations for User ID:", user_id)
    #print(recommendations[['user_id', 'fiction_id', 'title','rating', 'predicted_rating']].head(20))

    return recommendations[['fiction_id']].head(20).to_json()



# Example of calling the function
# for checking

#url_rating = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQwAbiu8ldvpGWuIZtrx_QFzFZ_SvXAxLdbhmNg5lyxiflfNmzm94Ie3mJioEumkslTXOP_d-WuwNfX/pub?output=csv'
#url_fiction = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT2u8napMK0lNviIL48m4jUiqtLezC2KlI61HWr5ekunHYVYYbNJKfP_4PptUgr7ZYwz_z1ozC9mfzh/pub?output=csv'
#model_path = 'best_NCF_pre-model.h5'
#user_id_to_recommend = 1  # Set the desired user_id for recommendations
#genre = 'kesehatan'  # set the desired genre: 'fantasy', 'romance', 'adventure', etc.

#request_fanfic_CF(url_rating, url_fiction, model_path, user_id_to_recommend, genre)