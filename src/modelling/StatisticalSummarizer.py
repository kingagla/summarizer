import re
from collections import Counter

from src import nlp
from src.modelling.utils import score_sentence
from src.utils import spacy_lemmatize
stopwords = nlp.Defaults.stop_words


class StatisticalSummarizer:

    new_sentence_splitter = '\. (?=[A-ZĆŁŃÓŚŹŻ-])|\n'

    def __init__(self, article):
        self.title = article['title']
        self.text = article['text']
        self.stopwords = stopwords

    @property
    def lemmatized_article(self):
        text = re.split(self.new_sentence_splitter, self.text)
        new_text = ''
        for sentence in text:
            temp_text = next(spacy_lemmatize(sentence))
            temp_text = re.sub('[^a-ż]', ' ', temp_text)
            temp_text = " ".join([word for word in temp_text.split() if word not in stopwords])
            new_text += temp_text + '. '
        return new_text

    @property
    def common_words(self):
        words = Counter()
        words.update(self.lemmatized_article.split())
        return dict(filter(lambda x: (x[1] > 1) & (x[0] != '.'), words.most_common()))

    def _text_to_score(self):
        """
        Map text to list including sentence index and score

        :return:
        """
        article_lem_split = self.lemmatized_article.split('.')
        article_len = len(article_lem_split)
        return list(zip(range(article_len),
                        map(lambda x: score_sentence(x, words_popularity=self.common_words),
                            article_lem_split)))

    def create_summary(self, n_sentences=3):
        sentences_to_summary = sorted(self._text_to_score(), key=lambda x: x[1], reverse=True)
        sentences_to_summary = list(map(lambda x: x[0], sentences_to_summary))[:n_sentences]
        split_text = re.split(self.new_sentence_splitter, self.text)
        sentences_to_summary = map(split_text.__getitem__, sentences_to_summary)
        return ". ".join(sentences_to_summary)
