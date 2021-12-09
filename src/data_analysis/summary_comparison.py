import os

import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from src.configs import *
from src.modelling.utils import get_bert_representation, split_text
from src.utils import load_json, create_directory


class SummaryComparator:
    def __init__(self, original_json, statistical_json, bert_json, bart_json):
        assert (original_json['title'] == statistical_json['title'] == bert_json['title'] == bart_json['title']), \
            "Titles of summaries must be the same as title of article!"
        self.title = original_json['title']
        self.original_text = original_json['text']
        self.summaries = {'statistical': statistical_json['summary'], 'bert': bert_json['summary'],
                          'bart': bart_json['summary']}

    def similarity_spacy(self, reference_text):
        similarity_dict = {}
        for kind, summary in self.summaries.items():
            doc1 = nlp(reference_text)
            doc2 = nlp(summary)
            similarity_dict[kind] = [doc1.similarity(doc2)]
        return pd.DataFrame(similarity_dict)

    def similarity_cosine(self, reference_text, tokenizer, model):
        if len(split_text(reference_text)) > 1:
            bert_reference = get_bert_representation(reference_text, tokenizer, model)
        else:
            input_ = tokenizer.encode(reference_text)
            bert_reference = model(torch.tensor([input_])).pooler_output.detach().numpy()

        similarity_dict = {'title': [self.title]}
        for kind, summary in self.summaries.items():
            bert_summary = get_bert_representation(summary, tokenizer, model)
            similarity_dict[kind] = cosine_similarity(bert_reference, bert_summary)[0]
        return pd.DataFrame(similarity_dict)


def generate_excel_with_comparison(directory, tokenizer, model):
    create_directory(directory)
    articles_directory = os.path.join(main_data_directory, articles_folder)
    statistical_directory = os.path.join(main_data_directory, statistical_folder)
    bert_directory = os.path.join(main_data_directory, bert_folder)
    bart_directory = os.path.join(main_data_directory, bart_folder)

    # files = os.listdir(articles_directory)
    files = os.listdir(statistical_directory)

    cos_sim = pd.DataFrame()
    cos_sim_centroid = pd.DataFrame()
    spacy_sim = pd.DataFrame()
    spacy_sim_centroid = pd.DataFrame()

    for file in tqdm(files):
        article_json = load_json(os.path.join(articles_directory, file))
        stat_json = load_json(os.path.join(statistical_directory, file))
        bert_json = load_json(os.path.join(bert_directory, file))
        bart_json = load_json(os.path.join(bart_directory, file))

        comparison = SummaryComparator(article_json, stat_json, bert_json, bart_json)
        cos_sim = cos_sim.append(comparison.similarity_cosine(article_json['title'], tokenizer, model))
        cos_sim_centroid = cos_sim_centroid.append(comparison.similarity_cosine(article_json['text'], tokenizer, model))
        spacy_sim = spacy_sim.append(comparison.similarity_spacy(article_json['title']))
        spacy_sim_centroid = spacy_sim_centroid.append(comparison.similarity_spacy(article_json['text']))

    cos_sim.to_excel(os.path.join(directory, 'cos_sim.xlsx'), index=False)
    cos_sim_centroid.to_excel(os.path.join(directory, 'cos_sim_centroid.xlsx'), index=False)
    spacy_sim.to_excel(os.path.join(directory, 'spacy_sim.xlsx'), index=False)
    spacy_sim_centroid.to_excel(os.path.join(directory, 'spacy_sim_centroid.xlsx'), index=False)

