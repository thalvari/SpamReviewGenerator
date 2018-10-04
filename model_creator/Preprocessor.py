import string
from ntpath import basename, splitext

import pandas as pd
from markovify import NewlineText
from nltk.stem import WordNetLemmatizer

from model_creator import Dataset


class Preprocessor:

    def __init__(self, dataset, rating, state_size):
        self.dataset = dataset
        self.rating = rating
        self.state_size = state_size
        self.reviews = None
        self.model = None

    def load_and_normalize_dataset(self):
        if self.dataset == Dataset.HOTEL:
            self.reviews = pd.read_csv(Dataset.HOTEL.path, index_col=0)
            self.reviews = self.reviews[['reviews.rating', 'language.textcat', 'reviews.text']]
            self.reviews.columns = ['rating', 'language', 'text']
            self.reviews = self.reviews.query('language in ["english", "scots"]')
            self.reviews = self.reviews.drop('language', axis=1)
        elif self.dataset == Dataset.PREDATOR:
            self.reviews = pd.read_csv(Dataset.PREDATOR.path, index_col=0, encoding="ISO-8859-1")
        elif self.dataset == Dataset.CELL:
            self.reviews = pd.read_json(Dataset.CELL.path, orient='records', lines=True)
            self.reviews = self.reviews[['overall', 'reviewText']]
            self.reviews.columns = ['rating', 'text']

    def print_rating_distribution(self):
        print('\n'.join('{}: {}'.format(i, self.reviews.query('rating == {}'.format(i)).shape[0]) for i in range(1, 6)))

    def create_model(self):
        self.reviews = self.reviews.query('rating == {}'.format(self.rating))
        punctuation = set(string.punctuation)
        punctuation -= {'.', '\''}
        self.reviews['text'] = self.reviews['text'].str.lower()
        self.reviews['text'] = self.reviews['text'].str.replace('\?|!', '.')
        self.reviews['text'] = self.reviews['text'].apply(
            lambda review: ''.join([char for char in review if char not in punctuation]))
        self.__text_to_sentences()
        self.__lemmatize_sentences()
        self.reviews = self.reviews.query('sentence != ["", "more"]')
        text = '\n'.join([sentence for sentence in self.reviews['sentence']])
        self.model = NewlineText(text, state_size=self.state_size)

    def __text_to_sentences(self):
        self.reviews = self.reviews.join(
            self.reviews['text'].str.split('.').apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame(
                'sentence'))

    def __lemmatize_sentences(self):
        lemmatizer = WordNetLemmatizer()
        self.reviews['sentence'] = self.reviews['sentence'].apply(
            lambda sentence: " ".join([lemmatizer.lemmatize(word) for word in sentence.split()]))

    def write_model_to_file(self):
        f = open('models/{}_{}_{}.json'.format(splitext(basename(self.dataset.path))[0], self.rating, self.state_size),
                 'w')
        f.write(self.model.to_json())
        f.close()
