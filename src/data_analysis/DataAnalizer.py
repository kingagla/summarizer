import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from tqdm import tqdm

from src.utils import lemmatize_text, create_directory


class DataAnalyser:
    def __init__(self, articles_generator, stopwords, plot_directory, n_articles=None):
        self.stopwords = stopwords
        self._preprocess(articles_generator, total=n_articles)
        create_directory(plot_directory)
        self.plot_directory = plot_directory

    def _preprocess(self, articles_generator, total=None):
        # extract data from texts
        words_amount = []
        sentences_amount = []
        full_text = ''
        for article in tqdm(articles_generator, total=total):
            full_text += article['text']
            words_amount.append(len(article['text'].split()))
            sentences_amount.append(len(article['text'].split('. ')))

        # lowercase texts
        full_text = full_text.lower()
        # remove non-words and numbers
        full_text = re.sub('[^a-ż]', ' ', full_text)
        # remove stop words if provided
        full_text = " ".join([word for word in full_text.split() if word not in self.stopwords.values.flatten()])
        full_text = lemmatize_text(text=full_text)

        self.words_amount, self.sentences_amount, self.full_text = words_amount, sentences_amount, full_text
        return self

    def plot_word_freq(self, n=30):
        # create word counter
        words = Counter()
        words.update(self.full_text)

        # create df containing word frequency
        popular_words, amount = list(zip(*words.most_common()))
        df = pd.DataFrame({'Word': popular_words, 'Amount': amount})

        # plot barplot
        plt.figure(figsize=(20, 10))
        sns.set(font_scale=1.5)
        sns.barplot('Amount', 'Word', data=df.iloc[:n])

        # save plot
        plt.savefig(os.path.join(self.plot_directory, 'most_popular_words.png'), format='png')
        plt.close()

    def plot_histogram(self, attribute, bins=30):
        plt.figure(figsize=(12, 8))
        if attribute == 'both':
            x = self.words_amount
            y = self.sentences_amount
        elif attribute == 'words':
            x = self.words_amount
            y = None
        elif attribute == 'sentences':
            x = self.sentences_amount
            y = None
        else:
            raise AttributeError("attribute should be one of ('both', 'words', 'sentences')")
        file_name = f'{attribute}_hist_{bins}.png'
        sns.histplot(x=x, y=y, cbar=True, cbar_kws=dict(shrink=.75), bins=bins)
        plt.savefig(os.path.join(self.plot_directory, file_name), format='png')
        plt.close()
