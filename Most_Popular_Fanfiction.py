import pandas as pd
import requests
import io

import warnings
warnings.filterwarnings('ignore')


def preprocess_rating(rating):
    """
    Preprocesses the rating dataframe by converting specific columns to integer type

    dataset header: user_id, fiction_id, click, like, rating
    
    Args:
        rating (DataFrame): The rating dataframe to be preprocessed.
        
    Returns:
        DataFrame: The preprocessed rating dataframe.
    """
    rating['user_id'] = rating['user_id'].astype(int)        # user_id to int 
    rating['fiction_id'] = rating['fiction_id'].astype(int)  # fiction_id to int
    rating['click'] = rating['click'].astype(int)            # click to int
    rating['like'] = rating['like'].astype(int)              # like to int
    rating['rating'] = rating['rating'].astype(int)          # rating to int
    return rating

def preprocess_fiction(fiction):
    """
    Preprocesses the given fanfiction data

    dataset header: fiction_id, title, overview, language, release_date, latest_update, tags, genres, chapter

    Args:
        fiction (pandas.DataFrame): The fanfiction data to be preprocessed.

    Returns:
        pandas.DataFrame: The preprocessed fanfiction data.
    """    
    fiction['fiction_id'] = fiction['fiction_id'].astype(int)   # fiction_id to int
    fiction['title'] = fiction['title'].astype(str)             # title to str
    fiction['release_date'] = pd.to_datetime(fiction['release_date'])  # release_date to datetime
    return fiction

def filter_by_time(df, time_range):
    """
    Filter a DataFrame based on a specified time range.

    Parameters:
    df (DataFrame): The DataFrame to be filtered.
    time_range (str): The time range to filter by. Valid options are 'weekly', 'monthly', 'yearly', or 'all'.

    Returns:
    DataFrame: The filtered DataFrame.
    """
    today = pd.Timestamp('today')
    if time_range == 'weekly': # this week most popular fanfiction
        start_date = today - pd.DateOffset(weeks=1)
    elif time_range == 'monthly': # this month most popular fanfiction
        start_date = today - pd.DateOffset(months=1)
    elif time_range == 'yearly': # this year most popular fanfiction
        start_date = today - pd.DateOffset(years=1)
    else:
        return df  # all time most popular fanfiction

    filtered_df = df[df['release_date'] >= start_date] # filter by start date
    return filtered_df

def request_popular_content(time_range=None):
    """
    Requests and processes popular fanfiction content.

    Args:
        time_range (str, optional): Time range to filter the fanfiction data 
        by time period (weekly, monthly, yearly). Defaults to None = all time.

    Returns:
        str: JSON representation of the top 20 popular fanfictions based on click count.
    """
    # URL datasets
    url_rating = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQwAbiu8ldvpGWuIZtrx_QFzFZ_SvXAxLdbhmNg5lyxiflfNmzm94Ie3mJioEumkslTXOP_d-WuwNfX/pub?output=csv'
    url_fiction = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT2u8napMK0lNviIL48m4jUiqtLezC2KlI61HWr5ekunHYVYYbNJKfP_4PptUgr7ZYwz_z1ozC9mfzh/pub?output=csv'

    # request data
    rating_content = requests.get(url_rating).content
    fiction_content = requests.get(url_fiction).content

    # read data
    rating = pd.read_csv(io.StringIO(rating_content.decode('utf-8')))
    fiction_metadata = pd.read_csv(io.StringIO(fiction_content.decode('utf-8')))
    fiction = fiction_metadata[['fiction_id', 'title', 'release_date']]

    # preprocess data
    rating = preprocess_rating(rating)
    fiction = preprocess_fiction(fiction)

    # merge data
    fanfiction_data = fiction.merge(rating, how='inner', on='fiction_id')

    # filter data by time period
    filtered_fiction_data = filter_by_time(fanfiction_data, time_range)

    # group by fiction_id and sum the click column
    fiction_grouped = filtered_fiction_data.groupby('fiction_id')['click'].sum().reset_index()

    # sort descending by click count
    fiction_sorted = fiction_grouped.sort_values(by='click', ascending=False)

    # return top 20 fiction_id in JSON
    return print(fiction_sorted[['fiction_id']].head(20).to_json()) # hilangkan print

# run main function
request_popular_content(time_range=None) # choose time_range: 'weekly', 'monthly', 'yearly', or None (all time)