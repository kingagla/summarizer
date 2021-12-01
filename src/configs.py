from src import nlp
from src.utils import create_directory

# main directory


# folders
statistical_folder = 'statistical_summaries'
bert_folder = 'extractive_bert'
bart_folder = 'abstractive_bart'
articles_folder = 'articles'

# define variables
url_ = "https://wiadomosci.wp.pl"
n_pages_ = 1
main_data_directory = '../data/current_analysis'
create_directory(main_data_directory)
stopwords = nlp.Defaults.stop_words
plot_directory = '../plots2'