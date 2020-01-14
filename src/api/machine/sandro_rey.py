
import pandas as pd
import pickle

from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier


def pred_y_buenas_noches(X):
    df = X
    gbc = joblib.load('output/pred/model_gbc_0.2.pkl')
    y_pred = gbc.predict(X)

    df['lesividad'] = y_pred
    df = df[df.lesividad != 'No']
    df.to_csv('output/X_to_pred.csv', index=False)

    df['weights'] = df.lesividad.apply(
        lambda x: 0.2 if x == 'Leve' else (1 if x == 'Moderada' else 2))

    return df
