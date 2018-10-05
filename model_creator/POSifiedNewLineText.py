import spacy
from markovify import NewlineText

nlp = spacy.load("en")


class POSifiedNewLineText(NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
