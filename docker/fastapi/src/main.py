from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict
import pandas as pd
import numpy as np
from datetime import datetime as dt, timedelta 
from entsoe import EntsoePandasClient
import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
#from .functions import *
#from .CO2_dict import *
#from .last28day_crawler import *

###packages for geo_to_TSOzone####
import requests
from shapely.geometry import shape, Point, Polygon,GeometryCollection
import geopandas as gpd
import numpy as np
import json


def initial_market_zone_load():
    geo_dict={
    "DE_50HZ"    :{"name" : "DE_50HZ", "source_url" :     'https://raw.githubusercontent.com/tightdelay/Germany_EnergyGrid_DataSources/main/GeoJson/50Hertz.geo.json', "geometry": None}, 
    "DE_AMPRION" :{"name" : "DE_AMPRION", "source_url" :  'https://raw.githubusercontent.com/tightdelay/Germany_EnergyGrid_DataSources/main/GeoJson/Amprion.geo.json', "geometry": None}, 
    "DE_TENNET"  :{"name" : "DE_TENNET", "source_url" :   'https://raw.githubusercontent.com/tightdelay/Germany_EnergyGrid_DataSources/main/GeoJson/TenneT.geo.json', "geometry": None}, 
    "DE_TRANSNET":{"name" : "DE_TRANSNET", "source_url" : 'https://raw.githubusercontent.com/tightdelay/Germany_EnergyGrid_DataSources/main/GeoJson/TransnetBW.geo.json', "geometry": None} 
    }

    geo_dict["DE_50HZ"]["geometry"] = GeometryCollection([shape(feature["geometry"]).buffer(0) for feature in requests.get(geo_dict["DE_50HZ"]["source_url"]).json()["features"]])
    geo_dict["DE_AMPRION"]["geometry"] = Polygon = shape(requests.get(geo_dict["DE_AMPRION"]["source_url"]).json()["features"][0]["geometry"])
    geo_dict["DE_TENNET"]["geometry"] = Polygon = shape(requests.get(geo_dict["DE_TENNET"]["source_url"]).json()["features"][0]["geometry"])
    geo_dict["DE_TRANSNET"]["geometry"] = Polygon = shape(requests.get(geo_dict["DE_TRANSNET"]["source_url"]).json()["features"][0]["geometry"])
    return geo_dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    global geo_dict 
    geo_dict= initial_market_zone_load()
    print("geodict initialized")
    yield #{"geo_dict": geo_dict}
    #await ("cya later")


app = FastAPI(lifespan=lifespan)

#@app.get("/hello_world/")

@app.get("/get_market_zone")
async def get_market_zone(lattidue: float, longitude: float):
    point = Point(longitude, lattidue)
    #geo_dict = geo_dict()
    for key, value in geo_dict.items():
        if geo_dict[key]["geometry"].contains(point):
            print(f"your location({point}) is in market zone {key}")
            return {"location": key, "message": f"your location({point}) is in market zone {key}"}
            #return(f"your location({point}) is in market zone {key}")
    print(f"your location({point}) is not in any market zone (Germany)")
    return{"location": "Error", "message":f"your location({point}) is not in any market zone (Germany)"}


@app.get("/predict_co2_intensity")
async def predict_co2_intensity(lattidue: float, longitude: float):
    country_code = await get_market_zone(lattidue, longitude)
    print(country_code["location"])
    cc = country_code["location"]
    print(f"/shared_data/{cc}_forecast.csv")
    x = pd.read_csv(f"/shared_data/{cc}_forecast.csv", index_col=0, parse_dates=True)
    x["timestamp"] = x.index.to_series().dt.strftime('%Y-%m-%dT%H:%MZ')
    #x.replace([np.inf, -np.inf], np.nan, inplace=True)
    #x.dropna(inplace=True)
    x = x.replace(np.nan, None)
    print(x)


    nested_data = []
    for index, row in x.iterrows():
        nested_item = {
            "from": row["timestamp"],
            "intensity": {
                "forecast": row["forecast"],
                "actual": row["actual"]  # Make sure this column exists in your DataFrame
            }
        }
        nested_data.append(nested_item)
    

    # Check the resulting nested data
    #print(f"last elemt: {nested_data[-1]}")

    return {"data": nested_data}
    #return x.to_json()
 