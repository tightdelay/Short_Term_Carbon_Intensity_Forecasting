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
    - [Training code](#Training-code)
    - [Evaluation code](#Evaluation-code)
    - [Pretrained models](#Pretrained-models)
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

1a. Data and Model - Create an environment and install requirements
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
 -  Download power generation data and day-ahead price from Entso-E Transparency (only with [authorized API token](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation))
 - 

1. [Data Collection]

Here are some examples:
- [Paperswithcode](https://github.com/paperswithcode/releasing-research-code)
- [ML Reproducibility Checklist](https://ai.facebook.com/blog/how-the-ai-community-can-get-serious-about-reproducibility/)
- [Simple & clear Example from Paperswithcode](https://github.com/paperswithcode/releasing-research-code/blob/master/templates/README.md) (!)
- [Example TensorFlow](https://github.com/NVlabs/selfsupervised-denoising)

### Training code

Does a repository contain a way to train/fit the model(s) described in the paper?

### Evaluation code

Does a repository contain a script to calculate the performance of the trained model(s) or run experiments on models?

### Pretrained models

Does a repository provide free access to pretrained model weights?

## Results

Does a repository contain a table/plot of main results and a script to reproduce those results?

## Project structure

(Here is an example from SMART_HOME_N_ENERGY, [Appliance Level Load Prediction](https://github.com/Humboldt-WI/dissertations/tree/main/SMART_HOME_N_ENERGY/Appliance%20Level%20Load%20Prediction) dissertation)

```bash
├── README.md
├── requirements.txt                                -- required libraries                                            -- stores csv file 
├── plots                                           -- stores image files
└── src
    └── data
        ├── 01_DataCollection.ipynb                 -- data collection
        ├── 02_DataPreparation.ipynb                -- preparing dataset 
        └── 03_DataAnalysis.ipynb                   -- data analysis
    └── model
        ├── 01_baseline.ipynb                       -- preprocesses data
        ├── 02_TFT_transfomrer.ipynb                -- preparing datasets
        ├── model_tuning.ipynb                      -- tuning functions
        └── run_experiment.ipynb                    -- run experiments 
        └── plots                                   -- plotting functions          
    └── docker                                      -- Home Assistant implementation in Docker       
```
