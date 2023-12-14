"""
Plagiarism_Checker_System_JSON_ver.py: Checking the content of uploaded work in the case of plagiarism in any form, whether it is accidental or intentional

Args:
    fiction_id (str): the story id of all work in database.
    chapter_id (str): the chapter id of all work in database.
    story (str): the content of the story of all work in database.

Returns:
    final (json): final similarity score and whether the file is safe to be uploaded or not.
    details (json): lines with high similarity and the related works.
"""

import json
import re
import requests
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing.text import Tokenizer

import warnings
warnings.filterwarnings('ignore')

def request(story_url='https://readscape.live/pdftodatabase'):
    """
    Requesting and loading data from database.

    Args:
        story_url (str): url of database.

    Returns:
        story (pd.Dataframe): data loaded from database.
    """
    story = requests.get(story_url)
    story = story.json()
    story = pd.DataFrame(story['data'])
    return story, story_url

def remove(text):
    """
    Cleaning the unnecessary symbols inside the text.

    Args:
        text (str): text to be cleaned.

    Returns:
        words (str): cleaned text.
    """
    pattern = r'[\“\”\‘\’\"\']'
    sub_text = re.sub(pattern, '', text)
    pattern = r'[\-\–\—\/?!_,.()\[\]:;]'
    sub_text = re.sub(pattern, ' ', sub_text)
    token_text = word_tokenize(sub_text)
    words = [word for word in token_text if word]
    words = ' '.join(words)
    return words

def text_list(story_data):
    """
    Creating the text array.

    Args:
        story_data (pd.Dataframe): story texts from database.

    Returns:
        lists (array): list of cleaned texts.
    """
    lists = []
    for _, row in story_data.iterrows():
        list_arr = []
        text_to_line = sent_tokenize(row[-4].lower())
        for text in text_to_line:
            list_arr.append(remove(text))
        lists.append(list_arr)
    return lists

def tokenizing(flat_text,text):
    """
    Tokenizing the texts.

    Args:
        flat_text (array): flatted texts from all story.
        text (array): original array of the texts.

    Returns:
        tokenid (array): tokenized texts.
    """
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(flat_text)
    word_index = tokenizer.word_index
    tokenid = []
    for i in text:
        tokens = tokenizer.texts_to_sequences(i)
        tokenid.append(tokens)
    return tokenid

def vecTfid(flat_text, text):
    """
    Vectorizing the texts.

    Args:
        flat_text (array): flatted texts from all story.
        text (array): original array of the texts.

    Returns:
        vecarr (array): vectorized texts.
    """
    vec = TfidfVectorizer()
    vec.fit(flat_text)
    vecarr = []
    for i in text:
        transform = vec.transform(i).toarray()
        vecarr.append(transform)
    return vecarr

def add_values(story_dict, line_key, values, ori_id, opp_id):
    """
    Creating the similar text lines dictionary.

    Args:
        story_dict (dictionary): the dictionary to be used.
        key (str): text line of the story being checked.
        values (array): array of the text lines from the other story that has high similarity with key line.
        id (array): fiction_id and chapter_id of the other story.

    Returns:
        story_dict (dictionary): the dictionary filled with new values.
    """
    # Define the fiction and chapter id
    ori_fic_id, ori_chap_id = ori_id
    opp_fic_id, opp_chap_id = opp_id

    # Set the dictionary
    story_dict.setdefault(ori_fic_id, {}).setdefault(ori_chap_id, {}).setdefault(line_key, {}).setdefault(opp_fic_id, {}).setdefault(opp_chap_id, [])

    # Adding the lines into each dictionary keys
    for line in values:
        if line not in story_dict[ori_fic_id][ori_chap_id][line_key][opp_fic_id][opp_chap_id]:
            story_dict[ori_fic_id][ori_chap_id][line_key][opp_fic_id][opp_chap_id].append(line)

def count_flag(token1, token2, tf1, tf2, story_dict, text1, text2, ori_id, opp_id):
  """
  Detecting lines with high similarity.

  Args:
      token1 (array): the tokenized array of the story being checked.
      token2 (array): the tokenized array of the other story.
      tf1 (array): the vectorized array of the story being checked.
      tf2 (array): the vectorized array of the other story.
      story_dict (dictionary): the dictionary to be called in add_values function
      text1 (str): text of the story being checked.
      text2 (str): text of the other story.
      id (array): fiction_id and chapter_id of the other story

  Returns:
      plag_tf_token (int): number of lines with similarity >0.35 and <0.9999
      di (int): total number of line in the story being checked.
      hs (int): number of line with vectorized similarity >0.9999
      cp (int): number of line with tokenized similarity >0.9999
  """
  # Defining all necessary flag variables
  plag_tf_token = 0
  di = len(tf1)
  token_cos = []
  cp = 0
  hs = 0

  # Getting the similarity on Tokenized text and Vectorized text
  tf_cos = cosine_similarity(tf1,tf2)
  for i in range(len(token1)):
    cos_line= []
    for j in range(len(token2)):
      cos = len(set(token1[i])&set(token2[j]))/len(list(set(token1[i]+token2[j])))
      cos_line.append(cos)
    token_cos.append(cos_line)

  # Iterating through all the line
  for i in range(di):
    tf = 0

    # For high similarity checking
    if any(vals >= 0.9999 for vals in tf_cos[i]):
      tryis = [index for index, vals in enumerate(tf_cos[i]) if vals >= 0.9999]
      add_values(story_dict, text1[i],[text2[i] for i in tryis], ori_id, opp_id)
      hs+=1
    elif any(0.35 < vals < 0.9999 for vals in tf_cos[i]):
      tryish = [index for index, vals in enumerate(tf_cos[i]) if 0.35 < vals < 0.9999]
      tf = 1

    # For high structure similarity checking
    if any(vals >= 0.9999 for vals in token_cos[i]):
      tryis = [index for index, vals in enumerate(token_cos[i]) if vals >= 0.9999]
      add_values(story_dict, text1[i],[text2[i] for i in tryis], ori_id, opp_id)
      cp+=1
    elif any(0.7 < vals < 0.9999 for vals in token_cos[i]):
      tryis = [index for index, vals in enumerate(token_cos[i]) if 0.7 < vals < 0.9999]
      if tf == 1:
        plag_tf_token += 1
        add_values(story_dict, text1[i],[text2[i] for i in tryis], ori_id, opp_id)
        add_values(story_dict, text1[i],[text2[i] for i in tryish], ori_id, opp_id)
      
  return plag_tf_token, di, hs, cp
    
def main_code(story_data,text_list):
  """
  Main code of the system, checking the newly uploaded story checked against other stories in database.

  Args:
      story_data (pd.DataFrame): Data loaded from database.
      text_list (array): list of cleaned text.

  Returns:
      final (json): final similarity score and whether the file is safe to be uploaded or not.
      details (json): lines with high similarity and the related works.
  """
  # Flattened the text to smooth out the tokenize and vectorize
  flat_text = [line for text in text_list for line in text]

  # Calling the tokenizer and vectorizer function
  tfid = vecTfid(flat_text,text_list)
  token = tokenizing(flat_text,text_list)

  plag_score = 0
  fin_plag_score = 0
  verdict = ""
  YN = 0
  story_dict = {}
  cid = -1

  # Iterating each text to examine the similarity between text
  for j in range(len(token)):
    # Skip chapter text of same story
    if story_data.iloc[cid,1] != story_data.iloc[j,1]:
      plag_ft, di, hs, cp = count_flag(token[cid], token[j], tfid[cid], tfid[j], story_dict, text_list[cid], text_list[j], story_data.iloc[cid,1:3], story_data.iloc[j,1:3])
      plag_score = (plag_ft+(hs+cp)/2)/di
    if plag_score > fin_plag_score:
      fin_plag_score = plag_score

  if fin_plag_score >= 0.3:
    YN = 1
    verdict = "Unfortunately, your plagiarism score has exceeded the maximum percentage. Please revise and try again."
  else:
    YN = 0
    verdict = "Congratulations, your plagiarism score is within safe percentage! You may upload your work!"

  if len(story_dict) == 0:
    add_values(story_dict, '-', '-', story_data.iloc[cid,1:3], ['-', '-'])

  data = [{'ori_fic_id': ori_fic_id, 'ori_chap_id': ori_chap_id, 'ori_line': key, 'opp_fic_id': opp_fic_id, 'opp_chap_id': opp_chap_id, 'sim_line': value}
        for ori_fic_id, chap_id in story_dict.items()
        for ori_chap_id, key_dict in chap_id.items()
        for key, file_dict in key_dict.items()
        for opp_fic_id, chap_dict in file_dict.items()
        for opp_chap_id, value in chap_dict.items()]

  df = pd.DataFrame(data)
  df_e = df.explode('sim_line')
  df_e.reset_index(drop=True, inplace=True)

  final = {'final_plag_score': round(fin_plag_score * 100, 2), 'yes_or_no': YN, 'verdict': verdict,
           'ori_fic_id': story_data.iloc[cid,1], 'opp_fic_id': [id['opp_fic_id'] for id in data]}

  details = df_e.to_json()
  final = json.dumps(final)

  return final, details

def Plagiarism_Checker(data):
    """
    Function to call the main code and post result.

    Args:
        data (pd.DataFrame): data loaded from database.

    Returns:
        show_arr (json): contain final and details json from main code.
    """
    show_arr = main_code(data[0], text_list(data[0]))
    response = requests.post(data[1], data=[show_arr])
    if response.status_code == 200:
        print(response.json)
    return show_arr

Plagiarism_Checker(request())
