import string

import pandas as pd
from nltk.stem import WordNetLemmatizer

from app.generator import Dataset


class Preprocessor:

    def __init__(self):
        self.reviews = None

    def load_dataset(self, dataset):
        if dataset == Dataset.HOTEL:
            self.reviews = pd.read_csv(Dataset.HOTEL.path, index_col=0)
            self.reviews = self.reviews[['reviews.rating', 'language.textcat', 'reviews.text']]
            self.reviews.columns = ['rating', 'language', 'text']
            self.reviews = self.reviews.query('language in ["english", "scots"]')
            self.reviews = self.reviews.drop('language', axis=1)
        elif dataset == Dataset.PREDATOR:
            self.reviews = pd.read_csv(Dataset.PREDATOR.path, index_col=0, encoding="ISO-8859-1")
        # elif dataset == Dataset.CELL:
        #     self.reviews = pd.read_json(Dataset.CELL.path, orient='records', lines=True)
        #     self.reviews = self.reviews[['overall', 'reviewText']]
        #     self.reviews.columns = ['rating', 'text']
        else:
            self.reviews = None
            return

        self.reviews = self.reviews.query('rating in [1, 2, 3, 4, 5]')

    def print_rating_distribution(self):
        print('\n'.join('{}: {}'.format(i, self.reviews.query('rating == {}'.format(i)).shape[0]) for i in range(1, 6)))

    def process_dataset(self):
        punctuation = set(string.punctuation)
        punctuation -= {'.', '!', '?'}
        lemmatizer = WordNetLemmatizer()
        self.reviews['text'] = self.reviews['text'].str.lower()
        self.reviews['text'] = self.reviews['text'].str.replace('\?|!', '.')
        self.reviews['text'] = self.reviews['text'].apply(
            lambda review: ''.join([char for char in review if char not in punctuation]))
        self.reviews = self.reviews.join(
            self.reviews['text'].str.split('.').apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame(
                'sentence'))
        self.reviews = self.reviews.drop('text', axis=1)
        self.reviews['sentence'] = self.reviews['sentence'].apply(
            lambda sentence: " ".join([lemmatizer.lemmatize(word) for word in sentence.split()]))
        self.reviews = self.reviews.query('sentence != ["", "more"]')

    def print_sample_sentences(self, rating, n_reviews=1):
        print('\n'.join(self.reviews.query('rating == {}'.format(rating)).head(n_reviews)['sentence']))
