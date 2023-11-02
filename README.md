# < For the Progress of Machine Learning Part of READSCAPE >
There are 3 parts of Machine Learning:
1. Content Based Recommendation System
2. Colaborative Based Recommendation System
3. Plagiarism Checker System

## Content Based Recommendation System
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
* System can show how much line are copy-pasted or has high similarity (threshold = 0.9999, 0.7, 0.3)
* System has been designed to show which text are plagiarized and which text are save to be uploaded by Author

Next progress:
* Similarity threshold may be changed depending on the format and type of text
* Try implementing a Neural Network into the system

![image](https://github.com/ReadScape/ML-Thingy/assets/141800409/a2a3b058-3c77-4aaf-a247-2ece1dbebd99)
