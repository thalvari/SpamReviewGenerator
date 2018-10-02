import string

import markovify
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer

reviews = pd.read_csv('data/7282_with_textcat_languagetags.csv', index_col=0)
reviews = reviews[['reviews.rating', 'language.textcat', 'reviews.text']]
reviews.columns = ['rating', 'language', 'text']
reviews = reviews.query('language in ["english", "scots"]')
reviews = reviews.drop('language', axis=1)
# reviews = pd.read_csv('data/predator.csv', index_col=0, encoding = "ISO-8859-1")

reviews = reviews.query('rating in [1, 2, 3, 4, 5]')
# print('\n'.join('{}: {}'.format(i, reviews.query('rating == {}'.format(i)).shape[0]) for i in range(1, 6)))

nltk.download('wordnet')
punctuation = set(string.punctuation)
punctuation -= {'.', '!', '?'}
lemmatizer = WordNetLemmatizer()
reviews['text'] = reviews['text'].str.lower()
reviews['text'] = reviews['text'].str.replace('\?|!', '.')
reviews['text'] = reviews['text'].apply(
    lambda review: ''.join([char for char in review if char not in punctuation]))
reviews = reviews.join(
    reviews['text'].str.split('.').apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame('sentence'))
reviews = reviews.drop('text', axis=1)
reviews['sentence'] = reviews['sentence'].apply(
    lambda sentence: " ".join([lemmatizer.lemmatize(word) for word in sentence.split()]))
reviews = reviews.query('sentence != ["", "more"]')
# print('\n'.join(reviews.query('rating == 1').head(25)['sentence']))

text = '\n'.join([sentence for sentence in reviews.query('rating == 1')['sentence']])
model = markovify.NewlineText(text)
for i in range(25):
    print(model.make_sentence())
