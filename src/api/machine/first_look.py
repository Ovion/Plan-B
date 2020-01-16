import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import SpectralClustering
from sklearn.cluster import KMeans
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier


import prepare_data as ppd

data = pd.read_csv('input/clean_data/bici_clean.csv')
data = ppd.prepare_df(data)


models = {
    'KNC': KNeighborsClassifier(n_jobs=-1, algorithm='brute', weights='distance'),
    'KNC2': KNeighborsClassifier(n_jobs=-1, algorithm='kd_tree', weights='distance'),
    'KNC3': KNeighborsClassifier(n_jobs=-1, algorithm='auto', weights='distance'),
    'RFC': RandomForestClassifier(n_jobs=-1, n_estimators=1000, criterion='entropy'),
    'GBC1': GradientBoostingClassifier(validation_fraction=0.2),
    # 'GBC2': GradientBoostingClassifier(validation_fraction=0.2, min_samples_leaf=2),
    # 'GBC3': GradientBoostingClassifier(validation_fraction=0.2, min_samples_split=3),
    # 'linear_svc': LinearSVC(),
    'svc': SVC(gamma='auto'),
    # 'Spectral': SpectralClustering(n_jobs=-1),
    'KMeans': KMeans(n_jobs=-1)
}

X = data.drop(['lesividad'], axis=1)
y = data.lesividad

for model_name, model in models.items():
    print(f'Training model: {model_name}')
    lst_success = []
    lst_leve = []
    for i in range(5):
        print(f'Iteration number {i}')
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        dpre = pd.DataFrame({
            'pred': y_pred,
            'GT': y_test,
            'All_leve': 'Leve'})

        success = round(
            (dpre[dpre.pred == dpre.GT].shape[0]/len(dpre.pred))*100, 2)
        lst_success.append(success)

        leve = round(
            (dpre[dpre.All_leve == dpre.GT].shape[0]/len(dpre.All_leve))*100, 2)
        lst_leve.append(leve)

    print("Saving data at 'output/pred/records.txt'...")
    success_mean = round(sum(lst_success)/len(lst_success), 2)
    leve_mean = round(sum(lst_leve)/len(lst_leve), 2)
    params = model.get_params
    with open('output/pred/records.txt', "a+") as file:
        file.write(
            f'''Model: {model_name}\t Acierto: {success_mean}%\t Leve: {leve_mean}%
            \n\tParams: {params} \n\n'''
        )
    print(f'Model {model_name} analyzed')
