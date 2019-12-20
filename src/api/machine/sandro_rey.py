
import pandas as pd
import pickle

from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier


def pred_y_buenas_noches(X):
    df = X
    knc = joblib.load('output/pred/model_knc_brute_uni.pkl')
    y_pred = knc.predict(X)
    df['lesividad'] = y_pred
    df = df[df.lesividad != 'Leve']
    df.to_csv('output/X_to_pred.csv', index=False)
    df['weights'] = df.lesividad.apply(
        lambda x: 1 if x == 'Moderada' else 2)

    return df
