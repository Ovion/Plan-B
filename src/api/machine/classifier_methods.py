import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier

import prepare_data as ppd

print('Creating model...')
damage = pd.read_csv('input/clean_data/bici_clean.csv')
damage = ppd.prepare_df(damage)

no_damage = pd.read_csv('input/clean_data/no_damage.csv')
no_damage = ppd.prepare_df_no_damage(no_damage)

data = pd.concat([damage, no_damage], ignore_index=True)

X = data.drop(['lesividad'], axis=1)
y = data.lesividad

gbc = GradientBoostingClassifier(validation_fraction=0.2)
gbc.fit(X, y)

print("Saving model in 'output/pred/model_gbc_0.2.pkl'")
joblib.dump(gbc, 'output/pred/model_gbc_0.2.pkl')

# Load the model from the file
# knn_from_joblib = joblib.load('filename.pkl')

# Use the loaded model to make predictions
# knn_from_joblib.predict(X_test)
