from load_data import load_data
from prep_data import preprocess_data
from filter_time_popular_fanfic import filter_by_time

def request_popular_content(url_rating, url_fiction, time_range=None):
    """
    Requests popular fanfiction content based on ratings and fiction data.

    Args:
        url_rating (str): The URL of the rating data.
        url_fiction (str): The URL of the fiction data.
        time_range (str, optional): The time range to filter the fanfiction data. Defaults to None.

    Returns:
        str: The JSON representation of the top 20 popular fanfictions.
    """

    # Load data
    rating, fiction = load_data(url_rating, url_fiction)

    # Preprocess data
    rating, fiction = preprocess_data(rating, fiction)

    # Merge data
    fanfic_data = fiction.merge(rating, how='outer', on='fiction_id')

    # Filter by time
    if time_range:
        fanfic_data = filter_by_time(fanfic_data, time_range)

    # Calculate total click & sort descending
    fiction_grouped = fanfic_data.groupby('fiction_id')['click'].sum().reset_index()
    fiction_sorted = fiction_grouped.sort_values(by='click', ascending=False)

    return print(fiction_sorted[['fiction_id']].head(20).to_json())