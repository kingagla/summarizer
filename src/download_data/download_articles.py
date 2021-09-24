import json
import os
import re
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

from src import time_counter
from src.utils import create_directory


# TODO Pobrac morfeusza, zamienic slowo na najprostsza forme i zrobic podsumowanie co najczesciej wystepuje +
#  rozklad dlugosci atrykulow pod wzgledem dlugosci ogolem oraz liczby slow

def find_iter(soup, tagname):
    tag = soup.find(tagname)
    while tag is not None:
        yield tag
        tag = tag.find_next(tagname)


def load_page(url, n_pages):
    for page in range(1, n_pages + 1):
        if n_pages == 1:
            response = requests.get(url)
        else:
            response = requests.get(url + f'/{page}')
        yield BeautifulSoup(response.text, 'lxml')


@time_counter
def main(url, n_pages, saving_directory):
    soups = load_page(url, n_pages)
    i = 0
    for soup in tqdm(soups, total=n_pages):
        iterator = find_iter(soup, 'a')
        for item in iterator:
            try:
                if re.search('\d+[a-z]', item['href']) and item['href'].startswith('/'):
                    current_url = 'https://wiadomosci.wp.pl' + item['href']

                    temp_soup = next(load_page(current_url, 1))

                    title = temp_soup.find('h1').text
                    temp_iterator = find_iter(temp_soup, 'p')
                    text = ''
                    for item in temp_iterator:
                        if len(item.text) < 50:
                            continue
                        text += item.text + '\n'

                    article = {'title': title,
                               'text': text}
                    create_directory(saving_directory)
                    with open(os.path.join(saving_directory, f'{i}.json'), 'w') as outfile:
                        json.dump(article, outfile)

            except Exception as e:
                print(e)

            finally:
                i += 1


if __name__ == '__main__':
    url_ = "https://wiadomosci.wp.pl"
    n_pages_ = 380
    main(url_, n_pages_, '../../data/articles/')
