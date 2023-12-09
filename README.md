# < For the Progress of Machine Learning Part of READSCAPE >
There are 3 parts of Machine Learning:
1. Content Based Recommendation System
2. Colaborative Based Recommendation System
3. Plagiarism Checker System

## Content Based Recommendation System  
The Content Base Recommendation System is a recommendation system used for content search features and post pages. It gives recommendations based on feature content. Recommended content is based on the similarity between the content that is searched for or liked and the content available. The content-based recommendation system used in this application is divided into three categories, including:
### 1. Recommendation content similarity based  
Recommendation content similarity-based (search_recommendation_content.py) is a recommendation system that recommends fanfiction based on content similarity with entry titles and sorts based on popularity. This recommendation system is used for the content search feature.  
Args:  
* title (str): The title of the fanfiction to be recommended.
* rating_dir (str): The directory of the calculated rating data.
* fiction_dir (str): The directory of the fiction data.

Process:  
* request rating data and fiction data from url
* read rating data and fiction data
* make fiction dataframe
* preprocess rating data and fiction data
* make fiction_recs dataframe by calculating rating, click, like, and popularity
* merge fiction and fiction_recs dataframe
* calculate weighted mean
* preprocess rating prediction by scaling and calculating the score
* preprocess content dataframe by applying text preprocessing and merging columns
* find the most similar title based on content similarity
* predict the top recommended fiction based on content similarity and popularity

Returns:  
* json: the top 10 recommended fanfiction titles
### 2. Recommendation content popularity based  
Recommendation content popularity-based (popular_content_rec.py) is a recommendation system that recommends fanfiction based on popularity. This recommendation system is used to feature the most popular content on content pages.  
Args:  
* rating_dir (str): The directory path of the rating data file.
* fiction_dir (str): The directory path of the fiction metadata file.

Process:  
* request rating data and fiction data from url
* read rating data and fiction data
* make fiction dataframe
* preprocess rating data and fiction data
* make fiction_recs dataframe by calculating rating, click, like, and popularity
* merge fiction and fiction_recs dataframe
* sort the dataframe by popularity
* return the top 20 popular fiction IDs
 
Returns:  
* json: The top 20 popular fiction IDs

### 3. Recommendation post popularity and similarity based  
Recommendation post popularity and similarity-based (popular_post_rec.py) is a recommendation system that recommends fanfiction based on popularity order and filters based on tags that are of interest to users. This recommendation system is used in the posting feature on the posting page.  
Args:  
* user_id (int): The user ID.
* post_dir (str): The directory path of the post data file.
* interaction_dir (str): The directory path of the interaction data file.
* tags_dir (str): The directory path of the tags data file.

Process:  
* request post data, interaction data, and tags data from url
* read post data, interaction data, and tags data
* preprocess post data, interaction data, and tags data
* preprocess user tags by splitting the tags into lists
* calculate popularity of each post based on interactions
* sort the post data by popularity
* filter the post data by tags
* return the filtered post recommendations for the user

Returns:  
* json: The filtered post recommendations for the user.
## Fanfiction Recommendation System using Collaborative Filtering

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

### 2. Recommendation content popularity based  
Recommendation content popularity-based (popular_content_rec.py) is a recommendation system that recommends fanfiction based on popularity. This recommendation system is used to feature the most popular content on content pages.  
Args:  
* rating_dir (str): The directory path of the rating data file.
* fiction_dir (str): The directory path of the fiction metadata file.

Process:  
* request rating data and fiction data from url
* read rating data and fiction data
* make fiction dataframe
* preprocess rating data and fiction data
* make fiction_recs dataframe by calculating rating, click, like, and popularity
* merge fiction and fiction_recs dataframe
* sort the dataframe by popularity
* return the top 20 popular fiction IDs
 
Returns:  
* json: The top 20 popular fiction IDs

### 3. Recommendation post popularity and similarity based  
Recommendation post popularity and similarity-based (popular_post_rec.py) is a recommendation system that recommends fanfiction based on popularity order and filters based on tags that are of interest to users. This recommendation system is used in the posting feature on the posting page.  
Args:  
* user_id (int): The user ID.
* post_dir (str): The directory path of the post data file.
* interaction_dir (str): The directory path of the interaction data file.
* tags_dir (str): The directory path of the tags data file.

Process:  
* request post data, interaction data, and tags data from url
* read post data, interaction data, and tags data
* preprocess post data, interaction data, and tags data
* preprocess user tags by splitting the tags into lists
* calculate popularity of each post based on interactions
* sort the post data by popularity
* filter the post data by tags
* return the filtered post recommendations for the user

Returns:  
* json: The filtered post recommendations for the user.

## Plagiarism Checker System
Plagiarism checker system is a system used to check the originality of the Author's work. To ensure integrity and fairness, we have decided to incorporate this system into our READSCAPE.

Plagiarism checker system has several features:

* System will check any copy-pasted element inside the text
* System will check any sentences with high similarity
* System will decide if the work are save to be uploaded

This system uses several library, such as: tensorflow, os, sklearn, nltk, re, numpy, PyPDF2 and docx.

And also uses available functions, such as: TfidfVectorizer, cosine_similarity, word_tokenize, sent_tokenize, Tokenizer and pad_sequences.

Current progress:
* System can show how much line are copy-pasted or has high similarity (threshold = 0.99, 0.7, 0.3)
* System has been designed to show which text are plagiarized and which text are save to be uploaded by Author

Next progress:
* Similarity threshold may be changed depending on the format and type of text
* Try implementing a Neural Network into the system

![image](https://github.com/ReadScape/ML-Thingy/assets/141800409/a2a3b058-3c77-4aaf-a247-2ece1dbebd99)

[Latest Plagiarism Checker System link](https://colab.research.google.com/drive/1ppuMaEjXKjWd24T_JPt4IWbjVE5O_Uum?usp=sharing) 
