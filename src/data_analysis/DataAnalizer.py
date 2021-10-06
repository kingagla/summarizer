import logging
import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from tqdm import tqdm

from src.utils import morf_lemmatize, create_directory


class DataAnalyser:
    def __init__(self, articles, stopwords, save_directory, n_articles=None):
        self.stopwords = stopwords
        self._preprocess(articles, total=n_articles)
        create_directory(save_directory)
        self.save_directory = save_directory

    def _preprocess(self, articles, total=None):
        # extract data from texts
        words_amount = []
        sentences_amount = []
        full_text = ''
        for article in tqdm(articles, total=total):
            full_text += article['text']
            words_amount.append(len(article['text'].split()))
            sentences_amount.append(len(article['text'].split('. ')))

        # lowercase texts
        logging.info('Texts to lowercase')
        full_text = full_text.lower()
        # remove non-words and numbers
        logging.info('remove non-words and numbers')
        full_text = re.sub('[^a-ż]', ' ', full_text)
        # remove stop words if provided
        logging.info('removing stopwords')
        full_text = " ".join([word for word in full_text.split() if word not in self.stopwords])
        logging.info('lemmatize text')
        full_text = morf_lemmatize(text=full_text)

        self.words_amount, self.sentences_amount, self.full_text = words_amount, sentences_amount, full_text
        return self

    def plot_word_freq(self, n=30):
        # create word counter
        words = Counter()
        words.update(self.full_text.split())

        # create df containing word frequency
        popular_words, amount = list(zip(*words.most_common()))
        df = pd.DataFrame({'Word': popular_words, 'Amount': amount})

        # plot barplot
        plt.figure(figsize=(20, 10))
        sns.set(font_scale=1.5)
        sns.barplot('Amount', 'Word', data=df.iloc[:n])

        # save plot
        plt.savefig(os.path.join(self.save_directory, 'most_popular_words.png'), format='png')
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
        plt.savefig(os.path.join(self.save_directory, file_name), format='png')
        plt.close()

    def save_statistics(self):
        df = pd.DataFrame({'words': self.words_amount, 'sentences': self.sentences_amount})
        df.describe(percentiles=[0, 0.25, 0.5, 0.75, 0.8, 0.9, 0.95, 0.99]).\
            to_excel(os.path.join(self.save_directory, f'statistics.xlsx'))
