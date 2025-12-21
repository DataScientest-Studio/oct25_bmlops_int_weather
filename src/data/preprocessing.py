import pandas as pd
import numpy as np
import os



def vector_normalize(X):
    ''' Normalize the data using vector normalization
    '''
    X_np = X.values.astype(float)
    norms = np.linalg.norm(X_np, axis=1, keepdims=True)
    # avoid dividing zero
    norms[norms == 0] = 1e-10
    X_normalized = X_np /norms
    return pd.DataFrame(X_normalized, columns=X.columns)


def preprocessing(INPUT_FILE, DATE) -> str:
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    df= pd.read_csv(INPUT_FILE) 
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
    # ADDED: assign the replacements back to the columns
    # avoid FutureWarning message
    df['RainToday'] = df['RainToday'].replace({'No': False, 'Yes': True}).infer_objects(copy=False)
    df['RainTomorrow'] = df['RainTomorrow'].replace({'No': False, 'Yes': True}).infer_objects(copy=False)
    
    #############
    # vector normalization as an example
    
    num_cols = df.select_dtypes(include=[np.number]).columns # only  columns with numbers
    df[num_cols] = vector_normalize(df[num_cols])
    
    # ADDED: drop Date
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])
    
    # Encode with get_dummies
    df = pd.get_dummies(df, dtype=float)
    
    
    
    #############
    #Exporting file
    
    OUTPUT_DIR = os.path.join(THIS_DIR, "../../data/processed")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_FILE = f'{OUTPUT_DIR}/weatherAUS_preprocessed_{DATE}.csv'
    df.to_csv(OUTPUT_FILE, index=False)
    print("Preprocessing done")

    return OUTPUT_FILE



if __name__ == "__main__":
    preprocessing()
