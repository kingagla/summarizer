import numpy as np
import pandas as pd
import torch
from sklearn.cluster import KMeans
from sklearn.neighbors import DistanceMetric

from src.modelling.utils import split_text


class BERTExtractiveSummarizer:
    """
    Extractive summary creator - uses BERT pooler output to represent each sentence. Uses K-Means algorithm
    to decide which sentences should be a part of the summary
    """

    def __init__(self, article, config, tokenizer, model):
        # article
        self._title = article['title']
        self._text = article['text']

        # define model
        self.config = config
        self.tokenizer = tokenizer
        self.model = model

        # length of sentence representation
        *others, last = model.parameters()
        self.n_features = last.shape[0]

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text

    def encode_text(self):
        encoded_text = []

        for sentence in split_text(self._text):
            input_ = self.tokenizer.encode(sentence)
            output = self.model(torch.tensor([input_])).pooler_output.detach().numpy().reshape((self.n_features,))
            encoded_text.append(output)
        return np.array(encoded_text)

    def _choose_sentences_to_summary(self, n_sentences, metric='euclidean'):
        # encode text
        encoded_text = self.encode_text()

        # predict clusters for sentences
        kmeans = KMeans(n_clusters=n_sentences, random_state=0).fit(encoded_text)
        predicted = kmeans.predict(encoded_text)
        centers = list(map(lambda x: kmeans.cluster_centers_[x], predicted))

        # count distance to centers
        dist = DistanceMetric.get_metric(metric)
        distances = np.diagonal(dist.pairwise(encoded_text, centers))

        temp = pd.DataFrame({'group': predicted, 'distance': distances})
        return temp.groupby('group').idxmin().values.flatten()

    def create_summary(self, n_sentences=4, metric='euclidean'):
        # choose sentences to summary (indices)
        sentences_to_summary = self._choose_sentences_to_summary(n_sentences=n_sentences, metric=metric)
        # split text to sentences
        text = split_text(self._text)
        # choose sentences to summary (text)
        sentences_to_summary = map(text.__getitem__, sentences_to_summary)
        return " ".join(sentences_to_summary)
