Predicting Rain in Australia
==============================

Project Aim
------------
The aim of the project is to predict if it will rain tomorrow based on todays weather.

Data Exploration
------------
The given Dataset from Australia has 23 different columns and contains 145460 data entrys.
The target column is RainTomorrow, which is a Boolean. The target is unevenly distibuted (fewer rainy days).
The Data for today contains information about the date, the city, temperature, humidity, pressure, wind, clouds, sunshine and rain. Most variables are numeric. Categorical values are the location , wind related values (e.g. wind direction). Rains today is a boolean.
The dataset contains measurements from 49 citys/places.

Missing values in %
Date              0.000000
Location          0.000000
MinTemp           1.020899
MaxTemp           0.866905
Rainfall          2.241853
Evaporation      43.166506
Sunshine         48.009762
WindGustDir       7.098859
WindGustSpeed     7.055548
WindDir9am        7.263853
WindDir3pm        2.906641
WindSpeed9am      1.214767
WindSpeed3pm      2.105046
Humidity9am       1.824557
Humidity3pm       3.098446
Pressure9am      10.356799
Pressure3pm      10.331363
Cloud9am         38.421559
Cloud3pm         40.807095
Temp9am           1.214767
Temp3pm           2.481094
RainToday         2.241853
RainTomorrow      2.245978

How  to proceed with missing values: 
- delete entrys with over 10% of missing values
- replace Nans for cateforical variables with mode
- replace Nans for numerical variables with median

First Observation
------------
If it rains today, there is 50% chance that it also rains tomorrow. If it does not rain today, it will most likely also not rain tomorrow.

Preprocessing data
------------
- How  to proceed with missing values: 
    - delete entrys with over 10% of missing values
    - replace Nans for cateforical variables with mode
    - replace Nans for numerical variables with median
- delete Date column since it is not used for modelling (note from Reviewer: Not sure yet about this, at least it is probably reduntant since it is highly correlated with the other values.)
- encode RainToday and RainTomorrow in binary variable (0/1) (note from Reviewer: Or as Boolean (True/False), maybe we will choose a binary decision tree)
- encode location and variables for wind direction with get_dummies
- Should we include Scaling? (note from Reviewer, most likely yes, I would propose a vector normalization or Min/Max normalization


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── visualize.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

Step SQL)
Task: store data in a local database (SQL)
Solution: src/data/convert_data_to_sql.py 
-> takes the big weatherAUS.cvs from this source: https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package?resource=download
-> converts it into a table called weather_table in weather_australia.db and saev it in data/raw
src/test.sql.py 
-> checks for missing/extra columns and the right data type in the table (so far float or string)
src/data/make_dataset.py
-> loads the sql, ignores specific columns and simply filter (e.g the location) the big database. The results will be saved in data/raw
--note: for first instances the data folder and the database are not gitignored!!