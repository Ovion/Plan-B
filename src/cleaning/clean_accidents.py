import pandas as pd

import functions.clean_fn as fnc


# 2019
bici_19 = fnc.get_df_norm_header_index(
    'bicicletas/AccidentesBicicletas_2019.csv')
bici_19 = fnc.create_date(bici_19)
bici_19 = fnc.create_dir(bici_19)
bici_19 = fnc.fill_drop(bici_19)

bici_19.tipo_accidente = bici_19.tipo_accidente.apply(
    lambda x: fnc.change_accident(x))
bici_19.lesividad = bici_19.lesividad.apply(
    lambda x: fnc.change_injury(str(x)))

bici_19 = fnc.order_columns(bici_19)

# 2018
bici_18 = pd.read_csv(
    'bicicletas/AccidentesBicicletas_2018.csv', encoding='latin_1', sep=';')
bici_18 = fnc.change_cols_17_18(bici_18)

bici_18 = fnc.create_weather_17_18(bici_18)
bici_18 = fnc.create_weather_17_18(bici_18)
bici_18.meteo = bici_18.meteo.apply(lambda x: fnc.refactor_meteo_17_18(x))

bici_18 = fnc.create_dir(bici_18)

bici_18.tipo_accidente = bici_18.tipo_accidente.apply(
    lambda x: fnc.change_accident(x))
bici_18.lesividad = bici_18.lesividad.apply(
    lambda x: fnc.change_injury_17_18(x.strip()))

bici_18 = fnc.order_columns(bici_18)

# 2017
bici_17 = pd.read_csv(
    'bicicletas/AccidentesBicicletas_2017.csv', encoding='latin_1', sep=';')
bici_17 = fnc.minor_change_2017(bici_17)
bici_17 = fnc.change_cols_17_18(bici_17)

bici_17 = fnc.create_weather_17_18(bici_17)
bici_17 = fnc.create_weather_17_18(bici_17)
bici_17.meteo = bici_17.meteo.apply(lambda x: fnc.refactor_meteo_17_18(x))

bici_17 = fnc.create_dir(bici_17)

bici_17.tipo_accidente = bici_17.tipo_accidente.apply(
    lambda x: fnc.change_accident(x))
bici_17.lesividad = bici_17.lesividad.apply(
    lambda x: fnc.change_injury_17_18(x.strip()))

bici_17 = fnc.order_columns(bici_17)
