import pandas as pd
import numpy as np

#############
#Read file

df= pd.read_csv(r"data\raw\weatherAUS.csv")

#################
#Handeling Nans

# droping columns with 11% and more missing values

df= df.drop(["Evaporation","Sunshine","Cloud9am","Cloud3pm"], axis=1)

# Get categorical variables
s = (df.dtypes == "object")
object_cols = list(s[s].index)

# fill missing values of categorical values with mode
for i in object_cols:
    df[i].fillna(df[i].mode()[0], inplace=True)

# Get numerical variables
t = (df.dtypes == "float64")
num_cols = list(t[t].index)

# fill missing values of numeric variables with median
for i in num_cols:
    df[i].fillna(df[i].median(), inplace=True)

# drop date column to not include in modelling
df.drop(columns = ['Date'], inplace = True)

#############
# Encoding

# Replace RainToday and Raintomorrow with binary values (0:no rain, 1:rain)
df['RainToday'].replace({'No': 0, 'Yes': 1},inplace = True)
df['RainTomorrow'].replace({'No': 0, 'Yes': 1},inplace = True)

# Encode with get_dummies
df = pd.get_dummies(df, dtype=float)

#############
# Should we add Scaling?

#############
#Exporting file
df.to_csv(r"data\processed\weatherAUS_preprocessed.csv")