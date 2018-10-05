# -*- coding: utf-8 -*-
"""
API exposes the geoJson with populaiton density by admin area.
"""

from flask import Flask, Response
from flask_restful import Api, Resource
from rasterstats import zonal_stats
import json

# global variables
GEOMETRY_FILE = "geometry.geojson"
WORLDPOP_RASTER = "AFR_PPP_2020_adj_v2.tif"


app = Flask(__name__)
api = Api(app)


# summarize the pop density raster within vector layer
stats = zonal_stats(GEOMETRY_FILE, WORLDPOP_RASTER, stats=['sum', 'mean'], geojson_out=True)
pop_by_adm = {"type": "FeatureCollection","features": stats}


class return_data(Resource):
    def get(self):

        return Response(
            response=json.dumps(pop_by_adm),
            mimetype='application/json',
            status=200)

api.add_resource(return_data, '/data')


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
