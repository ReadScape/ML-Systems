import pandas as pd
from load_data import load_data

def preprocess_data(rating, fiction):
    """
    Preprocesses the rating and fiction dataframes by adjusting column names and data types.

    Args:
        rating (DataFrame): The rating dataframe.
        fiction (DataFrame): The fiction dataframe.

    Returns:
        Tuple: A tuple containing the preprocessed rating and fiction dataframes.
    """
    # Check and adjust column names if needed
    if 'user_id' not in rating.columns:
        raise ValueError("The 'user_id' column is not present in the rating DataFrame.")

    rating['user_id'] = rating['user_id'].astype(str)
    rating['fiction_id'] = rating['fiction_id'].astype(str)
    rating['click'] = rating['click'].astype(int)
    rating['love'] = rating['love'].astype(int)
    rating['rating'] = rating['rating'].astype(int)

    fiction['fiction_id'] = fiction['fiction_id'].astype(str)
    fiction['title'] = fiction['title'].astype(str)
    fiction['created_at'] = pd.to_datetime(fiction['created_at'])
    fiction['tags'] = fiction['tags'].astype(str)

    return rating, fiction

# Check
#rating, fiction = load_data(
#    url_rating = "https://readscape.live/fiction_ratings",
#    url_fiction = "https://readscape.live/fiction"
#)

#rating, fiction = preprocess_data(rating, fiction)

# Merge data
#fanfic_data = fiction.merge(rating, how='outer', on='fiction_id')

#print(fanfic_data)