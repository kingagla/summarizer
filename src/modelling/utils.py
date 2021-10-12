from src import nlp


def score_sentence(sentence, words_popularity):
    return sum(map(lambda x: words_popularity.get(x, 0), sentence.split()))


def spacy_lemmatize(text):
    doc = nlp(text)
    yield " ".join([token.lemma_ for token in doc])


def split_text(text):
    text = nlp(text)
    text = text.sents
    return [item.text for item in text]
