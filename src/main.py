import json
import logging
import os

import multiprocessing as mp
import numpy as np

from src import nlp, time_counter
from src.data_analysis.DataAnalizer import DataAnalyser
from src.download_data.download_articles import download_articles
from src.utils import create_directory, save_statistical_summary

pool = mp.Pool(mp.cpu_count())


def full_data_analysis(articles_list, stopwords, plot_directory, articles_directory):
    articles = map(lambda x: json.load(open(os.path.join(articles_directory, x), 'r')), articles_list)
    n_articles = len(articles_list)

    analyser = DataAnalyser(articles, stopwords, plot_directory, n_articles)
    analyser.plot_word_freq()
    analyser.plot_histogram('both')
    analyser.plot_histogram('words')
    analyser.plot_histogram('sentences')
    analyser.save_statistics()


def generate_statistical_summary(articles_list, articles_directory):
    articles = map(lambda x: json.load(open(os.path.join(articles_directory, x), 'r')), articles_list)
    n_articles = len(articles_list)
    statistical_directory = os.path.join(os.path.dirname(articles_directory), 'statistical_summaries')
    create_directory(statistical_directory)
    args = zip(articles, [statistical_directory] * n_articles, articles_list, range(n_articles))
    pool.starmap_async(save_statistical_summary, args).get()
    pool.close()


@time_counter
def main():
    logging.info(f"\n{'=' * 100}\nprocess started")

    # define variables
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 50
    articles_directory = '../data/articles'
    articles_list = os.listdir(articles_directory)
    articles_list = np.random.choice(articles_list, size=1_000)
    stopwords = nlp.Defaults.stop_words
    plot_directory = '../plots2'

    # # download articles
    # logging.info(f'Downloading articles - {n_pages_} pages')
    # download_articles(url_, n_pages_, articles_directory)

    # # analyse downloaded data
    # full_data_analysis(articles_list, stopwords, plot_directory, articles_directory)

    # statistical summary
    print('Saving statistical summaries...')
    generate_statistical_summary(articles_list, articles_directory)
    logging.info(f"\nprocess finished\n{'=' * 100}")


if __name__ == '__main__':
    main()
