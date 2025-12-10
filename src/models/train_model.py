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
def training() -> mlflow.models.model.ModelInfo: 
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(THIS_DIR, "../../models")
    FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")
    PROCESSED_PATH = os.path.join(THIS_DIR, "../../data/processed/weatherAUS_10percent_preprocessed.csv")

    # initialize mlflow experiment; allow override via env for Docker
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8080"))
    experiment = mlflow.get_experiment_by_name("MLflowTrackingWeatherAustralia_10percent")
    if experiment is None:
        experiment_id = mlflow.create_experiment("MLflowTrackingWeatherAustralia_10percent")
    else:
        experiment_id = experiment.experiment_id
    mlflow.set_experiment(experiment_id=experiment_id)
    # mlflow.sklearn.autolog()

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
    params = {
        "KNeighbors": {"n_neighbors": 10},
        "DecisionTree": {"max_depth": 10, "random_state": 42},
        "RandomForest": {"n_estimators": 10, "max_depth": 10, "random_state": 42},
        "GradientBoosting": {"random_state": 42},
    }
    models = {
        "KNeighbors": KNeighborsClassifier(**params["KNeighbors"]),
        "DecisionTree": DecisionTreeClassifier(**params["DecisionTree"]),
        "RandomForest": RandomForestClassifier(**params["RandomForest"]),
        "GradientBoosting": GradientBoostingClassifier(**params["GradientBoosting"]),
        }

    # with mlflow.start_run(run_name="weather_20percent_best_model") as parent_run:
    first_model = True
    for name, model in models.items():
        # with mlflow.start_run(run_name=name, nested=True) as child_run:
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


    with mlflow.start_run(run_name="weather_10percent_best_model") as run:
        mlflow.log_params(params[best_name])
        # log best model metrics
        mlflow.log_metric("accuracy", best_acc)
        mlflow.log_metric("precision", best_prec)
        mlflow.log_metric("recall", best_rec)
        mlflow.log_metric("f1_score", best_f1)
        # log best model
        model_info = mlflow.sklearn.log_model(sk_model=best_model,
                                              name="best_model",
                                              input_example=X_train_np[:1])

    print("best model is saved.")

    mlflow.set_tag("Training Info", "best model for Weather Australia data")

    print("\nBest model (by F1-score):")
    print(f"  Name     : {best_name}")

    joblib.dump(list(X.columns), FEATURES_PATH)
    print("training is finished.")

    return model_info

#####################################################


if __name__ == "__main__":
    training()
