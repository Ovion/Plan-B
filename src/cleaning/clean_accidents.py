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

# 2018-2017
