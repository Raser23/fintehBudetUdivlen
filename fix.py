import nltk
import string
import numpy as np
import pymorphy2
from nltk.corpus import stopwords
from pandas import read_csv

morph = pymorphy2.MorphAnalyzer()


def tokenize_me(file_text):
    #deleting stop_words
    stop_words = stopwords.words('russian')
    #print(stop_words)
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', 'хочу'])
    tokens = [t for t in file_text.split(' ') if t!= '' and t!=' ' and t not in stop_words]
    new_tok = []
    for i in tokens:
        new_tok.append(morph.parse(i)[0].normal_form)
    tokens = new_tok
    for i in range(len(tokens) - 1):
        if(tokens[i+1][0:4] == 'карт'):
            if (tokens[i][0:7] == 'кредитн'):
                tokens[i] = ''
                tokens[i+1] = 'кредитка'
        else:
            if(tokens[i][0:7] == 'кредитн'):
                if (tokens[i + 1][0:4] == 'карт'):
                    tokens[i] = ''
                    tokens[i + 1] = 'кредитка'

    return tokens


