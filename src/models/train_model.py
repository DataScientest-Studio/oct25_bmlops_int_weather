import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


###################################################
def training():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(THIS_DIR, "../../models")
    MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
    FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")
    PROCESSED_PATH = os.path.join(THIS_DIR, "../../data/processed/weatherAUS_10percent_preprocessed.csv")

    # initialize mlflow experiment
    mlflow.set_tracking_uri("http://localhost:8080") 
    mlflow.set_experiment("MLflow Tracking-Weather Australia_10percent")
    mlflow.sklearn.autolog()

    df = pd.read_csv(PROCESSED_PATH)

    print("data is loaded.")

    # drop index column if it exists
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    y = df["RainTomorrow"].astype(int)   
    X = df.drop(columns=["RainTomorrow"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=7, stratify=y
    )

    X_train_np = X_train.values
    X_test_np = X_test.values
    y_train_np = y_train.values # need to convert for autologging
    y_test_np = y_test.values
    print("train-test split is done.")

    # Define baseline models
    # models = {
    #     "KNeighbors": KNeighborsClassifier(n_neighbors=10), "DecisionTree": DecisionTreeClassifier(random_state=0), "RandomForest": RandomForestClassifier(n_estimators=10, random_state=5), "GradientBoosting": GradientBoostingClassifier(random_state=10),}
    models = {
        "KNeighbors": KNeighborsClassifier(n_neighbors=10, n_jobs=1),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=1),
        "GradientBoosting": GradientBoostingClassifier(random_state=42),
        }

    with mlflow.start_run(run_name="weather_10percent_best_model"):
        first_model = True
        for name, model in models.items():
            model.fit(X_train_np, y_train_np)
            y_pred = model.predict(X_test_np)

            acc = accuracy_score(y_test_np, y_pred)

            prec = precision_score(y_test_np, y_pred)

            rec = recall_score(y_test_np, y_pred)

            f1 = f1_score(y_test_np, y_pred)

            print(f"\nModel: {name}")
            print(f"  Accuracy : {acc}")
            print(f"  Precision: {prec}")
            print(f"  Recall   : {rec}")
            print(f"  F1-score : {f1}")

            if first_model:
                best_name, best_acc, best_prec, best_rec, best_f1, best_model = name, acc, prec, rec, f1, model
                first_model = False
            else:
                # Choose best model by F1-score
                if f1 > best_f1:
                    best_name, best_acc, best_prec, best_rec, best_f1, best_model = name, acc, prec, rec, f1, model

        # log best model
        mlflow.sklearn.log_model(sk_model=best_model, name="best_model")

        # log best model metrics
        mlflow.log_metric("accuracy", best_acc)
        mlflow.log_metric("precision", best_prec)
        mlflow.log_metric("recall", best_rec)
        mlflow.log_metric("f1_score", best_f1)

    mlflow.set_tag("Training Info", "best model for Weather Australia data")

    print("\nBest model (by F1-score):")
    print("  Name     : {best_name}")

    # Save best model and feature list
    # os.makedirs("models", exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(best_model, MODEL_PATH)

    joblib.dump(list(X.columns), FEATURES_PATH)
    print("best model is saved.")
    print("training is finished.")

#####################################################


# if __name__ == "__main__":
#     train_model()
