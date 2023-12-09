import pandas as pd
import requests
import io
import warnings
warnings.filterwarnings('ignore')

def load_data(url_rating, url_fiction):
    """
    Load data from the given URLs and return the rating and fiction metadata.

    Parameters:
    url_rating (str): The URL of the rating dataset.
    url_fiction (str): The URL of the fiction dataset.

    Returns:
    rating (pd.DataFrame): The rating data.
    fiction_metadata (pd.DataFrame): The fiction metadata with selected columns.
    """

    # Load data from the given URLs
    rating_content = requests.get(url_rating).content
    fiction_content = requests.get(url_fiction).content

    # Convert the content to pandas DataFrame
    rating = pd.read_csv(io.StringIO(rating_content.decode('utf-8')))
    fiction_metadata = pd.read_csv(io.StringIO(fiction_content.decode('utf-8')))

    return rating, fiction_metadata[['fiction_id', 'title', 'release_date', 'genres']] # Columns to used