import pandas as pd
from load_data import load_data
from prep_data import preprocess_data
from calculate_engagement_recsys_fanfic import calculate_engagement

def request_fanfic_recommendation(url_rating, url_fiction, genre=None):
    """
    Requests fanfiction recommendations based on given ratings and fiction data.

    Args:
        url_rating (str): The URL or file path of the ratings data.
        url_fiction (str): The URL or file path of the fiction data.
        genre (str, optional): The genre to filter the recommendations by. Defaults to None.

    Returns:
        None
    """
    # Load data
    rating_recsys, fiction_recsys = load_data(url_rating, url_fiction)

    # Preprocess data
    rating_recsys, fiction_recsys = preprocess_data(rating_recsys, fiction_recsys)

    # Calculate engagement
    combined_data = calculate_engagement(rating_recsys)

    # Merge dataframes based on 'fiction_id'
    fanfic_recsys = pd.merge(fiction_recsys, rating_recsys, on='fiction_id', how='inner')
    fanfic_recsys = pd.merge(fanfic_recsys, combined_data[['fiction_id', 'Total']], on='fiction_id', how='left')

    # Remove duplicates for 'fiction_id'
    fanfic_recsys = fanfic_recsys.drop_duplicates(subset=['fiction_id'])

    # Filter by genre and sort by Total
    if genre:
        filtered_data = fanfic_recsys[fanfic_recsys['genres'].str.contains(genre, case=False, na=False)]
        filtered_data = filtered_data.sort_values(by='Total', ascending=False)
    else:
        filtered_data = fanfic_recsys.sort_values(by='Total', ascending=False)

    # Display the top recommendations in JSON format
    print(filtered_data[['fiction_id']].head(20).to_json())