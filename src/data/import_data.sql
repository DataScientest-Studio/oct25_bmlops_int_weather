SET sql_mode=''; -- needs to be activated

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/weatherAUS.csv'
INTO TABLE weather_data
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Date, Location, MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine,
 WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm, WindSpeed9am,
 WindSpeed3pm, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm,
 Cloud9am, Cloud3pm, Temp9am, Temp3pm, RainToday, RainTomorrow)
SET 
  MinTemp       = NULLIF(TRIM(MinTemp), 'NA'),
  MaxTemp       = NULLIF(TRIM(MaxTemp), 'NA'),
  Rainfall      = NULLIF(TRIM(Rainfall), 'NA'),
  Evaporation   = NULLIF(TRIM(Evaporation), 'NA'),
  Sunshine      = NULLIF(TRIM(Sunshine), 'NA'),
  WindGustSpeed = NULLIF(TRIM(WindGustSpeed), 'NA'),
  WindSpeed9am  = NULLIF(TRIM(WindSpeed9am), 'NA'),
  WindSpeed3pm  = NULLIF(TRIM(WindSpeed3pm), 'NA'),
  Humidity9am   = NULLIF(TRIM(Humidity9am), 'NA'),
  Humidity3pm   = NULLIF(TRIM(Humidity3pm), 'NA'),
  Pressure9am   = NULLIF(TRIM(Pressure9am), 'NA'),
  Pressure3pm   = NULLIF(TRIM(Pressure3pm), 'NA'),
  Cloud9am      = NULLIF(TRIM(Cloud9am), 'NA'),
  Cloud3pm      = NULLIF(TRIM(Cloud3pm), 'NA'),
  Temp9am       = NULLIF(TRIM(Temp9am), 'NA'),
  Temp3pm       = NULLIF(TRIM(Temp3pm), 'NA'),
  WindGustDir   = NULLIF(TRIM(WindGustDir), 'NA'),
  WindDir9am    = NULLIF(TRIM(WindDir9am), 'NA'),
  WindDir3pm    = NULLIF(TRIM(WindDir3pm), 'NA'),
  RainToday     = NULLIF(TRIM(RainToday), 'NA'),
  RainTomorrow  = NULLIF(TRIM(RainTomorrow), 'NA');
  
SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'; -- deactivated