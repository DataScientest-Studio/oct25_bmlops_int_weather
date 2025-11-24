import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")



###################################################
def main():
    df = pd.read_csv("data/processed/weatherAUS_preprocessed.csv")


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

    # Define baseline models
    models = {
        "KNeighbors": KNeighborsClassifier(n_neighbors=10), "DecisionTree": DecisionTreeClassifier(random_state=0), "RandomForest": RandomForestClassifier(n_estimators=10, random_state=5), "GradientBoosting": GradientBoostingClassifier(random_state=10),}


    results = []

    for name, model in models.items():
        model.fit(X_train_np, y_train)

        y_pred = model.predict(X_test_np)

        acc = accuracy_score(y_test, y_pred)

        prec = precision_score(y_test, y_pred)

        rec = recall_score(y_test, y_pred)

        f1 = f1_score(y_test, y_pred)

        print(f"\nModel: {name}")
        print(f"  Accuracy : {acc}")
        print(f"  Precision: {prec}")
        print(f"  Recall   : {rec}")
        print(f"  F1-score : {f1}")

        results.append((name, acc, prec, rec, f1, model))

    # Choose best model by F1-score
    best_name, best_acc, best_prec, best_rec, best_f1, best_model = max(results, key=lambda x: x[4])

    print("\nBest model (by F1-score):")
    print(f"  Name     : {best_name}")

    # Save best model and feature list
    os.makedirs("models", exist_ok=True)

    joblib.dump(best_model, MODEL_PATH)

    joblib.dump(list(X.columns), FEATURES_PATH)

#####################################################

if __name__ == "__main__":
    main()
