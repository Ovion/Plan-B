import pandas as pd
import prepare_data as ppd

import h2o
from h2o.automl import H2OAutoML

h2o.init(nthreads=-1, max_mem_size=12)

data = pd.read_csv('input/clean_data/bici_clean.csv')
data = ppd.prepare_df(data)
data.to_csv('input/clean_data/to_h2o.csv', index=False)

data = h2o.import_file('input/clean_data/to_h2o.csv')

splits = data.split_frame(ratios=[0.8], seed=1)
train = splits[0]
test = splits[1]

y = 'lesividad'
train[y] = train[y].asfactor()
test[y] = test[y].asfactor()

X_test = test.drop(['lesividad'], axis=1)

aml = H2OAutoML(nfolds=5, max_runtime_secs=300)
aml.train(y=y, training_frame=train, validation_frame=test)

y_pred = aml.predict(X_test)

aux = test['lesividad']
aux['pred'] = test['lesividad']
aux['GT'] = y_pred['predict']
aux = aux.as_data_frame(use_pandas=True)

acierto = round((aux[aux.pred == aux.GT].shape[0]/len(aux.pred))*100, 2)

with open('../../output/pred/records.txt', "a+") as file:
    file.write(
        f'''Model: H2O\t Acierto: {acierto}%\t Params: \n\n'''
    )
