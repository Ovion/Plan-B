
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

import pandas as pd

from atlas_mongo.Mongo import ConectColl


def create_df_coords(datas):
    df = pd.DataFrame(columns=['Lat', 'Lon'])
    for data in datas:
        df = df.append({
            'Lat': data['localizacion']['coordinates'][1],
            'Lon': data['localizacion']['coordinates'][0]}, ignore_index=True)
    return df


def create_map(df):
    # Create a base map
    heat_m = folium.Map(location=[40.416, -3.694],
                        tiles='cartodbpositron', zoom_start=16)

    # Add a heatmap to the base map
    HeatMap(data=df[['Lat', 'Lon']], radius=15).add_to(heat_m)

    return heat_m


def print_heat_map(coll):
    bicis = coll.acc.find()
    accidents = create_df_coords(bicis)
    heat_map = create_map(accidents)
    heat_map.save(f'output/heat_map.html')
    return heat_map


def print_heat_map_h(coll, interh):
    bicis = coll.acc.find({"horario": interh})
    accidents = create_df_coords(bicis)
    heat_map = create_map(accidents)
    heat_map.save(f'output/heat_map_{interh}.html')
    return heat_map
