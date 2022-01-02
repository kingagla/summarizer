import json
import logging
import multiprocessing as mp
import os
from functools import partial

from src import time_counter


def create_directory(directory):

    if not os.path.isdir(directory):
        print('Creating directory', os.path.abspath(directory))
        directory = os.path.abspath(directory).split('/')
        for i in range(2, len(directory) + 1):
            direc = "/".join(directory[:i])
            if not os.path.isdir(direc):
                os.mkdir(direc)


def save_summary(article, directory, filename, counter, summary_class, **kwargs):
    summary = summary_class(article=article, **kwargs)
    summary = summary.create_summary()
    title = article['title']
    summary = {'title': title, 'summary': summary}
    with open(os.path.join(directory, filename), 'w') as outfile:
        json.dump(summary, outfile)
    logging.info(f'Element number {counter} in progress...')


def generate_summaries(main_directory, summary_type, args, **kwargs):
    directory = os.path.join(main_directory, summary_type)
    create_directory(directory)

    pool = mp.Pool(mp.cpu_count())
    # pool.starmap_async(save_summary, args).get()
    pool.starmap_async(partial(save_summary, **kwargs), args).get()
    pool.close()


def load_json(filepath, *args, **kwargs):
    with open(os.path.join(filepath), 'r') as outfile:
        file = json.load(outfile, *args, **kwargs)
    return file
