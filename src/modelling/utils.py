import numpy as np
import torch

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


def get_bert_representation(text, tokenizer, model):
    text = split_text(text)
    representation = []
    for sent in text:
        summary_input = tokenizer.encode(sent)
        summary_output = model(torch.tensor([summary_input])).pooler_output.detach().numpy()
        representation.append(summary_output)
    return np.array(representation).mean(axis=0)
