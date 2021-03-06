from flask import Flask, request, render_template
import pymongo
import pandas as pd

from atlas_mongo.Mongo import ConectColl
import atlas_mongo.folium_maps as fmaps
import atlas_mongo.external_api as exa
import machine.prepare_data as mppd
import machine.sandro_rey as sandro

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hi Ovi!'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/home')
def home_two():
    return render_template('home.html')


@app.route('/create', methods=['POST'])
def create():
    fecha = request.form.get('fecha')
    year = int(request.form.get('year'))
    horario = request.form.get('horario')
    festividad = request.form.get('festividad')
    tipo_accidente = request.form.get('tipo_accidente')
    lesividad = request.form.get('lesividad')
    meteo = request.form.get('meteo')
    distrito = request.form.get('distrito')
    direccion = request.form.get('direccion')
    lon = round(float(request.form.get('lon')), 6)
    lat = round(float(request.form.get('lat')), 6)
    coll.create(fecha, year, horario, festividad, tipo_accidente,
                lesividad, meteo, distrito, direccion, lon, lat)
    coll.acc.create_index([('localizacion', pymongo.GEOSPHERE)])
    return 'Doc Inserted'

# ----
@app.route('/create/pred', methods=['POST'])
def create_pred():
    lon = round(float(request.form.get('lon')), 6)
    lat = round(float(request.form.get('lat')), 6)
    weight = round(float(request.form.get('weights')), 1)
    coll.create_pred(lon, lat, weight)
    coll.pred.create_index([('localizacion', pymongo.GEOSPHERE)])
    return 'Pred Inserted'
# -----


@app.route('/historical/direction', methods=['GET'])
def insert_dir():
    return render_template('historical.html')


@app.route('/historical/direction', methods=['POST'])
def get_coord_dir():
    pto_a = request.form.get('pto_a')
    pto_b = request.form.get('pto_b')
    lat_a, lon_a = exa.get_coord_dir(pto_a)
    lat_b, lon_b = exa.get_coord_dir(pto_b)
    folium_map = fmaps.print_heat_map_dir(coll, lat_a, lon_a, lat_b, lon_b)
    return folium_map._repr_html_()


# Predicciones y buenas noches

@app.route('/prediction/direction', methods=['GET'])
def insert_dir_pred():
    weather, day = exa.get_weather_day()
    fest = mppd.get_fest(day)
    return render_template('prediction.html', vble_w=weather, vble_d=day, vble_f=fest)


@app.route('/prediction/direction', methods=['POST'])
def get_coord_dir_pred():
    pto_a = request.form.get('pto_a')
    pto_b = request.form.get('pto_b')
    horario_cat = request.form.get('horario')

    lat_a, lon_a = exa.get_coord_dir(pto_a)
    lat_b, lon_b = exa.get_coord_dir(pto_b)
    weather, day = exa.get_weather_day()

    data = mppd.prepare_to_predict(
        horario_cat, day, lon_a, lat_a, lon_b, lat_b, weather)
    # data.to_csv('output/X_to_pred.csv', index=False)
    data_to_map = sandro.pred_y_buenas_noches(data)

    folium_map = fmaps.print_heat_map_pred(
        data_to_map, lat_a, lon_a, lat_b, lon_b)
    return folium_map._repr_html_()


if __name__ == '__main__':
    coll = ConectColl()
    app.run(debug=True)
