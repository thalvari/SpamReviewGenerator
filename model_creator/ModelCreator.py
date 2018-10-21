import string

import pandas as pd

from model_creator import POSifiedNewLineText


class ModelCreator:

    def __init__(self, category, rating, state_size):
        self.category = category
        self.rating = rating
        self.state_size = state_size
        self.reviews = None
        self.model = None

    def load_and_normalize_dataset(self):
        if self.category == 'hotel':
            self.reviews = pd.read_csv('datasets/hotel.csv', index_col=0)
            self.reviews = self.reviews[['reviews.rating', 'language.textcat', 'reviews.text']]
            self.reviews.columns = ['rating', 'language', 'text']
            self.reviews = self.reviews.query('language in ["english", "scots"]')
            self.reviews = self.reviews.drop('language', axis=1)
        elif self.category == 'marvel':
            self.reviews = pd.read_csv('datasets/marvel.csv', index_col=0, encoding="ISO-8859-1")
        elif self.category == 'cell':
            self.reviews = pd.read_json('datasets/cell.json', orient='records', lines=True)
            self.reviews = self.reviews[['overall', 'reviewText']]
            self.reviews.columns = ['rating', 'text']

    def preprocess_dataset(self):
        self.reviews = self.reviews.query('rating == {}'.format(self.rating))
        self.__preprocess_reviews()
        self.__text_to_sentences()
        self.__remove_punctuation()
        self.__clean_sentences()

    def __preprocess_reviews(self):
        self.reviews['text'] = self.reviews['text'].str.lower()
        self.reviews['text'] = self.reviews['text'].str.replace('a\.m\.', 'am')
        self.reviews['text'] = self.reviews['text'].str.replace('p\.m\.', 'pm')
        self.reviews['text'] = self.reviews['text'].str.replace('\?|!', '.')
        self.reviews['text'] = self.reviews['text'].str.replace('<br/>|http://|www\.|\.com', ' ')

    def __text_to_sentences(self):
        sentences = self.reviews['text'].str.split('.').apply(pd.Series).stack().reset_index(level=1, drop=True)
        self.reviews = self.reviews.join(sentences.to_frame('sentence'))

    def __remove_punctuation(self):
        punctuation = set(string.punctuation)
        punctuation -= {'.', '\'', '%', '-', ':'}
        self.reviews['sentence'] = self.reviews['sentence'].apply(
            lambda sentence: ''.join([char if char not in punctuation else ' ' for char in sentence]))
        self.reviews['sentence'] = self.reviews['sentence'].str.replace('(\W)(\'+|-+)', r'\1 ')
        self.reviews['sentence'] = self.reviews['sentence'].str.replace('(\'+|-+)(\W)', r' \2')
        self.reviews['sentence'] = self.reviews['sentence'].str.replace('(\D):+', r'\1 ')
        self.reviews['sentence'] = self.reviews['sentence'].str.replace(':+(\D)', r' \1')

    def __clean_sentences(self):
        self.reviews['sentence'] = self.reviews['sentence'].apply(
            lambda sentence: " ".join([word for word in sentence.split() if not word.isspace()]))
        self.reviews = self.reviews.query('sentence != ["", "more"]')

    def create_model(self):
        text = '\n'.join([sentence for sentence in self.reviews['sentence']])
        self.model = POSifiedNewLineText(text, state_size=self.state_size)

    def write_model_to_file(self):
        f = open('models/{}_{}_{}.json'.format(self.category, self.rating, self.state_size), 'w')
        f.write(self.model.to_json())
        f.close()

    def write_sample_to_file(self, n_sample):
        n_sample = min(self.reviews.shape[0], n_sample)
        text = '. '.join([sentence for sentence in self.reviews['sentence'].head(n_sample)])
        text += '.\n'
        f = open('datasets/{}_{}_sample_{}.txt'.format(self.category, self.rating, n_sample), 'w')
        f.write(text)
        f.close()
