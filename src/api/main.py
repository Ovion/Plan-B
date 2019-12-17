from flask import Flask, request
import pymongo
from atlas_mongo.Mongo import ConectColl

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


if __name__ == '__main__':
    coll = ConectColl()
    app.run(debug=True)
