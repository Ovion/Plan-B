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


def get_fest(day):
    cal = pd.read_csv('input/clean_data/cal_clean.csv')
    fest_cat = cal[cal.dia == day]['festividad'].values[0]
    return fest_cat


def prepare_df(data):
    data.drop(['fecha', 'dia', 'year', 'tipo_accidente',
               'distrito', 'direccion'], axis=1, inplace=True)
    data.horario = data.horario.apply(lambda x: num_horario(x))
    data.festividad = data.festividad.apply(lambda x: num_fest(x))
    data = pd.get_dummies(data, columns=['meteo'], prefix_sep='', prefix='')
    return data


def prepare_to_predict(hour, day, lon_a, lat_a, lon_b, lat_b, weather):
    horario = int(num_horario(hour))

    fest_cat = get_fest(day)
    fest = int(num_fest(fest_cat))

    lats = [lat_a, lat_b]
    lons = [lon_a, lon_b]

    df = pd.DataFrame(columns=['horario', 'festividad',
                               'lon', 'lat', 'Despejado', 'Lluvia', 'Niebla'])

    min_lat = int((min(lats)-0.01)*2000)
    max_lat = int((max(lats)+0.01)*2000)

    min_lon = int((min(lons)-0.01)*2000)
    max_lon = int((max(lons)+0.01)*2000)

    for lat in range(min_lat, max_lat):
        for lon in range(min_lon, max_lon):
            df = df.append({
                'horario': horario,
                'festividad': fest,
                'lon': lon/2000,
                'lat': lat/2000,
                'Despejado': int(1 if weather == 'Despejado' else 0),
                'Lluvia': int(1 if weather == 'Lluvia' else 0),
                'Niebla': int(1 if weather == 'Niebla' else 0),
            }, ignore_index=True)

    return df
