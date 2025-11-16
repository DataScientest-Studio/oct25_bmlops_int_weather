import pandas as pd
from sqlalchemy import create_engine

SQL_PATH = 'data/raw/weather_australia.db'
TABLE_NAME = 'weather_table'

engine = create_engine(f'sqlite:///{SQL_PATH}')

columns_to_load = [ # comment the columns you want to drop
    'Date', 
    'Location', 
    'MinTemp', 
    'MaxTemp', 
    'Rainfall',
    #'Evaporation',
    #'Sunshine',
    'WindGustDir',
    'WindGustSpeed',
    'WindDir9am',
    'WindDir3pm',
    'WindSpeed9am',
    'WindSpeed3pm',
    'Humidity9am',
    'Humidity3pm',
    'Pressure9am',
    'Pressure3pm',
    #'Cloud9am',
    #'Cloud3pm',
    'Temp9am',
    'Temp3pm',
    'RainToday',
    'RainTomorrow'
    ]

#filter query eg.loacation (Canberra, Sydney, Melbourne, Brisbane, Adelaide)
'''
all locations:
'Albury' 'BadgerysCreek' 'Cobar' 'CoffsHarbour' 'Moree' 'Newcastle'
 'NorahHead' 'NorfolkIsland' 'Penrith' 'Richmond' 'Sydney' 'SydneyAirport'
 'WaggaWagga' 'Williamtown' 'Wollongong' 'Canberra' 'Tuggeranong'
 'MountGinini' 'Ballarat' 'Bendigo' 'Sale' 'MelbourneAirport' 'Melbourne'
 'Mildura' 'Nhil' 'Portland' 'Watsonia' 'Dartmoor' 'Brisbane' 'Cairns'
 'GoldCoast' 'Townsville' 'Adelaide' 'MountGambier' 'Nuriootpa' 'Woomera'
 'Albany' 'Witchcliffe' 'PearceRAAF' 'PerthAirport' 'Perth' 'SalmonGums'
 'Walpole' 'Hobart' 'Launceston' 'AliceSprings' 'Darwin' 'Katherine'
 'Uluru']
 '''
query = f"SELECT {', '.join(columns_to_load)} FROM {TABLE_NAME} WHERE Location='Sydney'"

df = pd.read_sql(query, engine)

df.to_csv('data/raw/sydney_weather.csv', index=False)