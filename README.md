# Short-Term Carbon Intensity Forecasting

**Type:** Master's Thesis 

**Author:** Carl Tramburg




**1st Examiner:** Dr. Alona Zharova

**2nd Examiner:** Prof. Dr. Stefan Lessmann 

<!--- This is an HTML comment in Markdown
![results](/Tennet_HomeAssistant.png)
<img src="/Tennet_HomeAssistant.png" width="50%">
-->
<p>
  <img src="/results.png" width="49%" style="margin-right: 2%;">
  <img src="/Tennet_HomeAssistant.png" width="49%">
</p>


## Table of Content

- [Summary](#summary)
- [Working with the repo](#Working-with-the-repo)
    - [Dependencies](#Dependencies)
    - [Setup](#Setup)
- [Reproducing results](#Reproducing-results)
- [Results](#Results)
- [Project structure](-Project-structure)

## Summary

**Keywords**: smart home, carbon emissions, forcasting, temporal fusions transformers, 50Hertz, Aprion, Tennet, Transnet 

**Full text**: 
Short-term carbon intensity forecasting is crucial for optimizing energy consumption towards carbon emissions. This thesis focuses on predicting carbon intensity across the four German Transmission System Operators (TSO) zones: 50Hertz, Amprion, Tennet, and TransnetBW. The data sets are enriched by weather and market price data. The accuracies of ARIMA, SARIMA, and Temporal Fusion Transformer (TFT) models is assessed in all four regions. Results indicate that the univariate SARIMA model consistently outperforms both ARIMA and TFT models across all TSO zones, utilizing an input window of 28 days and a forecast length of 24 hours.
Additionally, this study presents a smart home solution designed to provide users with real-time carbon intensity forecasts. The visualization in Home Assistant and the backend are developed in an open-source microservice architecture approach, allowing for flexible adjustments and integration of various forecasting methods.

## Working with the repo

### Dependencies

This repository contains the Juypter notebooks in Python Version 3.10.10. 

The packages, required to run the code, are provided in [requirements.txt](requirements.txt).

In order to retrieve the energy market data from [ENTSOE](https://transparency.entsoe.eu/), a personal token is required and must be requested [here](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation).

Docker is required to deploy the real-time smart home application.

### Setup

1a. Data and models - Create an environment and install requirements
```bash
conda create -n "my_env" python=3.10.10
conda activate my_env
Pip install —upgrade pip
pip install -r requirements.txt
pip install --user ipykernel
python -m ipykernel install --user --name=$MYENV$

```

2b. Implementation with Home Assistant and FastAPI

Note: Before starting the application, please update API-Key (Line16) [here](/docker/calculations/src/last28days_crawler.py)

```bash
docker compose -f docker/compose.yaml up -d --build
```

## Reproducing results

1 [Data collection:](01_DataCollection.ipynb)
 - Data collection of power generation data and day-ahead prices from ENTSO-E and weather data from DWD per TSO zone

2 [Data preparation:](02_DataPreparation.ipynb)
- Missing value handling
- Feature creation

3 [Data analyis:](03_DataAnalysis.ipynb)
- data Description and insights

4 Model assessment:
- model training, evaluation
- [ARIMA](04_ARIMA.ipynb)
- [SARIMA](05_SARIMA.ipynb)
- TFT (4 notebooks)

5 [Results:](07_Results.ipynb)


## Project structure


```bash
├── README.md
├── requirements.txt                                    -- required packages
├── 01_DataCollection.ipynb                             -- Data retrieval
├── 02_DataPreparation.ipynb                            -- Data cleaning, NA handling     
├── 03_DataAnalysis.ipynb                               --      
├── 04_ARIMA.ipynb                                      --  
├── 05_SARIMA.ipynb                                     --  
├── 06_TFT_50HZ.ipynb                                   -- TFT model of 50Hertz
├── 06_TFT_AMPRION.ipynb                                -- TFT model of Amprion    
├── 06_TFT_TENNET.ipynb                                 -- TFT model of Tennet
├── 06_TFT_TRANSNET.ipynb                               -- TFT model of TransnetBW
├── 07_Results.ipynb                                    -- results collection and calculation
└──data
    └── data_DE_$TSOzone$.parquet                       -- final data set of each zone
    ├── test_$TSOzone$.parquet                          -- Test data set for each zone
    ├── arima_results_test_$TSOzone$.parquet            -- evaluation result ARIMA
    ├── sarima_results_test_$TSOzone$_400_40024.parquet -- evaluation result SARIMA
    └── tft_results_test_$TSOzone$.parquet              -- evaluation result TFT

└── docker
    └── calculations                                    -- data collection and forecast
    ├── fastapi                                         -- communication
    └── homeassistant                                   -- smart home and visualization

└── best_tft_models                                     -- best models from TFT training
    └── BEST_tft_50hertz_epoch=14-step=8370.ckpt        -- best model 50Hertz
    ├── Best_tft_amprion_epoch=12-step=7254.ckpt        -- best model Amprion
    ├── Best_tft_tennet_epoch=10-step=6138.ckpt         -- best model Tennet
    └── Best_tft_transnet_epoch=14-step=8370.ckpt       -- best model TransnetBW      
```
