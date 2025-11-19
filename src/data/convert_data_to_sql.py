import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
import pandas as pd 

DATA_PATH = 'data/raw/weatherAUS.csv'
SAVE_PATH = 'data/raw/weather_australia.db'
TABLE_NAME='weather_table'

os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

df = pd.read_csv(DATA_PATH)

# NaN to None
df = df.where(pd.notnull(df), None)

# column_names={
#     'Date': String(),
#     'Location': String(),
#     'MinTemp': Float(),
#     'MaxTemp': Float(),
#     'Rainfall': Float(),
#     'Evaporation': Float(),
#     'Sunshine': Float(),
#     'WindGustDir': String(),
#     'WindGustSpeed': Float(),
#     'WindDir9am': String(),
#     'WindDir3pm': String(),
#     'WindSpeed9am': Float(),
#     'WindSpeed3pm': Float(),
#     'Humidity9am': Float(),
#     'Humidity3pm': Float(),
#     'Pressure9am': Float(),
#     'Pressure3pm': Float(),
#     'Cloud9am': Float(),
#     'Cloud3pm': Float(),
#     'Temp9am': Float(),
#     'Temp3pm': Float(),
#     'RainToday': String(),
#     'RainTomorrow': String()
# }

def save_data_sql(df, SAVE_PATH, TABLE_NAME):
    try:
    engine = create_engine(f'sqlite:///{SAVE_PATH}')
    df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)
    print(f"Data has been successfully converted and stored in '{SAVE_PATH}' as table '{TABLE_NAME}'.")
    except: 
    print(f"Error! '{TABLE_NAME}' could not be sucessfully converted into a database.")

if __name__ == "__main__":
    save_data_sql(df, SAVE_PATH, TABLE_NAME)
