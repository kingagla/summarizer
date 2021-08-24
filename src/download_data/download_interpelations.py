import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time


def get_tag(tagname, soup):
    tag = soup.find(tagname)
    while tag is not None:
        yield tag
        tag = tag.find_next(tagname)


def get_interpelation_info(soup):
    i = 0
    for tag in get_tag('td', soup):
        if i == 0:
            i += 1
            continue
        try:
            if i % 4 == 1:
                number = int(tag.text)
            elif i % 4 == 3:
                to = tag.text
                to = [item for item in re.split('(?=minister)|(?=prezes)', to.lower()) if item.strip()]
            elif i % 4 == 0:
                web_id = tag.find('a')['href']
                web_id = re.search('(?<=documentId=)\w+', web_id).group(0)

                yield number, to, web_id
        except ValueError as e:
            continue
        finally:
            i += 1


def main():
    url = "https://www.sejm.gov.pl/sejm7.nsf/interpelacje.xsp"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for i in get_interpelation_info(soup):
        print(i)


if __name__ == '__main__':
    main()

