import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
import os
from tqdm import tqdm
import logging
import json


def find_iter(soup, tagname):
    tag = soup.find(tagname)
    while tag is not None:
        yield tag
        tag = tag.find_next(tagname)


def load_page(url, n_pages):
    for page in range(1, n_pages + 1):
        if not n_pages:
            response = requests.get(url)
        else:
            response = requests.get(url + f'/{page}')
        yield BeautifulSoup(response.text, 'lxml')


def main(url, n_pages):
    soups = load_page(url, n_pages)
    i = 0
    for soup in tqdm(soups, total=n_pages):
        iterator = find_iter(soup, 'a')
        for item in iterator:
            try:
                if re.search('\d+[a-z]', item['href']) and item['href'].startswith('/'):
                    current_url = 'https://wiadomosci.wp.pl' + item['href']

                    temp_soup = load_page(current_url, None)

                    title = temp_soup.find('h1').text
                    temp_iterator = find_iter(temp_soup, 'p')
                    text = ''
                    for item in temp_iterator:
                        if len(item.text) < 50:
                            continue
                        text += item.text + '\n'

                    article = {'title': title,
                               'text': text}

                    with open(f'../../data/articles/{i}.json', 'w') as outfile:
                        json.dump(article, outfile)

            except Exception as e:
                print(e)

            finally:
                i += 1


if __name__ == '__main__':
    start = time.time()
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 380
    main(url_, n_pages_)
    print('Exec time', time.time() - start)