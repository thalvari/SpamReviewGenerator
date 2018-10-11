import pandas as pd

from model_creator.POSifiedNewLineText import POSifiedNewLineText


class Generator:

    def __init__(self, review_type, rating, state_size, n_reviews, output_format):
        self.review_type = review_type
        self.rating = rating
        self.state_size = state_size
        self.n_reviews = n_reviews
        self.output_format = output_format
        self.model = None

    def load_model(self):
        file = open('models/{}_{}_{}.json'.format(self.review_type, self.rating, self.state_size))
        self.model = POSifiedNewLineText.from_json(file.read())
        file.close()

    def generate_output(self):
        output_df = pd.DataFrame([self.__generate_sentence() for _ in range(self.n_reviews)], columns=['text'])
        output_df['rating'] = self.rating
        path = 'generated_datasets/{}_{}_{}_{}.{}'.format(self.review_type, self.rating, self.state_size,
                                                          self.n_reviews, self.output_format)
        if self.output_format is None:
            print('\n'.join(output_df['text']))
        elif self.output_format == 'csv':
            output_df.to_csv(path)
        elif self.output_format == 'txt':
            f = open(path, 'w')
            f.write('. '.join(output_df['text']))
            f.close()
        self.__print_statistics(output_df)

    def __generate_sentence(self):
        if self.model is None:
            return None
        sentence = str(self.model.make_sentence(tries=100, max_words=25))
        sentence = self.__postprocess_sentence(sentence)
        return sentence

    def __postprocess_sentence(self, sentence):
        sentence = sentence.replace(' \'', '\'')
        sentence = sentence.replace(' - ', '-')
        sentence = sentence.replace(' n\'t', 'n\'t')
        sentence = sentence.replace(' nt ', 'nt ')
        sentence = sentence.replace(' ll ', 'll ')
        sentence = sentence.replace(' ve ', 've ')
        sentence = sentence.replace('i m ', 'im ')
        return sentence

    def __print_statistics(self, output_df):
        print('\nStatistics: ')
        print('{}/{} unique.'.format(output_df['text'].nunique(), output_df.shape[0]))
