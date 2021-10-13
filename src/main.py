import json
import logging
import os

import multiprocessing as mp
import numpy as np

from src import nlp, time_counter
from src.data_analysis.DataAnalizer import DataAnalyser
from src.download_data.download_articles import download_articles
from src.modelling.statistical_summarizer import StatisticalSummarizer
from src.modelling.bert_extractive import BERTExtractiveSummarizer
from src.utils import create_directory, save_summary, generate_summaries
from transformers import AutoConfig, AutoTokenizer, AutoModel, BertTokenizer, BertConfig, BertModel


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
    summary_type = 'statistical_summaries'
    # define args
    articles = map(lambda x: json.load(open(os.path.join(articles_directory, x), 'r')), articles_list)
    n_articles = len(articles_list)
    statistical_directory = os.path.join(os.path.dirname(articles_directory), summary_type)
    args = zip(articles, [statistical_directory] * n_articles, articles_list, range(n_articles),
               [StatisticalSummarizer] * n_articles)

    # generate summaries
    generate_summaries(articles_directory, summary_type, args)


def generate_extractive_bert_summary(articles_list, articles_directory):
    summary_type = 'extractive_bert'
    # define args
    articles = map(lambda x: json.load(open(os.path.join(articles_directory, x), 'r')), articles_list)
    n_articles = len(articles_list)
    extractive_bert_directory = os.path.join(os.path.dirname(articles_directory), summary_type)

    # Load model, model config and tokenizer via Transformers
    pretrained_model = "dkleczek/bert-base-polish-cased-v1"
    config = BertConfig.from_pretrained(pretrained_model)
    config.return_dict = True
    tokenizer = BertTokenizer.from_pretrained(pretrained_model)
    model = BertModel.from_pretrained(pretrained_model, config=config)
    kwargs = {'config': config, 'tokenizer': tokenizer, 'model': model}

    args = zip(articles, [extractive_bert_directory] * n_articles, articles_list, range(n_articles),
               [BERTExtractiveSummarizer] * n_articles)

    # generate summaries
    generate_summaries(articles_directory, summary_type, args, **kwargs)


@time_counter
def main():
    logging.info(f"\n{'=' * 100}\nprocess started")

    # define variables
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 50
    articles_directory = '../data/articles'
    articles_list = os.listdir(articles_directory)
    articles_list = np.random.choice(articles_list, size=20)
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

    # extractive
    print('Saving extractive BERT summaries...')
    generate_extractive_bert_summary(articles_list, articles_directory)
    logging.info(f"process finished\n{'=' * 100}")


if __name__ == '__main__':
    main()
