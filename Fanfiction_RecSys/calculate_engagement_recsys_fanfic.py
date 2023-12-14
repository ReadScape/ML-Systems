import pandas as pd

def calculate_engagement(fanfic_data):
    """
    Calculate the engagement score for each fiction_id based on total clicks, likes, and ratings > 3 counts.

    Parameters:
    fanfic_data (DataFrame): The input DataFrame containing fanfiction data.

    Returns:
    DataFrame: A DataFrame containing the 'fiction_id' and 'Total' engagement score for each fiction_id.
    """
    # Get total clicks, likes, and ratings (> 3) for fiction_id
    total_clicks = fanfic_data.groupby('fiction_id')['click'].sum().nlargest(5)
    total_likes = fanfic_data.groupby('fiction_id')['love'].sum().nlargest(10)
    count_rating = fanfic_data[fanfic_data['rating'] > 3].groupby('fiction_id').size().sort_values(
        ascending=False)

    # Concat and calculate Total
    combined_data = pd.concat([count_rating, total_likes, total_clicks], axis=1).fillna(0)
    combined_data['Total'] = combined_data.sum(axis=1)

    # Sort based on the Total value
    combined_data = combined_data.sort_values(by='Total', ascending=False)

    # Return 'fiction_id' and 'Total'
    return combined_data[['Total']].reset_index()[['fiction_id', 'Total']]