import json
import logging
import os

import multiprocessing as mp
import numpy as np

from src import nlp
from src.utils import create_directory, save_statistical_summary

pool = mp.Pool(mp.cpu_count())


def main():
    logging.info(f"\n{'=' * 100}\nprocess started")
    # define variables
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 50
    path_to_articles = '../data/articles'
    articles_list = os.listdir(path_to_articles)
    articles_list = np.random.choice(articles_list, size=1_000)
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
    statistical_directory = os.path.join(os.path.dirname(path_to_articles), 'statistical_summaries')
    create_directory(statistical_directory)
    print('Saving statistical summaries...')
    args = zip(articles, [statistical_directory] * n_articles, articles_list, range(n_articles))
    pool.starmap_async(save_statistical_summary, args).get()
    pool.close()

    logging.info(f"\nprocess finished\n{'=' * 100}")


if __name__ == '__main__':
    main()
