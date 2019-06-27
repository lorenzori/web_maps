from fastapi import FastAPI
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table
import geopandas as gp

app = FastAPI()

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/population/{country}")
def read_item(country: str):
    print('in function')
    query = tbl.select(). \
        where(tbl.c.adm0_name == country)

    result = gp.GeoDataFrame.from_postgis(query, engine)
    print('fetched {} datapoints.'.format(len(result)))

    return {"result": result.to_json()}
