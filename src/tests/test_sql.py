import pandas as pd
from sqlalchemy import Float, MetaData, String, Table, create_engine, inspect, select, text

SQL_PATH = 'data/raw/weather_australia.db'
TABLE_NAME = 'weather_table'

column_names={
    'Date': String(),
    'Location': String(),
    'MinTemp': Float(),
    'MaxTemp': Float(),
    'Rainfall': Float(),
    'Evaporation': Float(),
    'Sunshine': Float(),
    'WindGustDir': String(),
    'WindGustSpeed': Float(),
    'WindDir9am': String(),
    'WindDir3pm': String(),
    'WindSpeed9am': Float(),
    'WindSpeed3pm': Float(),
    'Humidity9am': Float(),
    'Humidity3pm': Float(),
    'Pressure9am': Float(),
    'Pressure3pm': Float(),
    'Cloud9am': Float(),
    'Cloud3pm': Float(),
    'Temp9am': Float(),
    'Temp3pm': Float(),
    'RainToday': String(),
    'RainTomorrow': String()
}


def test_connection(SQL_PATH, TABLE_NAME ):
    engine = create_engine(f'sqlite:///{SQL_PATH}')

    inspector = inspect(engine)
    print("table_name:", inspector.get_table_names())

    metadata = MetaData()
    metadata.reflect(bind=engine) 
    table = Table(TABLE_NAME, metadata, autoload_with=engine)

    with engine.connect() as conn:
        result = conn.execute(select(table))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    print(df.head())

    # test parameters
    # check for correct column names
    expected_columns = set(column_names.keys())
    actual_columns = set(df.columns)
    
    if expected_columns == actual_columns:
        column_status = "SUCCESS! All expected columns are present."
    else:
        missing = expected_columns - actual_columns
        extra = actual_columns - expected_columns
        column_status = f"FAILURE! Missing columns: {missing}, Extra columns: {extra}"

    # colums types
    type_status_list = []
    for col, dtype in column_names.items():
        if col in table.c:
            actual_dtype = str(table.c[col].type).upper()
            expected_dtype = str(dtype).upper()
            
            # SQLite speichert String() intern als TEXT
            if expected_dtype in ["VARCHAR", "STRING"]:
                expected_dtype = "TEXT"
            
            if actual_dtype == expected_dtype:
                type_status_list.append(f"SUCCESS! Column {col} has correct type {actual_dtype}.")
            else:
                type_status_list.append(f"FAILURE! Column {col} has type {actual_dtype}, expected {expected_dtype}.")
        else:
            type_status_list.append(f"FAILURE! Column {col} not found for type check.")
                
    output = f'''
    ============================
            SQL Test
    ============================
    Column check:
    {column_status}

    Type check:
    {"\n".join(type_status_list)}
    ============================
    '''
    print(output)
    
if __name__ == "__main__":
    test_connection(SQL_PATH, TABLE_NAME)
