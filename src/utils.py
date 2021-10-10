import json
import logging
import os
import morfeusz2
from src import time_counter, nlp
from src.modelling.StatisticalSummarizer import StatisticalSummarizer

def create_directory(directory):
    directory = os.path.abspath(directory).split('/')
    for i in range(2, len(directory) + 1):
        direc = "/".join(directory[:i])
        if not os.path.isdir(direc):
            os.mkdir(direc)


@time_counter
def morf_lemmatize(text):
    if isinstance(text, str):
        text = text.split()
    morf = morfeusz2.Morfeusz(expand_dag=True, expand_tags=True)
    text_new = []
    for word in text:
        w = morf.analyse(word)[0][0][1].split(':')[0]
        text_new.append(w)
    return " ".join(text_new)


def save_statistical_summary(article, directory, filename, counter):
    summary = StatisticalSummarizer(article)
    summary = summary.create_summary()
    title = article['title']
    summary = {'title': title, 'summary': summary}
    with open(os.path.join(directory, filename), 'w') as outfile:
        json.dump(summary, outfile)
    logging.info(f'Element number {counter} in progress...')
