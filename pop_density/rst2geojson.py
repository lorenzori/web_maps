import os
import click
os.environ['GDAL_DATA'] = 'C:/Users/lorenzo.riches/anaconda/envs/gdal/Library/share/gdal'
from rasterstats import zonal_stats
import json

@click.command()
@click.option('--input', help="path to .tif with pop data")
@click.option('--geometry', help="path to .shp with geometries")
@click.option('--output', help="path to .geojson with results", default='pop_admin_drc.geojson')
def calculator(raster: str, geometry: str, output: str):
    """
    Script that reads in WorldPop population density rasters and computes the aggregates by amin areas.
    2 files are needed:
        - WorldPop's population density raster, find here: https://www.worldpop.org/project/categories?id=3
        - ADM2 Shapefile for the region relevant to the raster.
    """

    stats = zonal_stats(geometry, raster, stats=['sum', 'mean'], geojson_out=True)
    pop_by_adm = {"type": "FeatureCollection","features": stats}

    with open(output, 'w') as f:
        json.dump(pop_by_adm, f)


if __name__ == '__main__':
    # run
    calculator()