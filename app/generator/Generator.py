from markovify import NewlineText


class Generator:

    def __init__(self):
        self.model = None

    def load_model(self, exported_model, rating, state_size):
        file = open(exported_model.path.format(rating, state_size))
        self.model = NewlineText.from_json(file.read())
        file.close()

    def generate_review(self):
        if self.model is None:
            return None
        return str(self.model.make_sentence(tries=1000, max_words=25))
