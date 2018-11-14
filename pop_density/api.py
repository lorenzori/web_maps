# -*- coding: utf-8 -*-
"""
API exposes the geoJson with populaiton density by admin area.
"""

from flask import Flask, Response, render_template
from flask_restful import Api, Resource
from rasterstats import zonal_stats
import json
import requests

# get the data from the bucket
print('getting data from Bucket ...')
r = requests.get('https://population-density-data.ams3.digitaloceanspaces.com/AFR_PPP_2020_adj_v2.tif')
open('tmp_satser.tif', 'wb').write(r.content)
r = requests.get('https://population-density-data.ams3.digitaloceanspaces.com/geometry.geojson')
open('geometry.geojson', 'wb').write(r.content)
print('downloaded.')
app = Flask(__name__)
api = Api(app)


# summarize the pop density raster within vector layer
print('calculating values per admin ...')
stats = zonal_stats('geometry.geojson', 'tmp_satser.tif', stats=['sum', 'mean'], geojson_out=True)
pop_by_adm = {"type": "FeatureCollection","features": stats}

with open('pop_admin.geojson', 'w') as f:
    json.dump(pop_by_adm, f)

@app.route('/data', methods=['GET'])
def return_data():
  return json.dumps(pop_by_adm)
#class ReturnData(Resource):
#    def get(self):

#        return Response(
#            response=json.dumps(pop_by_adm),
#            mimetype='application/json',
#            status=200)

@app.route('/')
def home():
  return render_template('index.html')

#api.add_resource(ReturnData, '/data')


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
