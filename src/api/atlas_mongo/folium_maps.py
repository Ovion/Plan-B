
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
            'Weights': 0.2 if data['lesividad'] == 'Leve' else (2 if data['lesividad'] == 'Moderada' else 3)
        }, ignore_index=True)
    return df


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
    Marker([lat_a, lon_a], icon=folium.Icon(color='red')).add_to(heat_m)
    # Add childs
    heat_m.add_child(Marker([lat_b, lon_b], icon=folium.Icon(color='red')))

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


def print_heat_map_dir(coll, lat_a, lon_a, lat_b, lon_b):
    heat_map = create_map_dir(coll, lat_a, lon_a, lat_b, lon_b)
    heat_map.save(f'output/heat_map.html')
    return heat_map


def print_heat_map_pred(df, lat_a, lon_a, lat_b, lon_b):
    start_lat = round((lat_a+lat_b)/2, 7)
    start_lon = round((lon_b+lon_a)/2, 7)
    heat_map = folium.Map(location=[start_lat, start_lon],
                          tiles='cartodbpositron', zoom_start=15)
    HeatMap(data=df[['lat', 'lon', 'weights']],
            radius=16).add_to(heat_map)
    heat_map.add_child(
        Marker(location=[lat_a, lon_a], icon=folium.Icon(color='red')))
    heat_map.add_child(
        Marker(location=[lat_b, lon_b], icon=folium.Icon(color='red')))
    return heat_map
