from pandas import read_csv
import numpy as np
from sklearn.externals import joblib

clf = joblib.load('mega_faggot.pkl')
table = read_csv('1.csv')

def predict(text):
    prediction = clf.predict([text])[0]
    return prediction, table['theme'][prediction]


