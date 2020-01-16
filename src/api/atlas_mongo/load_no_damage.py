import pandas as pd
from Mongo import submit_df


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
# Here I calculate the 'no_damage' dataframe

lst_h = list(bici.horario.unique())
lst_f = list(bici.festividad.unique())
lst_m = list(bici.meteo.unique())

no_damage = pd.DataFrame(
    columns=['horario', 'festividad', 'lesividad', 'meteo', 'lon', 'lat'])


print('Creating a grid of Madrid...')
for h in lst_h:
    for f in lst_f:
        for m in lst_m:
            bici_test = bici.loc[(bici.horario == h) & (
                bici.festividad == f) & (bici.meteo == m)]

            min_lat = int((bici_test.lat.min()-0.0002)*125)
            max_lat = int((bici_test.lat.max()+0.0002)*125)

            min_lon = int((bici_test.lon.min()-0.00015)*93.75)
            max_lon = int((bici_test.lon.max()+0.00015)*93.75)

            for lat in range(min_lat, max_lat):
                for lon in range(min_lon, max_lon):
                    no_damage = no_damage.append({
                        'horario': h,
                        'festividad': f,
                        'lesividad': 'No',
                        'meteo': m,
                        'lon': lon/93.75,
                        'lat': lat/125,
                    }, ignore_index=True)

print('Counting the num of accidents...')
num_lon = 1/93.75*3/4
num_lat = 1/125*3/4

no_damage['num_acc'] = int()
lst_ = list()
for i, r in no_damage.iterrows():
    accs = len(bici.loc[
        (bici.horario == r['horario']) & (bici.festividad == r['festividad']) & (bici.meteo == r['meteo']) &
        (bici.lon >= (r['lon']-num_lon)) & (bici.lon <= (r['lon']+num_lon)) &
        (bici.lat >= (r['lat']-num_lat)) & (bici.lat <= (r['lat']+num_lat))])
    no_damage.loc[i, 'num_acc'] = accs

no_damage = no_damage.loc[no_damage.num_acc == 0]

print('Saving data in local and MongoDB...')
no_damage.to_csv('input/clean_data/no_damage.csv', index=False)
submit_df(no_damage)
