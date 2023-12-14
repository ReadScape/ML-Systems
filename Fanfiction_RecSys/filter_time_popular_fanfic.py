import pandas as pd

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

    filtered_df = df[df['created_at'] >= start_date] # filter by start date
    return filtered_df