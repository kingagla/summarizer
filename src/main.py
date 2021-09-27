import json
import os
import pandas as pd
from download_data import download_articles
from data_analysis.DataAnalizer import DataAnalyser

# TODO find reason for error, start modelling part

def main():
    # define variables
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 380
    path_to_articles = '../data/articles/'
    articles_list = os.listdir(path_to_articles)
    n_articles = len(articles_list)
    stopwords = pd.read_csv('../data/polish_stopwords.txt', names=['stopwords'], dtype={'stopwords': str})
    articles = map(lambda x: json.load(open(os.path.join(path_to_articles, x), 'r')), articles_list)
    plot_directory = '../plots'

    # # download articles
    # download_articles(url_, n_pages_, path_to_articles)

    # analyse downloaded data
    DataAnalyser(articles, stopwords, plot_directory, n_articles)


if __name__ == '__main__':
    main()