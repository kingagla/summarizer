from src import nlp

# main directory
main_data_directory = '../data/current_analysis'

# folders
statistical_folder = 'statistical_summaries'
bert_folder = 'extractive_bert'
bart_folder = 'abstractive_bart'
articles_folder = 'articles'

# define variables
url_ = "https://wiadomosci.wp.pl"
n_pages_ = 1

stopwords = nlp.Defaults.stop_words
plot_directory = '../plots2'

