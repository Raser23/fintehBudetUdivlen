from sklearn.feature_extraction.text import CountVectorizer
from pandas import read_csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
train = read_csv("fixed_train.csv", sep = ',')

"""
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train['Speech'])


tf_transformer = TfidfTransformer(use_idf=True).fit(X_train_counts)
X_train_tfidf = tf_transformer.transform(X_train_counts)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, train['ThemeLabel'])

#test, delete later
docs_new = ['я бы хотел заблокировать карту', 'я хотел бы взять кредит']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))
"""
#using Vectors

from sklearn.externals import joblib

clf = joblib.load('mega_faggot.pkl')
text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                            alpha=1e-3, n_iter=5, random_state=42)),])

import numpy as np
docs_test = train['Speech']
text_clf = text_clf.fit(train['Speech'], train['ThemeLabel'])
predicted = clf.predict(docs_test)
print(np.mean(predicted == train['ThemeLabel']))

joblib.dump(text_clf, 'mega_faggot.pkl')