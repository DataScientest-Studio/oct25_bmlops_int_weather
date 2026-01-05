import os
import mlflow
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import pandas as pd
from typing import Optional


##################################################

def predict(model_info: mlflow.models.model.ModelInfo,
            input_path: Optional[str] = None, 
            output_path: Optional[str] = None,
            callback: Optional[callable] = None):
    print("Starting prediction...")
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(THIS_DIR, "../../models")
    FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")
    # defaults for paths
    if input_path is None:
        input_path = os.path.join(THIS_DIR, "../../data/processed/weatherAUS_20percent_preprocessed.csv")
    if output_path is None:
        output_path = os.path.join(THIS_DIR, "../../data/processed/weather_predictions.csv")

    if callback:
        callback(10, "Loading model...")
    model = mlflow.sklearn.load_model(model_info.model_uri)

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

    if callback:
        callback(50, "Predicting...")
    # Predict
    y_pred = model.predict(X)

    if callback:
        callback(80, "Evaluating...")
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

    if callback:
        callback(90, "Saving predictions...")
    result = df.copy()
    result["RainTomorrow_pred"] = y_pred.astype(bool)
    result.to_csv(output_path, index=False)
    print(f"Predictions saved to: {output_path}")

######################################################


# if __name__ == "__main__":
#     predict()
