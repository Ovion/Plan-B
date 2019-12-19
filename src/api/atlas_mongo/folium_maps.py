
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

import pandas as pd

from atlas_mongo.Mongo import ConectColl


def create_df_coords(datas):
    df = pd.DataFrame(columns=['Lat', 'Lon', 'Weights'])
    for data in datas:
        df = df.append({
            'Lat': data['localizacion']['coordinates'][1],
            'Lon': data['localizacion']['coordinates'][0],
            'Weights': 0.2 if data['lesividad'] == 'Leve' else (5 if data['lesividad'] == 'Moderada' else 10)
        }, ignore_index=True)
    return df


def create_map(df):
    # Create a base map
    heat_m = folium.Map(location=[40.416, -3.694],
                        tiles='cartodbpositron', zoom_start=15)

    # Add a heatmap to the base map
    HeatMap(data=df[['Lat', 'Lon', 'Weights']], radius=15).add_to(heat_m)

    return heat_m


def create_map_dir(coll, lat_a, lon_a, lat_b, lon_b):
    # Create a base map
    start_lat = round((lat_a+lat_b)/2, 7)
    start_lon = round((lon_b+lon_a)/2, 7)
    heat_m = folium.Map(location=[start_lat, start_lon],
                        tiles='cartodbpositron', zoom_start=15)

    # Create groups

    manana_group = folium.FeatureGroup(name="Mañana")
    tarde_group = folium.FeatureGroup(name="Tarde")
    noche_group = folium.FeatureGroup(name="Noche")

    # Add a heatmap to the base map
    Marker([lat_a, lon_a]).add_to(heat_m)
    # Add childs
    heat_m.add_child(Marker([lat_b, lon_b]))

    bicis_manana = coll.acc.find({"horario": "Mañana"})
    acc_manana = create_df_coords(bicis_manana)
    HeatMap(data=acc_manana[['Lat', 'Lon', 'Weights']],
            radius=15).add_to(manana_group)

    bicis_tarde = coll.acc.find({"horario": "Tarde"})
    acc_tarde = create_df_coords(bicis_tarde)
    HeatMap(data=acc_tarde[['Lat', 'Lon', 'Weights']],
            radius=15).add_to(tarde_group)

    bicis_noche = coll.acc.find({"horario": "Noche"})
    acc_noche = create_df_coords(bicis_noche)
    HeatMap(data=acc_noche[['Lat', 'Lon', 'Weights']],
            radius=15).add_to(noche_group)

    manana_group.add_to(heat_m)
    tarde_group.add_to(heat_m)
    noche_group.add_to(heat_m)
    folium.LayerControl(collapsed=False).add_to(heat_m)

    return heat_m


def print_heat_map(coll):
    bicis = coll.acc.find()
    accidents = create_df_coords(bicis)
    heat_map = create_map(accidents)
    heat_map.save(f'output/heat_map.html')
    return heat_map


def print_heat_map_dir(coll, lat_a, lon_a, lat_b, lon_b):
    heat_map = create_map_dir(coll, lat_a, lon_a, lat_b, lon_b)
    heat_map.save(f'output/heat_map.html')
    return heat_map


# Deprecate


def print_heat_map_h(coll, interh):
    bicis = coll.acc.find({"horario": interh})
    accidents = create_df_coords(bicis)
    heat_map = create_map(accidents)
    heat_map.save(f'output/heat_map_{interh}.html')
    return heat_map


def print_heat_map_i(coll, injury):
    bicis = coll.acc.find({"lesividad": injury})
    accidents = create_df_coords(bicis)
    heat_map = create_map(accidents)
    heat_map.save(f'output/heat_map_{injury}.html')
    return heat_map
