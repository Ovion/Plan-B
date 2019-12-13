import pandas as pd
import numpy as np
import re
import random

#


def get_df_norm_header_index(path):
    lst_header = ['num_exp', 'dia', 'hora', 'calle', 'num', 'distrito',
                  'tipo_accidente', 'meteo', 'vehiculo', 'persona', 'edad', 'sexo', 'lesividad']
    df = pd.read_csv(path, encoding='latin_1', sep=';', names=lst_header)
    df.drop(0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def minor_change_2017(df):
    dict_rename = {
        'Nº VICTIMAS *': '* Nº VICTIMAS'
    }
    df.rename(columns=dict_rename, inplace=True)
    return df


def change_cols_17_18(df):
    dict_cols = {
        'FECHA': 'dia',
        'DISTRITO': 'distrito', 'LUGAR ACCIDENTE': 'calle', 'Nº': 'num',
        'TIPO ACCIDENTE': 'tipo_accidente', 'LESIVIDAD': 'lesividad',
        'CPFA Granizo': 'Granizo', 'CPFA Hielo': 'Hielo', 'CPFA Lluvia': 'Lluvia',
        'CPFA Niebla': 'Niebla', 'CPFA Seco': 'Despejado', 'CPFA Nieve': 'Nieve',
    }
    to_drop = ['Nº PARTE', 'CPSV Seca Y Limpia', 'CPSV Mojada', 'CPSV Aceite', 'CPSV Barro',
               'CPSV Grava Suelta', 'CPSV Hielo', '* Nº VICTIMAS', 'Tipo Vehiculo', 'TIPO PERSONA', 'SEXO', 'Tramo Edad']
    df.rename(columns=dict_cols, inplace=True)
    df.drop(to_drop, axis=1, inplace=True)

    return df


def create_weather_17_18(df):
    lst_w = list(df[df.columns[6:12]])
    for e in lst_w:
        df[e] = df[e].apply(lambda x: '' if (x == 'NO') else e)
    df['meteo'] = df[lst_w].sum(axis=1)
    df.drop(lst_w, axis=1, inplace=True)
    return df


def refactor_meteo_17_18(values):
    dict_meteo = {
        r'Granizo': 'Granizo',
        r'Hielo': 'Nieve',
        r'Nieve': 'Nieve',
        r'Lluvia': 'Lluvia',
        r'Niebla': 'Niebla', }
    for k, v in dict_meteo.items():
        if re.match(k, values):
            return v
    return 'Despejado'


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


def create_date_17_18(df):
    df['hora'] = df['RANGO HORARIO'].str.extract(r'(\d[\d]?:\d+\s)')
    create_date(df)
    df.drop(['RANGO HORARIO', 'DIA SEMANA'], axis=1, inplace=True)
    return df


def create_dir(df):
    df.num = df.num.apply(lambda x: x.strip())
    df.num = df.num.apply(lambda x: '-' if x == '0' else x)
    df.loc[(df.num == '-'), 'num'] = ''
    df['direccion'] = df.calle+' '+df.num
    df.direccion = df.direccion.apply(lambda x: x.strip())
    df.drop(['calle', 'num'], axis=1, inplace=True)
    return df


def change_accident(values):
    dict_accidente = {
        r'caída': 'Caida',
        r'colisión': 'Colision',
        r'alcance': 'Colision',
        r'atropello': 'Imprudencia',
        r'choque': 'Imprudencia'}
    for k, v in dict_accidente.items():
        if re.match(k, values.lower()):
            return v
    return 'Otro'


def change_injury(values):
    dict_injury = {
        '01': 'Moderada', '02': 'Moderada',
        '03': 'Grave',
        '04': 'Fallecido',
        '05': 'Leve', '06': 'Leve', '07': 'Leve', '14': 'Leve'}
    return dict_injury[values]


def change_injury_17_18(values):
    dict_injury = {
        'IL': 'Moderada',
        'HG': 'Grave',
        'MT': 'Fallecido',
        'HL': 'Leve', 'NO ASIGNADA': 'Leve'}
    return dict_injury[values]


def order_columns(df):
    return df[['fecha', 'meteo', 'tipo_accidente', 'lesividad', 'distrito', 'direccion']]
