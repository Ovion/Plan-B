import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import SpectralClustering
from sklearn.cluster import KMeans
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


import prepare_data as ppd

damage = pd.read_csv('input/clean_data/bici_clean.csv')
damage = ppd.prepare_df(damage)

no_damage = pd.read_csv('input/clean_data/no_damage.csv')
no_damage = ppd.prepare_df_no_damage(no_damage)

data = pd.concat([damage, no_damage], ignore_index=True)

models = {
    'KNC': KNeighborsClassifier(n_jobs=-1, algorithm='brute', weights='uniform'),
    'RFC': RandomForestClassifier(n_jobs=-1, n_estimators=1000),
    'linear_svc': LinearSVC(),
    'svc': SVC(gamma='auto'),
    'Spectral': SpectralClustering(n_jobs=-1),
    'KMeans': KMeans(n_jobs=-1)
}

X = data.drop(['lesividad'], axis=1)
y = data.lesividad

for model_name, model in models.items():
    print(f'Training model: {model_name}')
    lst_success = []
    for i in range(3):
        print(f'Iteration number {i}')
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        dpre = pd.DataFrame({
            'pred': y_pred,
            'GT': y_test})

        success = round(
            (dpre[dpre.pred == dpre.GT].shape[0]/len(dpre.pred))*100, 2)
        lst_success.append(success)

    print("Saving data at 'output/pred/records.txt'...")
    success_mean = round(sum(lst_success)/len(lst_success), 2)
    params = model.get_params
    with open('output/pred/records.txt', "a+") as file:
        file.write(
            f'''Model: {model_name}\t Acierto: {success_mean}%\t Params: {params} \n\n'''
        )
    print(f'Model {model_name} analized')
