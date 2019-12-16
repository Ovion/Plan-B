from flask import Flask
from atlas_mongo.Mongo import ConectColl

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hi Ovi!'


@app.route('/create', methods=['POST'])
def create():
    year = request.args['year']
    lat = request.args['lat']
    lon = request.args['lon']
    coll.create(year, lat, lon)
    return 'Doc Inserted'


if __name__ == '__main__':
    coll = ConectColl()
    app.run(debug=True)
