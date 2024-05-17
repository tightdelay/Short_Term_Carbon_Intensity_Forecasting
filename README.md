# Short-Term Carbon Intensity Forecasting

**Type:** Master's Thesis 

**Author:** Carl Tramburg




**1st Examiner:** Dr. Alona Zharova

**2nd Examiner:** Prof. Dr. Stefan Lessmann 



[Insert here a figure explaining your approach or main results]

![results](/result.png)

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

(Short summary of motivation, contributions and results)

**Keywords**: smart home, carbon emissions, forcasting, temporal fusions transformers, 50Hertz, Aprion, Tennet, Transnet 

**Full text**: [include a link that points to the full text of your thesis]
*Remark*: a thesis is about research. We believe in the [open science](https://en.wikipedia.org/wiki/Open_science) paradigm. Research results should be available to the public. Therefore, we expect dissertations to be shared publicly. Preferably, you publish your thesis via the [edoc-server of the Humboldt-Universität zu Berlin](https://edoc-info.hu-berlin.de/de/publizieren/andere). However, other sharing options, which ensure permanent availability, are also possible. <br> Exceptions from the default to share the full text of a thesis require the approval of the thesis supervisor.  

## Working with the repo

### Dependencies

Which Python version is required? 

Does a repository have information on dependencies or instructions on how to set up the environment?

### Setup

[This is an example]

1. Clone this repository

2a. Model and Data - Create an virtual environment and activate it and install requirements
```bash
conda env create -f environment.yml
source thesis-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2b. Implementation with Home Assistant and FastAPI

```bash
docker compose -f src/docker/compose.yaml up -d --build
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
