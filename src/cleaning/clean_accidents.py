import pandas as pd

import functions.clean_fn as fnc


# 2019
print('Cleaning 2019...')
bici_19 = fnc.get_df_norm_header_index(
    'input/raw_data/bicicletas/AccidentesBicicletas_2019.csv')

bici_19 = fnc.fill_drop(bici_19)

bici_19.meteo = bici_19.meteo.apply(lambda x: fnc.refactor_meteo(x))

bici_19 = fnc.create_date(bici_19)
bici_19 = fnc.create_dir(bici_19)

bici_19.tipo_accidente = bici_19.tipo_accidente.apply(
    lambda x: fnc.change_accident(x))
bici_19.lesividad = bici_19.lesividad.apply(
    lambda x: fnc.change_injury(str(x)))

bici_19 = fnc.order_columns(bici_19)
print('Done')
print('Saving 2019 in: input/clean_data/AB_19 ...')
bici_19.to_csv('input/clean_data/AB_19.csv', index=False)
print('Done')

# 2018
print('Cleaning 2018...')
bici_18 = pd.read_csv(
    'input/raw_data/bicicletas/AccidentesBicicletas_2018.csv', encoding='latin_1', sep=';')
bici_18 = fnc.change_cols_17_18(bici_18)

bici_18 = fnc.create_weather_17_18(bici_18)
bici_18.meteo = bici_18.meteo.apply(lambda x: fnc.refactor_meteo(x))

bici_18 = fnc.create_date_17_18(bici_18)
bici_18 = fnc.create_dir(bici_18)

bici_18.tipo_accidente = bici_18.tipo_accidente.apply(
    lambda x: fnc.change_accident(x))
bici_18.lesividad = bici_18.lesividad.apply(
    lambda x: fnc.change_injury_17_18(x.strip()))

bici_18 = fnc.order_columns(bici_18)
print('Done')
print('Saving 2018 in: input/clean_data/AB_18 ...')
bici_18.to_csv('input/clean_data/AB_18.csv', index=False)
print('Done')

# 2017
print('Cleaning 2017...')
bici_17 = pd.read_csv(
    'input/raw_data/bicicletas/AccidentesBicicletas_2017.csv', encoding='latin_1', sep=';')
bici_17 = fnc.minor_change_2017(bici_17)
bici_17 = fnc.change_cols_17_18(bici_17)

bici_17 = fnc.create_weather_17_18(bici_17)
bici_17.meteo = bici_17.meteo.apply(lambda x: fnc.refactor_meteo(x))

bici_17 = fnc.create_date_17_18(bici_17)
bici_17.dropna(inplace=True)
bici_17 = fnc.create_dir(bici_17)

bici_17.tipo_accidente = bici_17.tipo_accidente.apply(
    lambda x: fnc.change_accident(x))
bici_17.lesividad = bici_17.lesividad.apply(
    lambda x: fnc.change_injury_17_18(x.strip()))

bici_17 = fnc.order_columns(bici_17)
print('Done')
print('Saving 2017 in: input/clean_data/AB_17 ...')
bici_17.to_csv('input/clean_data/AB_17.csv', index=False)
print('Done')
