from markovify import NewlineText

from app.generator.Preprocessor import Preprocessor


class Generator:

    def __init__(self):
        self.preprocessor = Preprocessor()
        self.current_dataset = None
        self.current_rating = -1
        self.model = None

    def load_dataset(self, dataset):
        self.preprocessor.load_dataset(dataset)
        self.preprocessor.process_dataset()
        self.current_dataset = dataset
        self.current_rating = -1

    def generate_review(self, rating, n_sentences=1):
        if self.current_dataset is None or rating not in range(1, 6) or n_sentences < 1:
            return None
        elif rating != self.current_rating:
            text = '\n'.join(
                [sentence for sentence in self.preprocessor.reviews.query('rating == {}'.format(rating))['sentence']])
            self.model = NewlineText(text)
            self.current_rating = rating

        return '. '.join([str(self.model.make_sentence(max_overlap_ratio=0.3, tries=100, max_words=20)) for i in
                          range(0, n_sentences)])
