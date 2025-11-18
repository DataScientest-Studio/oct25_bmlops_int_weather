import pandas as pd
import numpy as np



def vector_normalize(X):
    ''' Normalize the data using vector normalization
    '''
    X_np = X.values.astype(float)
    norms = np.linalg.norm(X_np, axis=1, keepdims=True)
    X_normalized = X_np /norms
    return pd.DataFrame(X_normalized, columns=X.columns)

#############
#Read file

df= pd.read_csv(r"data\raw\weatherAUS.csv")

#################
#Handeling Nans
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

#############
# Encoding

# Replace RainToday and Raintomorrow with Booleans 
df['RainToday'].replace({'No': False, 'Yes': True})
df['RainTomorrow'].replace({'No': False, 'Yes': True})

# Encode with get_dummies
df = pd.get_dummies(df, dtype=float)

#############
# vector normalization as an example

num_cols = df.select_dtypes(include=[np.number]).columns # only  columns with numbers
df[num_cols] = vector_normalize(df[num_cols])



#############
#Exporting file
df.to_csv(r"data\processed\weatherAUS_preprocessed.csv")
