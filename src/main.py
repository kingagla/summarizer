import json
import logging
import os

import pandas as pd
from download_data import download_articles
from data_analysis.DataAnalizer import DataAnalyser
from src import nlp
from src.modelling.StatisticalSummarizer import StatisticalSummarizer


def main():
    logging.info(f"\n{'=' * 100}\nprocess started\n{'=' * 100}")
    # define variables
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 380
    path_to_articles = '../data/articles/'
    articles_list = os.listdir(path_to_articles)[:10]
    n_articles = len(articles_list)
    stopwords = nlp.Defaults.stop_words
    plot_directory = '../plots2'

    # # download articles
    # logging.info(f'Downloading articles - {n_pages_} pages')
    # download_articles(url_, n_pages_, path_to_articles)

    articles = map(lambda x: json.load(open(os.path.join(path_to_articles, x), 'r')), articles_list)

    # # analyse downloaded data
    # analyser = DataAnalyser(articles, stopwords, plot_directory, n_articles)
    # analyser.plot_word_freq()
    # analyser.plot_histogram('both')
    # analyser.plot_histogram('words')
    # analyser.plot_histogram('sentences')
    # analyser.save_statistics()

    # statistical summary
    for article in articles:
        summary = StatisticalSummarizer(article)
        summary = summary.create_summary()
        print(len(summary), len(summary.split()))


if __name__ == '__main__':
    main()
