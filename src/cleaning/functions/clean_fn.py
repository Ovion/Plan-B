import pandas as pd
import numpy as np
import re
import random


def get_df_norm_header_index(path):
    lst_header = ['num_exp', 'dia', 'hora', 'calle', 'num', 'distrito',
                  'tipo_accidente', 'meteo', 'vehiculo', 'persona', 'edad', 'sexo', 'lesividad']
    df = pd.read_csv(path, encoding='latin_1', sep=';', names=lst_header)
    df.drop(0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def fill_drop(df):
    df.lesividad.fillna('14', inplace=True)
    df.meteo.fillna('Se desconoce', inplace=True)
    df.drop(['sexo', 'vehiculo', 'persona', 'edad',
             'num_exp'], axis=1, inplace=True)
    return df


def create_date(df):
    df['fecha'] = df.dia+' '+df.hora
    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
    df['fecha'] = df['fecha'].dt.round('H')
    df.drop(['dia', 'hora'], axis=1, inplace=True)
    return df


def create_dir(df):
    df.num.apply(lambda x: x.strip())
    df.num = df.num.apply(lambda x: '-' if x == '0' else x)
    df.loc[(df.num == '-'), 'num'] = ''
    df['direccion'] = df.calle+' '+df.num
    df.direccion.apply(lambda x: x.strip())
    df.drop(['calle', 'num'], axis=1, inplace=True)
    return df


def change_accident(values):
    dict_accidente = {
        r'Caída': 'Caida',
        r'Colisión': 'Colision',
        r'Alcance': 'Colision',
        r'Atropello': 'Imprudencia',
        r'Choque': 'Imprudencia'}
    for k, v in dict_accidente.items():
        if re.match(k, values):
            return v
    return 'Otro'


def change_injury(values):
    dict_injury = {
        '01': 'Moderada', '02': 'Moderada',
        '03': 'Grave',
        '04': 'Fallecido',
        '05': 'Leve', '06': 'Leve', '07': 'Leve', '14': 'Leve'}
    return dict_injury[values]


def order_columns(df):
    return df[['fecha', 'meteo', 'tipo_accidente', 'lesividad', 'distrito', 'direccion']]
