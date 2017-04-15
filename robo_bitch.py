from pandas import read_csv
import numpy as np
import fix
from sklearn.externals import joblib
import re

r = re.compile('[^а-яА-Я]')

clf = joblib.load('mega_faggot5.pkl')
table = read_csv('1.csv')

def predict(text):
    text = text.lower()
    text = re.sub(r,' ',text)
    while '  ' in text:
        text= text.replace('  ',' ')
    tokens = fix.tokenize_me(text)
    '''
    tokens = text.split(' ');
    for i in range(len(tokens) - 1):
        if (tokens[i + 1][0:4] == 'карт'):
            if (tokens[i][0:7] == 'кредитн'):
                tokens[i] = ''
                tokens[i + 1] = 'кредитка'
        else:
            if (tokens[i][0:7] == 'кредитн'):
                if (tokens[i + 1][0:4] == 'карт'):
                    tokens[i] = ''
                    tokens[i + 1] = 'кредитка'
    '''
    text = ' '.join(tokens)
    pred = clf.predict_proba([text])
    max_value = [0, 0, 0, 0]
    max_num = [-1,-1,-1,-1]

    for i in range(len(pred[0])):
        if (pred[0][i] > max_value[3]):
            if (pred[0][i] > max_value[2]):
                max_value[3] = max_value[2]
                max_num[3] = max_num[2]
                if (pred[0][i] > max_value[1]):
                    max_value[2] = max_value[1]
                    max_num[2] = max_num[1]
                    if (pred[0][i] > max_value[0]):
                        max_value[1] = max_value[0]
                        max_num[1] = max_num[0]
                        max_value[0] = pred[0][i]
                        max_num[0] = i
                    else:
                        max_value[1] = pred[0][i]
                        max_num[1] = i
                else:
                    max_value[2] = pred[0][i]
                    max_num[2] = i
            else:
                max_value[3] = pred[0][i]
                max_num[3] = i
    prediction = clf.predict([text])[0]
    a = [(prediction, table['theme'][prediction])]
    for i in range(3):
        if (max_value[i+1] > 0.07):
            a.append((max_num[i+1], table['theme'][max_num[i+1]]))
    return a[0]
