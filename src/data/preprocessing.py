import pandas as pd
import numpy as np
import os


# define vector normalization
def vector_normalize(X):
    ''' Normalize the data using vector normalization
    '''
    X_np= np.nan_to_num(X.values.astype(float))
    norms = np.linalg.norm(X_np, axis=1, keepdims=True)
    # avoid dividing zero
    norms[norms == 0] = 1e-10
    X_normalized = X_np /norms
    return pd.DataFrame(X_normalized, columns=X.columns)

# define preprocesing
def preprocessing(INPUT_FILE, DATE) -> str:
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    df= pd.read_csv(INPUT_FILE).dropna(how='all')
    # correct import
    if df['RainTomorrow'].dtype == object:
        df['RainTomorrow'] = df['RainTomorrow'].str.strip()
        df['RainTomorrow'] = df['RainTomorrow'].replace({'NA': np.nan})
 
    #################
    #Handeling Nans

    # ADDED: drop Date
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])

    # drop nans in target
    df = df.dropna(subset=['RainTomorrow'])

    # Get categorical variables
    s = (df.dtypes == "object")
    object_cols = list(s[s].index)

    # fill missing values of categorical values with mode
    for i in object_cols:
        df[i].fillna(df[i].mode()[0], inplace=True)
    
    # Get numerical variables
    num_cols = df.select_dtypes(include=['float64']).columns

    # fill missing values of numeric variables with median
    for i in num_cols:
        df[i].fillna(df[i].median(), inplace=True)
    
    # vector normalization for numerical columns

    X_norm = vector_normalize(df[num_cols])  # falls noch NaNs drin sind
    X_norm.index = df.index  # sicherstellen, dass Index passt
    df[num_cols] = X_norm

    # Encode categorical features with get_dummies
    
    EXCLUDE = ["RainTomorrow", "RainToday"]

    df_encoded = pd.get_dummies(
        df.drop(columns=EXCLUDE),
        dtype=float
    )

    # Add again RainTomorrow and RainToday
    df_encoded["RainTomorrow"] = df["RainTomorrow"]
    df_encoded["RainToday"] = df["RainToday"]

  
    # Replace RainToday and Raintomorrow with Booleans 
    # ADDED: assign the replacements back to the columns
    # avoid FutureWarning message
    df_encoded['RainToday'] = df_encoded['RainToday'].replace({'No': False, 'Yes': True}).infer_objects(copy=False)
    df_encoded['RainTomorrow'] = df_encoded['RainTomorrow'].replace({'No': False, 'Yes': True}).infer_objects(copy=False)
    

    #############
    #Exporting file
    
    OUTPUT_DIR = os.path.join(THIS_DIR, "../../data/processed")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_FILE = f'{OUTPUT_DIR}/weatherAUS_preprocessed_{DATE}.csv'
    df_encoded.to_csv(OUTPUT_FILE, index=False)
    print("Preprocessing done")

    return OUTPUT_FILE



if __name__ == "__main__":
    preprocessing()
