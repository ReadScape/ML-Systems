import pandas as pd
import requests
import io
import warnings
warnings.filterwarnings('ignore')

def load_data(url_rating, url_fiction):
    """
    Load data from the given URLs and convert them into DataFrames.

    Parameters:
    url_rating (str): The URL to fetch the rating data.
    url_fiction (str): The URL to fetch the fiction data.

    Returns:
    rating_data (DataFrame): The rating data as a DataFrame.
    fiction_data (DataFrame): The fiction data as a DataFrame.
    """
    # Load data
    rating_content = requests.get(url_rating).json()
    fiction_content = requests.get(url_fiction).json()

    # Convert to DataFrame
    rating_data = pd.DataFrame(rating_content['data'])
    fiction_data = pd.DataFrame(fiction_content['data'])

    rating_data = rating_data[['user_id', 'fiction_id', 'click', 'love', 'rating']]
    fiction_data = fiction_data[['fiction_id', 'title', 'created_at', 'tags']]

    return rating_data, fiction_data

# Check
#url_rating = "https://readscape.live/fiction_ratings"
#url_fiction = "https://readscape.live/fiction"

#rating_data, fiction_data = load_data(url_rating, url_fiction)

# Display the loaded data
#print("Rating Data:")
#print(rating_data)

#print("\nFiction Metadata:")
#print(fiction_data)