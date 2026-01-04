-- Create weather_data table in weather_db database
USE weather_db;
-- Define the columns and their data types
CREATE TABLE weather_data (
    Date DATE,
    Location VARCHAR(255),
    MinTemp FLOAT,
    MaxTemp FLOAT,
    Rainfall FLOAT,
    Evaporation FLOAT,
    Sunshine FLOAT,
    WindGustDir VARCHAR(10),
    WindGustSpeed FLOAT,
    WindDir9am VARCHAR(10),
    WindDir3pm VARCHAR(10),
    WindSpeed9am FLOAT,
    WindSpeed3pm FLOAT,
    Humidity9am FLOAT,
    Humidity3pm FLOAT,
    Pressure9am FLOAT,
    Pressure3pm FLOAT,
    Cloud9am FLOAT,
    Cloud3pm FLOAT,
    Temp9am FLOAT,
    Temp3pm FLOAT,
    RainToday VARCHAR(5),
    RainTomorrow VARCHAR(5)
);
