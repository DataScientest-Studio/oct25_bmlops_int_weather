import os
import mlflow
import glob
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import pandas as pd
from typing import Optional


##################################################

def predict(model_info: mlflow.models.model.ModelInfo,
            input_path: Optional[str] = None, 
            output_path: Optional[str] = None):
    print("Starting prediction...")
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(THIS_DIR, "../../models")
    FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")
    # defaults for paths
    if input_path is None:
        input_path = os.path.join(THIS_DIR, "../../data/processed/weatherAUS_20percent_preprocessed.csv")
    if output_path is None:
        output_path = os.path.join(THIS_DIR, "../../data/processed/weather_predictions.csv")

    model = mlflow.sklearn.load_model(model_info.model_uri)
    # allow MLflow host override (Docker)
    MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8080")
    mlflow.set_tracking_uri(MLFLOW_URI)

    # Load model from local MLflow artifacts (latest model.pkl under mlartifacts)
    artifacts_root = Path(THIS_DIR).resolve().joinpath("..", "..", "mlartifacts")
    candidates = sorted(
        artifacts_root.glob("**/artifacts/model.pkl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise ValueError(
            "No MLflow model artifacts found under mlartifacts/**/artifacts/model.pkl. "
            "Run training first."
        )
    model_path = candidates[0]
    print(f"Loading local model from: {model_path}")
    model = joblib.load(model_path)
    print("Model loaded.")

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
    print(f"Predictions saved to: {output_path}")

######################################################


if __name__ == "__main__":
    predict()
