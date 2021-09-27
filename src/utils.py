import os
import morfeusz2
from src import time_counter


def create_directory(directory):
    directory = os.path.abspath(directory).split('/')
    for i in range(2, len(directory) + 1):
        direc = "/".join(directory[:i])
        if not os.path.isdir(direc):
            os.mkdir(direc)

@time_counter
def lemmatize_text(text):
    if isinstance(text, str):
        text = text.split()
    morf = morfeusz2.Morfeusz(expand_dag=True, expand_tags=True)
    text_new = []
    for word in text:
        w = morf.analyse(word)[0][0][1].split(':')[0]
        if w == 'oko':
            w = 'ok'
        text_new.append(w)
    return " ".join(text_new)
