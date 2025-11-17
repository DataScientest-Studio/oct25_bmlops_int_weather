import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import pandas as pd


##################################################

def predict(input_path: str = "/home/ubuntu/oct25_bmlops_int_weather/data/processed/weatherAUS_preprocessed.csv", 
            output_path: str = "/home/ubuntu/oct25_bmlops_int_weather/data/processed/weather_predictions.csv"):
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(THIS_DIR, "../../models")
    MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
    FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")

    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURES_PATH)

    df = pd.read_csv(input_path)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    if "RainTomorrow" in df.columns:
        y_true = df["RainTomorrow"].astype(int)
        df_features = df.drop(columns=["RainTomorrow"])
    else:
        y_true = None
        df_features = df

    df_features = df_features.reindex(columns=feature_names, fill_value=0)
    X = df_features.values

    # Predict
    y_pred = model.predict(X)

    # If labals exist, print metrics
    if y_true is not None:
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        print("\nEvaluation on this file:")
        print(f"  Accuracy : {acc}")
        print(f"  Precision: {prec}")
        print(f"  Recall   : {rec}")
        print(f"  F1-score : {f1}")
    else:
        print("No RainTomorrow column found")

    result = df.copy()
    result["RainTomorrow_pred"] = y_pred.astype(bool)
    result.to_csv(output_path, index=False)

######################################################


# if __name__ == "__main__":
#     predict()
