import pandas as pd

bici = pd.read_csv("input/clean_data/bici_clean.csv")

# Here I reduce the number of accidents with injury 'Leve' in order to a better prediction
num_lon = 1/93.75*0.5
num_lat = 1/125*0.5

bici['num_acc'] = 100

print('Reducing dataframe...')
for i, r in bici.loc[(bici.lesividad == 'Leve') & (bici.meteo != 'Lluvia')].iterrows():
    accs = len(bici.loc[
        (bici.horario == r['horario']) & (bici.festividad == r['festividad']) & (bici.meteo == r['meteo']) &
        (bici.lon >= (r['lon']-num_lon)) & (bici.lon <= (r['lon']+num_lon)) &
        (bici.lat >= (r['lat']-num_lat)) & (bici.lat <= (r['lat']+num_lat))])
    bici.loc[i, 'num_acc'] = accs

bici['mark'] = int()
bici.loc[(bici.lesividad == 'Leve') & (bici.festividad == 'Laborable')
         & (bici.meteo == 'Despejado') & (bici.num_acc <= 5), 'mark'] = 1

bici = bici.loc[bici.num_acc > 2]
bici = bici.loc[bici.mark == 0]
bici.drop(['num_acc', 'mark'], axis=1, inplace=True)

bici.to_csv('input/clean_data/bici_trick.csv', index=False)
print("New dataframe saved in 'input/clean_data/bici_trick.csv'")
