from src import nlp

# main directory
main_data_directory = '../data'

# folders
statistical_folder = 'statistical_summaries'
bert_folder = 'extractive_bert'
bart_folder = 'abstractive_bart'
articles_folder = 'articles'

# define variables
url_ = "https://wiadomosci.wp.pl"
n_pages_ = 30

stopwords = nlp.Defaults.stop_words
plot_directory = '../plots_3p_20211206'

