
import pandas as pd
import pickle

from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier


def pred_y_buenas_noches(X):
    df = X
    knc = joblib.load('output/pred/model_knc_brute_uni.pkl')
    y_pred = knc.predict(X)
    df['lesividad'] = y_pred
    df['weights'] = 0.2 if df['lesividad'] == 'Leve' else (
        5 if df['lesividad'] == 'Moderada' else 10)
    return df
