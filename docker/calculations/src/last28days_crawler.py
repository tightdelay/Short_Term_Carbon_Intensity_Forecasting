#import relevant packages
from entsoe import EntsoePandasClient
import pandas as pd
import numpy as np
import datetime as dt
import pytz
import concurrent.futures
import logging
from sklearn.preprocessing import FunctionTransformer
from wetterdienst.provider.dwd.observation import (DwdObservationRequest, 
                                                   DwdObservationPeriod, 
                                                   DwdObservationResolution, 
                                                   DwdObservationParameter, 
                                                   DwdObservationDataset) # =Observation data (historical data)

API_KEY = "55c76530-b737-48af-bf6e-40d4ebde04f2"

request_parameter = ['radiation_global',
    'sunshine_duration',
    'temperature_air_mean_200',
    'temperature_dew_point_mean_200',
    'wind_direction',
    'wind_speed']

df_50HZ_predict = pd.DataFrame()
df_AMPRION_predict = pd.DataFrame()
df_TENNET_predict = pd.DataFrame()
df_TRANSNET_predict = pd.DataFrame()

Mapping_dict = {
    "DE_50HZ": {
        "name": "DE_50HZ",
        "dwd_stationid": "03987",
        "df_predict": df_50HZ_predict
    },
    "DE_AMPRION": {
        "name": "DE_AMPRION",
        "dwd_stationid": "4336",
        "df_predict": df_AMPRION_predict
    },
    "DE_TENNET": {
        "name": "DE_TENNET",
        "dwd_stationid": "3668",
        "df_predict": df_TENNET_predict
    },
    "DE_TRANSNET": {
        "name": "DE_TRANSNET",
        "dwd_stationid": "2712",
        "df_predict": df_TRANSNET_predict
    }
}

# Entsoe API Call to retrieve datad
def get_TSO_generation_data(geozone, start, end):
    client = EntsoePandasClient(api_key=API_KEY)
    start = pd.Timestamp(start, tz='Europe/Berlin')
    end = pd.Timestamp(end, tz='Europe/Berlin')
    return client.query_generation(geozone, start=start,end=end, psr_type=None)

# Transformation to hourly and erasure of consumption columns    
def cleanup_generation_data(df_to_be_cleaned):
    # following columns also consume power (Hydro, solar, wind Onshore)
    drop_consumption = df_to_be_cleaned.xs('Actual Consumption', level=1, axis=1,drop_level=False).columns
    df_to_be_cleaned.xs('Actual Consumption', level=1, axis=1,drop_level=False).columns
    # therefore get rid of consumption for the fact that consumption does not produce co2
    df_generation_in_MW=df_to_be_cleaned.drop(columns = drop_consumption.tolist())
    #drop header level 1
    df_generation_in_MW.columns= df_generation_in_MW.columns.droplevel(1)
    df_generation_in_MW.head(5)
    #df_generation_in_MW.resample('H', closed='right').sum().reset_index().head(5)
    df_generation_in_MWh = df_generation_in_MW.resample('h').sum()#.reset_index()
    return df_generation_in_MWh
    ##df_generation_in_MW.to_csv("GenerationDE.csv")
#Analyze optimization 
def mixfunc(geozone, start, end):
    return(cleanup_generation_data(get_TSO_generation_data(geozone, start, end)))
#################################################################################
def get_day_ahead_price(geozone, start, end):
    client = EntsoePandasClient(api_key=API_KEY)
    start = pd.Timestamp(start, tz='Europe/Berlin') - - pd.DateOffset(hours=1)
    end = pd.Timestamp(end, tz='Europe/Berlin')
    return client.query_day_ahead_prices(geozone, start=start,end=end)

#################################################################################
def dwd_request_now(request_parameter, station_id):
    request = DwdObservationRequest(
        parameter=request_parameter,
        resolution=DwdObservationResolution.MINUTE_10,
        period=DwdObservationPeriod.NOW
    ).filter_by_station_id(station_id=[station_id])
    return request.values.all().df.to_pandas()

aggregations = {
    'radiation_global' : 'sum',
    'sunshine_duration': 'sum',
    'temperature_air_mean_200': 'mean',
    'temperature_dew_point_mean_200': 'mean',
    'wind_direction': 'mean',
    'wind_speed': 'mean'
}

def concatenate_df_now(station_id):
    df_list=[]
    for req in request_parameter:
        #print(req)
        egal = dwd_request_now(req, station_id)
        #egal = dwd_request_now(req,station_id)#.head(1))
        egal = egal.set_index("date")
        egal = egal.rename(columns={"value":req})
        egal = egal.drop(columns=["station_id","dataset","parameter","quality"])
        df_list.append(egal)
        x = pd.concat(df_list, axis=1)
    return x.resample('1h').agg(aggregations)
#.resample('1h').agg(aggregations)a

def dwd_request_recent(request_parameter, start, end, station_id):
    request = DwdObservationRequest(
                parameter=request_parameter,
                #resolution=DwdObservationResolution.HOURLY,
                resolution=DwdObservationResolution.HOURLY,
                period=DwdObservationPeriod.RECENT,
                #start_date=start,
                #end_date=end,
    ).filter_by_station_id(station_id=[station_id])
    return request.values.all().df.to_pandas()
#################################################################################
def concatenate_df_recent(station_id, start, end):
    df_list=[]
    for req in request_parameter:
        #print(req)
        egal = dwd_request_recent(request_parameter=req,start=start, end=end, station_id=station_id)
        #egal = dwd_request_now(req,station_id)#.head(1))
        egal = egal.set_index("date")
        egal = egal.rename(columns={"value":req})
        egal = egal.drop(columns=["station_id","dataset","parameter","quality"])
        df_list.append(egal)
        x = pd.concat(df_list, axis=1)###
    return x.resample('1h').agg(aggregations)
    #return pd.concat(df_list, axis=1)
#################################################################################
Co2_intensity={"Biomass" : 230,
"Fossil Brown coal/Lignite" : 966, #source2
"Fossil Coal-derived gas" : 1401, #https://arxiv.org/pdf/2110.07999.pdf, https://www.sciencedirect.com/science/article/pii/S0196890419307496?casa_token=RUR54mu8iKEAAAAA:cZjmcuxK79vyQAm87Y2wDcV9TkzOmWgPNPsAGgkMHw7BYzrOPJp51bkNNEXF03zCRcU0WerWHWs
"Fossil Gas" : 490,
"Fossil Hard coal" : 820,
"Fossil Oil" : 650, #Source3
"Geothermal" : 38 , #source3
"Hydro Pumped Storage" : 281,
"Hydro Run-of-river and poundage" : 24,
"Hydro Water Reservoir" : 24,
"Nuclear" : 12,
"Other" : 700,
"Other renewable" : 100 ,
"Solar" : 45,
"Waste" : 700,
"Wind Offshore" : 12,
"Wind Onshore" : 11
}
#################################################################################
def get_CO2_emission_per_generation(df):
    # Filter the scale_dict to only include keys that exist in the DataFrame's columns
    valid_co2_dict = {k: Co2_intensity[k] for k in df.columns if k in Co2_intensity}
    
    # Create a scaling DataFrame using the filtered dictionary
    co2_factors = pd.DataFrame(index=df.index, columns=df.columns)
    for key, value in valid_co2_dict.items():
        co2_factors[key] = value
    
    # Multiply the DataFrame by the scaling DataFrame
    emissionDF = df.mul(co2_factors, axis=0)
    
    return emissionDF

def extent_df_by_CI_TG_TE(df): # extend df by carbon intensity, total generation, total emisions
    df_emission_in_kgCO2eq = get_CO2_emission_per_generation(df)
    total_CO2_Emission = df_emission_in_kgCO2eq.sum(axis=1)
    total_generation = df.sum(axis=1)
    df.insert(0,"Total_Generation", total_generation)
    df.insert(0,"Total_Emissions_in_kg", total_CO2_Emission)
    df.insert(0,"CO2_intensity_in_gCO2_per_KWh", total_CO2_Emission/total_generation)
    return df
#################################################################################
#################### add co2-values, Total_ren,Total_conv

renewables=['Biomass',  
            'Geothermal', 
            'Hydro Pumped Storage',
            'Hydro Run-of-river and poundage',
            'Hydro Water Reservoir',
            'Other renewable', 
            'Solar',
            'Wind Offshore', 
            'Wind Onshore']

conventionals = ['Fossil Brown coal/Lignite',
                 'Fossil Coal-derived gas',
                 'Fossil Gas',
                 'Fossil Hard coal', 
                 'Fossil Oil',
                 'Nuclear' 
                 'Other',
                 'Nuclear' ,
                 'Waste']


def add_aggregations(df):
    existing_renewables = [source for source in renewables if source in df.columns]
    existing_conventionals = [source for source in conventionals if source in df.columns]

    # Filter for existing columns only
    existing_renewables = [source for source in renewables if source in df.columns]
    existing_conventionals = [source for source in conventionals if source in df.columns]

    # Calculate sums using existing columns
    df["total_ren"] = df[existing_renewables].sum(axis=1)
    df["total_conv"] = df[existing_conventionals].sum(axis=1)
    df["share_ren"] = df["total_ren"]/(df["total_ren"]+df["total_conv"])

    #print("share renewables: ", df["total_ren"].sum().sum()/(df["total_conv"].sum().sum()+df["total_ren"].sum().sum()))
    #print("share conventionals: ", df["total_conv"].sum()/(df["total_conv"].sum().sum()+df["total_ren"].sum().sum()))
    return df
#################################################################################
def sin_transformer(period):
    return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))
def cos_transformer(period):
    return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

# DateTime Features for Forecasting
def add_time_categorical_and_time_idx(df):
    df["sin_day_of_week"] = sin_transformer(7).fit_transform(df.index.dayofweek)
    df["cos_day_of_week"] = cos_transformer(7).fit_transform(df.index.dayofweek)

    df["sin_hour_of_day"] = sin_transformer(24).fit_transform(df.index.hour)
    df["cos_hour_of_day"] = cos_transformer(24).fit_transform(df.index.hour)

    df["sin_day_of_year"] = sin_transformer(356).fit_transform(df.index.day_of_year)
    df["cos_day_of_year"] = cos_transformer(365).fit_transform(df.index.day_of_year)
    
    df["hour_of_day"] = df.index.hour.astype(str).astype("category")
    df["day_of_month"] = df.index.day.astype(str).astype("category")
    df["day_of_year"] = df.index.dayofyear.astype(str).astype("category")
    df["month_of_year"] = df.index.month.astype(str).astype("category")
    df["week_of_year"] = df.index.isocalendar().week.astype(str).astype("category")
    df["day_of_week"] = df.index.dayofweek.astype(str).astype("category")  
    df["quarter_of_year"] = df.index.quarter.astype(str).astype("category")
    
    df["time_idx"] = ((df.index - pd.Timestamp('2015-01-05 00:00:00+0100', tz='Europe/Berlin'))/ np.timedelta64(1, 'h')).astype("int")
    #df.reset_index(drop=True, inplace=True)
    df['GroupKey'] = 'TSO'
    return df
##########################################
def timeidx2time(x):
    return x*np.timedelta64(1, 'h') + pd.Timestamp('2015-01-05 00:00:00+0100', tz='Europe/Berlin')

import concurrent.futures
import logging



def call_last28days(TSO_zone):
    end = dt.datetime.now() - dt.timedelta(hours=1)
    start = end - dt.timedelta(days=28)
    #start_weather = start.tz_convert(tz='UTC')
    #end_weather = end.tz_convert(tz='UTC')
    start_weather = pd.Timestamp(start, tz='Europe/Berlin').tz_convert(tz='UTC') - pd.DateOffset(hours=1)
    end_weather = pd.Timestamp(end, tz='Europe/Berlin').tz_convert(tz='UTC')
    geozone = Mapping_dict[TSO_zone]["name"]
    station_id = Mapping_dict[TSO_zone]["dwd_stationid"]

    request_parameter = ['radiation_global',
    'sunshine_duration',
    'temperature_air_mean_200',
    'temperature_dew_point_mean_200',
    'wind_direction',
    'wind_speed']

    param_mixfunc = [geozone, start, end]
    param_get_day_ahead_price =["DE_LU", start- dt.timedelta(hours=12), end]
    param_concatenate_df_now = [station_id]
    param_concatenate_df_recent = [station_id,start_weather, end_weather]

    # Use ThreadPoolExecutor to run multiple functions concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit each function to be executed in parallel
        parallel_last28days = executor.submit(mixfunc, *param_mixfunc)
        parallel_last28days_dap = executor.submit(get_day_ahead_price, *param_get_day_ahead_price)
        parallel_weather_last24h = executor.submit(concatenate_df_now, *param_concatenate_df_now)
        parallel_weather_last28days = executor.submit(concatenate_df_recent, *param_concatenate_df_recent)

        # Wait for all futures to complete and collect results
        results = {
            "last28days": parallel_last28days.result(),
            "last28days_dap": parallel_last28days_dap.result(),
            "weather_last24h": parallel_weather_last24h.result(),
            "weather_last28days": parallel_weather_last28days.result()
        }

    last28days = results["last28days"]
    last28days_dap = results["last28days_dap"]
    weather_last24h = results["weather_last24h"]
    weather_last28days = results["weather_last28days"]

    #####
    extent_df_by_CI_TG_TE(last28days)

    #weather_last28days.update(weather_last24h)
    concat_weather = pd.concat([weather_last28days,weather_last24h],axis=0,join='inner')

    last28days = last28days.join(last28days_dap.to_frame(name="day_ahead_price"), how="left")
    df_predict = last28days.join(concat_weather, how='left')
    # verschieben: df_predict.index.tz_convert(tz='Europe/Berlin')
    df_predict.index = df_predict.index.tz_convert(tz='Europe/Berlin')
    logging.warning('concat 4 df')

    #####
    add_aggregations(df_predict)
    #####
    df_predict_parallel = add_time_categorical_and_time_idx(df_predict)
    #####
    #telegram_message("workflow done")
    #####
    return df_predict_parallel