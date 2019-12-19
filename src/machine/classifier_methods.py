import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier

import prepare_data as ppd

data = pd.read_csv('input/clean_data/bici_clean.csv')
data = ppd.prepare_df(data)

X = data.drop(['lesividad'], axis=1)
y = data.lesividad

knc = KNeighborsClassifier(
    n_jobs=-1, algorithm='brute', weights='uniform')
knc.fit(X, y)

joblib.dump(knc, 'output/pred/model_knc_brute_uni.pkl')

# Load the model from the file
# knn_from_joblib = joblib.load('filename.pkl')

# Use the loaded model to make predictions
# knn_from_joblib.predict(X_test)
