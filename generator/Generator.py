import pandas as pd

from model_creator.POSifiedNewLineText import POSifiedNewLineText


class Generator:

    def __init__(self, category, rating, state_size, output_type):
        self.category = category
        self.rating = rating
        self.state_size = state_size
        self.output_type = output_type
        self.model = None

    def load_model(self):
        file = open('models/{}_{}_{}.json'.format(self.category, self.rating, self.state_size))
        self.model = POSifiedNewLineText.from_json(file.read())
        file.close()

    def generate_output(self, n_sentences):
        output_df = pd.DataFrame([self.__generate_sentence() for _ in range(n_sentences)], columns=['text'])
        output_df['rating'] = self.rating
        output_df = output_df.query('text != "None"')
        path = 'generated_datasets/{}_{}_{}_{}.{}'.format(self.category, self.rating, self.state_size, n_sentences,
                                                          self.output_type)
        if self.output_type is None:
            print('\n'.join(output_df['text']))
        elif self.output_type == 'csv':
            output_df.to_csv(path)
        elif self.output_type == 'txt':
            f = open(path, 'w')
            text = '. '.join(output_df['text'])
            text += '.\n'
            f.write(text)
            f.close()

    def __generate_sentence(self):
        if self.model is None:
            return None
        sentence = str(self.model.make_sentence(tries=10000, max_words=25))
        sentence = self.__postprocess_sentence(sentence)
        return sentence

    def __postprocess_sentence(self, sentence):
        sentence = sentence.replace(' \'', '\'')
        sentence = sentence.replace(' - ', '-')
        sentence = sentence.replace(' n\'t', 'n\'t')
        sentence = sentence.replace(' nt ', 'nt ')
        sentence = sentence.replace(' ll ', 'll ')
        sentence = sentence.replace(' ve ', 've ')
        sentence = sentence.replace(' s ', 's ')
        sentence = sentence.replace('i m ', 'im ')
        return sentence
