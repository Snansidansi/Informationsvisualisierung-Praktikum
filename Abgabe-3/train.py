import pandas as pd
import numpy as np
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_validate, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import resample
from sklearn.metrics import check_scoring
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

models = {
    "Logistische Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, solver="liblinear")),
    "Decision Tree": DecisionTreeClassifier(random_state=1),
    "K-Nearest Neighbor mit k = 3": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3)),
}

def train_10fold(df: pd.DataFrame, dump: bool = False):
    X = df.drop(columns="Survived")
    y = df["Survived"]
    
    kfold = KFold(n_splits=10, random_state=1, shuffle=True)

    rows = []
    
    predictions = {}
    fitted_models = {}

    for name, model in models.items():
        scoring = {
            "accuracy": "accuracy",
            "precision": "precision",
            "recall": "recall",
            "f1": "f1",
        }
        kf = cross_validate(model, X, y, cv=kfold, scoring=scoring)

        rows.append({
            "Klassifizierer":name,
            "Genauigkeit": kf["test_accuracy"].mean(),
            "Genauigkeit Std": kf["test_accuracy"].std(),
            "Präzision": kf["test_precision"].mean(),
            "Recall": kf["test_recall"].mean(),
            "F1": kf["test_f1"].mean(),
        })
        
        y_pred_cv = cross_val_predict(model, X, y, cv=kfold)
        predictions[name] = y_pred_cv
        
        fitted_model = clone(model).fit(X, y)
        fitted_models[name] = fitted_model

    results = pd.DataFrame(rows)
    if (dump):
        print(results)
    return results, predictions, fitted_models

def train_bootstrap_632(df: pd.DataFrame, dump: bool = False) -> pd.DataFrame:
    X = df.drop(columns="Survived")
    y = df["Survived"]

    bootstrap = Bootstrap()

    rows = []

    for name, model in models.items():
        bs = cross_validate(model, X, y, cv=bootstrap, scoring="accuracy")
        bs_oob_score = bs["test_score"].mean()
        fitted = clone(model).fit(X, y)
        chk = check_scoring(model, scoring="accuracy")
        bs_score = chk(fitted, X, y)
        bs_632_score = 0.368 * bs_score + 0.632 * bs_oob_score
        
        rows.append({
            "Klassifizierer": name,
            "Bootstrap 0.632": bs_632_score,
        })

    results = pd.DataFrame(rows)
    if (dump):
        print(results)
    return results

class Bootstrap:
    def __init__(self, n_splits=100, random_state=None):
        self.n_splits = n_splits
        self.random_state = random_state

    def split(self, X, y=None, groups=None):
        rng = np.random.RandomState(self.random_state)
        n = len(X)
        idx = np.arange(n)

        for _ in range(self.n_splits):
            train_idx = resample(
                idx,
                replace=True,
                n_samples=n,
                random_state=rng.randint(0, 2**31 - 1),
            )

            test_mask = np.ones(n, dtype=bool)
            test_mask[train_idx] = False
            test_idx = idx[test_mask]

            if len(test_idx):
                yield train_idx, test_idx

    def get_n_splits(self, X=None, y=None, groups=None):
        return self.n_splits

if __name__ == "__main__":
    from datenbereinigung import clean_data
    df = clean_data("Titanic.csv")
    res_cv, preds_cv, models_cv = train_10fold(df, dump=True)
    train_bootstrap_632(df, dump=True)
