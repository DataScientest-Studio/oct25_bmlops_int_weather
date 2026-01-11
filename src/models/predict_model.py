import os
import mlflow
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import pandas as pd
from typing import Optional
import logging
from io import StringIO


##################################################

def predict(model_info: mlflow.models.model.ModelInfo,
            input_path: Optional[str] = None, 
            output_path: Optional[str] = None,
            callback: Optional[callable] = None):
    log_stream = StringIO()
    logger = logging.getLogger("predict_model")
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicates if called multiple times
    logger.handlers = []
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

    logger.info("Starting prediction...")

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
    logger.info("Loading model from MLFlow...")
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

    logger.info(f"Generated {len(y_pred)} predictions")

    if callback:
        callback(80, "Evaluating...")

    # If labals exist, print metrics
    if y_true is not None:
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred)
        rec = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        logger.info("\nEvaluation on this model:")
        logger.info(f"  Accuracy : {acc}")
        logger.info(f"  Precision: {prec}")
        logger.info(f"  Recall   : {rec}")
        logger.info(f"  F1-score : {f1}")

        cm =confusion_matrix(y_true, y_pred)
        labels = ["No Rain", "Rain"] 
        clabels = ["No Rain Pred.", "Rain Pred."] 
        df_cm = pd.DataFrame(cm, index=labels, columns=clabels)

        logger.info("\nConfusion Matrix:")
        logger.info(df_cm.to_string())
        
    else:
        logger.info("No RainTomorrow column found")

    if callback:
        callback(90, "Saving predictions...")
    result = df.copy()
    result["RainTomorrow_pred"] = y_pred.astype(bool)
    result.to_csv(output_path, index=False)

    logger.info("Prediction completed successfully!")

    if callback:
        callback(100, log_stream.getvalue())

######################################################

