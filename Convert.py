import nltk
import string
import numpy as np
from nltk.corpus import stopwords
from pandas import read_csv
from pymystem3 import Mystem
import pymystem3
#nltk.download()


def tokenize_me(file_text):
    #deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    tokens = [t for t in file_text.split(' ') if t!= '' and t!=' ' and t not in stop_words]
    #print(tokens)
    return tokens
f = open('fixed_train.csv', 'w', encoding="utf-8")
f.write('Index,' + 'Speech,' + 'ThemeLabel' + '\n')
train = read_csv("train.csv", sep = ',')
for i in range(11326):
    index = train['Index'][i]
    new_text = str(' '.join(tokenize_me(train['Speech'][i])))
    if (new_text == '' or new_text == ' '):
        continue
    answer = str(train['ThemeLabel'][i])
    f.write(str(index) + ',' + new_text + ',' + answer + '\n')
    #print(answer)

