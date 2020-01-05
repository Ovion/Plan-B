import requests
import pandas as pd
from IPython.display import clear_output

bicis = pd.read_csv('input/clean_data/bici_clean.csv')

print('Loading data to mongo...')
url = 'http://localhost:5000/create'
for indx, row in bicis.iterrows():
    clear_output()
    params = {
        'fecha': row['fecha'],
        'year': row['year'],
        'horario': row['horario'],
        'festividad': row['festividad'],
        'tipo_accidente': row['tipo_accidente'],
        'lesividad': row['lesividad'],
        'meteo': row['meteo'],
        'distrito': row['distrito'],
        'direccion': row['direccion'],
        'lon': row['lon'],
        'lat': row['lat']
    }
    requests.post(url, data=params).text

print('Load complete')
