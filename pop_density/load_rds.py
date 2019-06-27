from sqlalchemy import create_engine, MetaData, Table, and_
import os
import click
from dotenv import load_dotenv
import geopandas as gpd


@click.command()
@click.option('--input', help="a .geojson with adm0_code, adm1_code, adm2_code, sum", default='pop_admin_asia.geojson')
def loader(input):
    """ script to load the population data into a PostGIS instance. """

    # load secrets
    if not load_dotenv(): raise Exception("no .env found")
    load_dotenv()

    # set up connection to DB
    engine = create_engine('postgresql://{UID}:{PWD}@{SERVER}:5432/{DB}'.format(
        UID=os.getenv('RDS_UID'),
        PWD=os.getenv('RDS_PWD'),
        SERVER=os.getenv('RDS_SERVER'),
        DB=os.getenv('RDS_DATABASE')
    ))

    connection = engine.connect()
    metadata = MetaData()
    tbl = Table('global_adm2', metadata, autoload=True, autoload_with=engine)

    # load pop data in memory
    assert os.path.exists(input)
    data = gpd.read_file(input).dropna()

    # loop over geometries and load
    for ix, row in data.iterrows():
        query = tbl.update(). \
            where(and_(tbl.c.adm2_code == row['adm2_code'],
                       tbl.c.adm1_code == row['adm1_code'])
                  ).values(dict(
            pop_sum=row['sum'],
            pop_mean = row['mean'])
        )

        connection.execute(query)


if __name__ == '__main__':
    # run
    loader()