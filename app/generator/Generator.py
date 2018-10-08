from model_creator.POSifiedNewLineText import POSifiedNewLineText


class Generator:

    def __init__(self):
        self.model = None

    def load_model(self, exported_model, rating, state_size):
        file = open(exported_model.path.format(rating, state_size))
        self.model = POSifiedNewLineText.from_json(file.read())
        file.close()

    def generate_review(self):
        if self.model is None:
            return None
        sentence = str(self.model.make_sentence(tries=100, max_words=25))
        sentence = self.__postprocess_review(sentence)
        return sentence

    def __postprocess_review(self, sentence):
        sentence = sentence.replace(' \'', '\'')
        sentence = sentence.replace(' - ', '-')
        sentence = sentence.replace(' n\'t ', 'n\'t ')
        sentence = sentence.replace(' nt ', 'nt ')
        sentence = sentence.replace(' ll ', 'll ')
        sentence = sentence.replace(' ve ', 've ')
        sentence = sentence.replace('i m ', 'im ')
        return sentence
