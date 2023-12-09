# Fanfiction Recommendation System using Collaborative Filtering

This is a Fanfiction Recommendation System that provides two main features: displaying popular fanfiction content and offering personalized recommendations based on user preferences.

## Features

### 1. Most Popular Fanfiction
- Displays the top 20 most popular fanfictions based on click within a specified time range.
- Time range options include 'weekly', 'monthly', 'yearly', or None (all time)

### 2. Personalized Fanfiction Recommendations
- Utilizes collaborative filtering to provide personalized fanfiction recommendations for a specific user.
- If the user has less than 5 interactions, a custom recommendation system is used. Otherwise, collaborative filtering recommendations are generated.
- Allows filtering recommendations by genre & time range.

## Usage

To use the Fanfiction Recommendation System, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/ReadScape/ML-Thingy.git
    cd ML-Thingy/Fanfiction_RecSys
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script:

    ```bash
    python main.py
    ```

    You can customize the main function's parameters in the script to control the system's behavior.

## Configuration

Modify the `main.py` file to configure the following parameters:

- `is_popular_content`: Set to `True` to display popular fanfiction content.
- `is_recommendation_system`: Set to `True` to use the recommendation system.
- `url_rating`: URL of the rating data. Header: [['user_id', 'fiction_id', 'click', 'like', 'rating']].
- `url_fiction`: URL of the fanfiction data. Header (minimun req): [['fiction_id', 'title', 'release_date', 'genres']].
- `model_path`: Path to the collaborative filtering model.h5
- `user_id`: User ID for personalized recommendations.
- `time_range`: Time range for popular content (options: 'weekly', 'monthly', 'yearly', or `None` for all time).
- `genre`: Genre for fanfiction recommendations (options: 'fantasi', 'romansa', 'petualangan', 'drama', 'sci-fi', 'slice of life', 'aksi', 'misteri', 'komedi', 'horor', 'spiritual', 'non-fiksi', 'kesehatan').

## Example

```python
# Example configuration
is_popular_content = True
is_recommendation_system = True
url_rating = 'https://your-rating-data-url.com'
url_fiction = 'https://your-fiction-data-url.com'
model_path = 'path/to/your/model.h5'
user_id = 5
time_range = 'monthly'
genre = 'romansa'

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
```