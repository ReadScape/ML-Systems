# < For the Progress of Machine Learning Part of READSCAPE >
There are 3 parts of Machine Learning:
1. Content Based Recommendation System
2. Colaborative Based Recommendation System
3. Plagiarism Checker System

## Content Based Recommendation System  
The Content Base Recommendation System is a recommendation system used for content search features and post pages. It gives recommendations based on feature content. Recommended content is based on the similarity between the content that is searched for or liked and the content available. The content-based recommendation system used in this application is divided into three categories, including:
### 1. Recommendation content similarity based  
Recommendation content similarity-based (recommendation_content.py) is a recommendation system that recommends fanfiction based on content similarity with entry titles and sorts based on popularity. This recommendation system is used for the content search feature.  
Args:  
* title (str): The title of the fanfiction to be recommended.
* rating_dir (str): The directory of the rating data.
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
## Colaborative Based Recommendation System
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
