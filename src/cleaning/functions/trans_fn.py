
import pandas as pd
import re


def horario(df):
    df['fecha'] = pd.to_datetime(df['fecha'], yearfirst=True)
    df['hora'] = df.fecha.dt.hour
    df['horario'] = df.hora.apply(lambda x: 'Mañana' if (
        x >= 6 and x <= 12) else ('Tarde' if (x > 12 and x <= 20) else 'Noche'))
    df.drop(['hora'], axis=1, inplace=True)
    df['dia'] = df.fecha.dt.date
    df.dia = pd.to_datetime(df.dia, yearfirst=True)
    return df


def clean_calendar(df):
    df.drop(['Dia_semana', 'Tipo de Festivo',
             'Festividad'], axis=1, inplace=True)
    df.Dia = pd.to_datetime(df['Dia'], dayfirst=True)
    df.rename(columns={
              'Dia': 'dia', 'laborable / festivo / domingo festivo': 'festividad'}, inplace=True)
    df.festividad = df.festividad.apply(lambda x: 'Festivo' if (
        x == 'domingo' or x == 'festivo') else 'Laborable')
    return df


def prepare_to_google(df):
    df.direccion = df.direccion.apply(lambda x: re.sub(r'CALL.', 'CALLE', x))
    df.direccion = df.direccion + ' Madrid'
    df['lon'] = ''
    df['lat'] = ''
    return df
