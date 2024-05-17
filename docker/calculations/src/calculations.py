import time
import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
#from last28days_crawler import call_last28days
from last28days_crawler import *
import warnings

warnings.filterwarnings(
    "ignore",
    message=".*map_elements.*"
)
# Dictionary containing items to iterate over
TSO_dict = {
    "DE_50HZ": "DE_50HZ",
    "DE_AMPRION": "DE_AMPRION",
    "DE_TENNET": "DE_TENNET",
    "DE_TRANSNET": "DE_TRANSNET"}
##################ARIMA ############################
def arima_calculation(TSO_zone):
    print(f"ARIMA4{TSO_zone}")
    logging.warning(f"ARIMA4{TSO_zone}")
    # call data from the last 28 days
    last28days = call_last28days(TSO_zone)

    # Prepare the data for ARIMA
    df_CI_series = last28days[["CO2_intensity_in_gCO2_per_KWh","time_idx"]]
    df_CI_series.index = df_CI_series["time_idx"].apply(lambda x: timeidx2time(x))
    df_CI_series.index.freq = 'h'
    CI_series = df_CI_series["CO2_intensity_in_gCO2_per_KWh"]

    # train ARIMA
    pmd_arima = auto_arima(CI_series, start_q=0, seasonal=False)
    model_order = pmd_arima.get_params().get("order")
    print(model_order)
    # Fit the ARIMA model
    model = ARIMA(CI_series, order=model_order)
    model_fit = model.fit()
    # Forecast next 24 hours
    forecast = model_fit.forecast(steps=24)

    CI_series.name = 'actual'
    forecast.name = 'forecast'
    inputAndForecast = pd.concat([CI_series[-48:],forecast],axis=1)

    #inputAndForecast = pd.concat([CI_series,forecast])
    CI_series.name = 'actual'
    forecast.name = 'forecast'
    inputAndForecast = pd.concat([CI_series[-48:],forecast],axis=1)

    return inputAndForecast

    # inputAndForecast["timestamp"] = inputAndForecast.index.to_series().dt.strftime('%Y-%m-%dT%H:%MZ')
    # inputAndForecast.fillna(0, inplace=True)
    # #inputAndForecast
    # nested_data = []
    # for index, row in inputAndForecast.iterrows():
    #     nested_item = {
    #         "from": row["timestamp"],
    #         "intensity": {
    #             "forecast": row["forecast"],
    #             "actual": row["actual"]  # Make sure this column exists in your DataFrame
    #         }
    #     }
    #     nested_data.append(nested_item)

    # # Check the resulting nested data
    # print(f"last elemt: {nested_data[-1]}")

    # return {"data": nested_data}
while True:
    for i in TSO_dict:
        try:
            # Perform calculations and then wait for an hour (3600 seconds)
            x = arima_calculation(i)
            x.to_csv(f"/shared_data/{i}_forecast.csv")
            print(x)
            time.sleep(10)
        except Exception as e:
            # Handle any other exception that isn't specifically caught
            print(f"An unexpected error occurred: {e}")
            time.sleep(5)
    time.sleep(300)



# while True:
#     # Write results to the shared file
#     with open('/shared_data/results.txt', 'w') as f:
#         for key, numbers in data.items():
#             total = sum(numbers)
#             f.write(f"{key}: Sum = {total}\n")
#         f.write("Completed one iteration.\n")
    
#     # Pause for a second before the next iteration
#     time.sleep(1)
