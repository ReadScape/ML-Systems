from load_data import load_data
from popular_fanfic import request_popular_content
from fanfic_recsys import request_fanfic_recommendation
from fanfic_CF import request_fanfic_CF
import warnings
warnings.filterwarnings('ignore')

def main(is_popular_content, is_recommendation_system, url_rating, 
         url_fiction, model_path, user_id, time_range=None, genre=None
         ):
    """
    Executes the main functionality of the Fanfiction Recommendation System.

    Parameters:
    - is_popular_content (bool): Flag indicating whether to display popular fanfiction content.
    - is_recommendation_system (bool): Flag indicating whether to use the recommendation system.
    - url_rating (str): URL of the rating data.
    - url_fiction (str): URL of the fanfiction data.
    - model_path (str): Path to the collaborative filtering model.
    - user_id (int): User ID for personalized recommendations.
    - time_range (str, optional): Time range for popular content. Defaults to None.
    - genre (str, optional): Genre for fanfiction recommendations. Defaults to None.
    """
    rating_data, _ = load_data(url_rating, url_fiction)

    # For 'Most Popular Fanfiction' Feature
    if is_popular_content:
        request_popular_content(url_rating, url_fiction, time_range)

    # For 'FYP Fanfiction' Feature
    if is_recommendation_system:
        if rating_data[rating_data['user_id'] == user_id].shape[0] < 5: # Cold start
            # Use our custom RecSys
            request_fanfic_recommendation(url_rating, url_fiction, genre)
        else: # Probably ready to use the CF model
            # Collaborative Filtering Recommendations using the model
            request_fanfic_CF(url_rating, url_fiction, model_path, user_id, genre)


# run main function
if __name__ == "__main__":
    is_popular_content = False  # Set to True for popular content
    is_recommendation_system = True  # Set to True for recommendation system
    url_rating = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQwAbiu8ldvpGWuIZtrx_QFzFZ_SvXAxLdbhmNg5lyxiflfNmzm94Ie3mJioEumkslTXOP_d-WuwNfX/pub?output=csv'
    url_fiction = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT2u8napMK0lNviIL48m4jUiqtLezC2KlI61HWr5ekunHYVYYbNJKfP_4PptUgr7ZYwz_z1ozC9mfzh/pub?output=csv'
    model_path = 'CF_DL_model_V0.1.h5'
    user_id = 5
    # set the desired time range: 'weekly', 'monthly', 'yearly', or None (all time)
    time_range = None
    # set the desired genre: 
    """
    'fantasi', 'romansa', 'petualangan', 'drama', 'sci-fi', 'slice of life', 'aksi',
    'misteri', 'komedi', 'horor', 'spiritual', 'non-fiksi', 'kesehatan'
    """
    genre = None

    main(
        is_popular_content,
        is_recommendation_system,
        url_rating,
        url_fiction,
        model_path,
        user_id,
        time_range,
        genre
    )
