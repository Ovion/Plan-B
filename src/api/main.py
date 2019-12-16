from flask import Flask, request
from atlas_mongo.Mongo import ConectColl

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hi Ovi!'


@app.route('/create', methods=['POST'])
def create():
    year = int(request.form.get('year'))
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    coll.create(year, lat, lon)
    return 'Doc Inserted'


if __name__ == '__main__':
    coll = ConectColl()
    app.run(debug=True)
