# Summary creator
The main aim of this project is to create a tool for summarizing Polish texts. The texts are news scrapped from https://www.wp.pl/ with download_articles.py file. 

I consider 3 approaches:
- **Statistical** - extractive summary where sentences are chosen based on "popular words". Each word (excluding stopwords) gets a score - more frequent word in the text, higher score. Then sentences get a score which is the sum of scores from words in the sentence. Three sentences with the highest score (ordered as in the original text makes a summary).
- **BERT based** - extractive summary where sentences are chosen based on BERT embeddings of sentences. BERT representation of each sentence is a vector of length 768. K-Mean algorithm is applied on those vectors, where k=3. Summary is created from sentences that are closest to each center of the cluster.
- **BART based** - abstractive summary using BART model with no customization.



