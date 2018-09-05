# -*- coding: utf-8 -*-
"""
API that returns the values of the shapes given a date. Ex:
curl http://localhost:5000/data/2018-06-23
"""

from flask import Flask, Response
from flask_restful import Api, Resource
import geopandas as gpd

app = Flask(__name__)
api = Api(app)

gdf = gpd.read_file('export.geojson')


class return_data(Resource):
    def get(self):

        t = gdf.to_json()

        print(t)
        return Response(
            response=t,
            mimetype='application/json',
            status=200)

api.add_resource(return_data, '/data')


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
