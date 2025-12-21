from datetime import datetime
import os
import pandas as pd
from sqlalchemy import create_engine, text


# add return valu
def make_dataset() -> tuple[str, str]: 
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_HOST = "weather_sql_container"  # Network? eg my_network
    MYSQL_PORT = 3306
    MYSQL_DB = "weather_db"
    
    
    TABLE_NAME = 'weather_data'
    NEW_TABLE_NAME = 'weather_subset'
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR= os.path.join(THIS_DIR, "../../data/raw") 
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    DATE = datetime.now().strftime("%Y%m%d_%H%M")
    OUTPUT_FILE = f'{OUTPUT_DIR}/weather_subset_{DATE}.csv'
    
    TABLE_PERCENT = 0.2  # x percent of the data

    engine = create_engine(
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    
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
    #query = f"SELECT {', '.join(columns_to_load)} FROM {TABLE_NAME} WHERE Location='Sydney'"
    
    
    # Filter random x % from the data
    with engine.connect() as conn:
        conn.execute(text(
            f"""
            DROP TABLE IF EXISTS {NEW_TABLE_NAME};
            """
        ))
    
    with engine.connect() as conn:
        total_rows = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}")).scalar()
        sample_size = int(total_rows * TABLE_PERCENT)
        conn.execute(text(
            f"""
            CREATE TABLE {NEW_TABLE_NAME} AS
            SELECT *
            FROM {TABLE_NAME}
            ORDER BY RAND()
            LIMIT {sample_size}
            """
        ))
    
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {NEW_TABLE_NAME}")).fetchone()
        print(result)   
    
    
    df = pd.read_sql(f"SELECT * FROM {NEW_TABLE_NAME}", engine)
    
    df.to_csv(OUTPUT_FILE, index=False)

    return OUTPUT_FILE, DATE

if __name__ == "__main__":
    make_dataset()