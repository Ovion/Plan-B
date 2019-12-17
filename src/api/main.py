from flask import Flask, request
import pymongo
from atlas_mongo.Mongo import ConectColl
import atlas_mongo.folium_maps as fmaps

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hi Ovi!'


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


@app.route('/historical')
def historical():
    folium_map = fmaps.print_heat_map(coll)
    return folium_map._repr_html_()


@app.route('/historical/horario/<interh>')
def historical_hour(interh):
    folium_map = fmaps.print_heat_map_h(coll, interh)
    return folium_map._repr_html_()


@app.route('/historical/lesividad/<injury>')
def historical_injury(injury):
    folium_map = fmaps.print_heat_map_i(coll, injury)
    return folium_map._repr_html_()


if __name__ == '__main__':
    coll = ConectColl()
    app.run(debug=True)
