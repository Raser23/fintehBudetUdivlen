from pandas import read_csv
import numpy as np
#import fix
from sklearn.externals import joblib
import re
import fix
r = re.compile('[^а-яА-Я]')

clf = joblib.load('mega_faggot2.pkl')
table = read_csv('1.csv')

def predict(text):
    if(text == 'инн'):
        return [(32,'Реквизиты банка')]
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
    a = []
    for i in range(3):
        if (max_value[i] > 0.225):
            a.append((max_num[i], table['theme'][max_num[i]]))
    return a

def predict_csv(csv_path):
    texts = read_csv(csv_path, sep = ',',encoding='utf-8')
    a = str(csv_path)[0:-4] + 'output.csv'
    f = open(a, 'w', encoding='utf-8')
    f.write('Index,ThemeLabel\n')
    for i in range(texts['Index'].size):
        #print(predict(texts['Speech'][i])[0][0])
        f.write(str(texts['Index'][i]) + ',' + str(predict(texts['Speech'][i])[0][0]) + '\n')
    return a

