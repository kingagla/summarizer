

def score_sentence(sentence, words_popularity):
    return sum(map(lambda x: words_popularity.get(x, 0),sentence.split()))