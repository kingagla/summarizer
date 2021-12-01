import json
import logging
import os

from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast, BartConfig, \
    BertTokenizer, BertConfig, BertModel

from src import time_counter
from src.configs import *
from src.data_analysis.data_analysis import DataAnalyser
from src.data_analysis.summary_comparison import generate_excel_with_comparison
from src.download_data.download_articles import download_articles
from src.modelling.bart_summarizer import BARTAbstractiveSummarizer
from src.modelling.bert_summarizer import BERTExtractiveSummarizer
from src.modelling.statistical_summarizer import StatisticalSummarizer
from src.utils import generate_summaries


def full_data_analysis(articles_list, stopwords, plot_directory, articles_directory):
    articles = map(lambda x: json.load(open(os.path.join(articles_directory, x), 'r')), articles_list)
    n_articles = len(articles_list)

    analyser = DataAnalyser(articles, stopwords, plot_directory, n_articles)
    analyser.plot_word_freq()
    analyser.plot_histogram('both')
    analyser.plot_histogram('words')
    analyser.plot_histogram('sentences')
    analyser.save_statistics()


def generate_statistical_summary(articles_list):
    summary_type = statistical_folder
    # define args
    articles = map(lambda x: json.load(open(os.path.join(main_data_directory, articles_folder, x), 'r')), articles_list)
    n_articles = len(articles_list)
    statistical_directory = os.path.join(main_data_directory, summary_type)
    args = zip(articles, [statistical_directory] * n_articles, articles_list, range(n_articles),
               [StatisticalSummarizer] * n_articles)

    # generate summaries
    generate_summaries(main_data_directory, summary_type, args)


def generate_extractive_bert_summary(articles_list):
    summary_type = bert_folder
    # define args
    articles = map(lambda x: json.load(open(os.path.join(main_data_directory, articles_folder, x), 'r')), articles_list)
    n_articles = len(articles_list)
    extractive_bert_directory = os.path.join(main_data_directory, summary_type)

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
    generate_summaries(main_data_directory, summary_type, args, **kwargs)


def generate_abstractive_bart_summary(articles_list):
    summary_type = bart_folder
    # define args
    articles = map(lambda x: json.load(open(os.path.join(main_data_directory, articles_folder, x), 'r')), articles_list)
    n_articles = len(articles_list)
    abstractive_bart_directory = os.path.join(main_data_directory, summary_type)

    # Load model, model config and tokenizer via Transformers
    model_dir = "../models/BART"
    config = BartConfig.from_pretrained(os.path.join(model_dir, "config.json"))
    tokenizer = PreTrainedTokenizerFast(tokenizer_file=os.path.join(model_dir, "tokenizer.json"))
    model = BartForConditionalGeneration.from_pretrained(model_dir, config=config)
    kwargs = {'config': config, 'tokenizer': tokenizer, 'model': model}

    args = zip(articles, [abstractive_bart_directory] * n_articles, articles_list, range(n_articles),
               [BARTAbstractiveSummarizer] * n_articles)

    # generate summaries
    generate_summaries(main_data_directory, summary_type, args, **kwargs)


@time_counter
def main():
    logging.info(f"process started\n{'=' * 100}")

    # # download articles
    logging.info(f'Downloading articles - {n_pages_} pages')
    articles_directory = os.path.join(main_data_directory, articles_folder)
    download_articles(url_, n_pages_, articles_directory)
    articles_list = [file for file in os.listdir(articles_directory) if file.endswith('.json')]

    # analyse downloaded data
    full_data_analysis(articles_list, stopwords, plot_directory, main_data_directory)

    # statistical summary
    print('Saving statistical summaries...')
    logging.info(f"Saving statistical summaries...\n{'=' * 100}")
    generate_statistical_summary(articles_list)
    # logging.info("")

    # extractive
    print('Saving extractive BERT summaries...')
    logging.info(f"Saving extractive BERT summaries...\n{'=' * 100}")
    generate_extractive_bert_summary(articles_list)

    # abstractive BART
    print('Saving abstractive BART summaries...')
    logging.info(f"Saving abstractive BART summaries...\n{'=' * 100}")
    generate_abstractive_bart_summary(articles_list)
    logging.info(f"process finished\n{'=' * 100}\n{'=' * 100}")

    # comparison
    pretrained_model = "dkleczek/bert-base-polish-cased-v1"
    config = BertConfig.from_pretrained(pretrained_model)
    tokenizer = BertTokenizer.from_pretrained(pretrained_model)
    model = BertModel.from_pretrained(pretrained_model, config=config)
    generate_excel_with_comparison(os.path.join(main_data_directory, 'comparison'), tokenizer, model)


if __name__ == '__main__':
    main()
