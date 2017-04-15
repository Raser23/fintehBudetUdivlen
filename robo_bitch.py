from pandas import read_csv
import numpy as np
from sklearn.externals import joblib
import re

r = re.compile('[^а-яА-Я]')

clf = joblib.load('mega_faggot.pkl')
table = read_csv('1.csv')

def predict(text):
    #print('called')
    text = text.lower()
    text = re.sub(r,' ',text)
    while '  ' in text:
        text= text.replace('  ',' ')
    #print(text)
    prediction = clf.predict([text])[0]
    return prediction, table['theme'][prediction]

