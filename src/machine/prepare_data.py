import pandas as pd


def num_horario(value):
    dict_hora = {
        'Mañana': 1,
        'Tarde': 2,
        'Noche': 3
    }
    return dict_hora[value]


def num_fest(value):
    dict_fest = {
        'Laborable': 1,
        'Vispera': 2,
        'Festivo': 3
    }
    return dict_fest[value]


def prepare_df(data):
    data.drop(['fecha', 'dia', 'year', 'tipo_accidente',
               'distrito', 'direccion'], axis=1, inplace=True)
    data.horario = data.horario.apply(lambda x: num_horario(x))
    data.festividad = data.festividad.apply(lambda x: num_fest(x))
    data = pd.get_dummies(data, columns=['meteo'], prefix_sep='', prefix='')
    return data


def prepare_to_predict(hour, day, lon_a, lat_a, lon_b, lat_b, weather):
    return df
