import pandas as pd

def clean_data(path: str, dump: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path, delimiter=",", quotechar='"', on_bad_lines="error", engine="python")

    df["PassengerId"] = df["PassengerId"].apply(pd.to_numeric, errors="coerce")

    df["Survived"] = df["Survived"].apply(pd.to_numeric, errors="coerce")

    df["Pclass"] = df["Pclass"].apply(pd.to_numeric, errors="coerce")

    df = df.drop(columns="Name") # nicht relevant

    df["Sex"] = df["Sex"].astype(pd.api.types.CategoricalDtype(["female", "male"]))

    df["Age"] = df["Age"].apply(pd.to_numeric, errors="coerce")
    df["Parch"] = df["Parch"].apply(pd.to_numeric, errors="coerce")
    df["SibSp"] = df["SibSp"].apply(pd.to_numeric, errors="coerce")

    df = df.drop(columns="Ticket") # nicht relevant

    df["Fare"] = df["Fare"].apply(pd.to_numeric, errors="coerce")

    df = df.drop(columns="Cabin") # extrem unvollständig

    df["Embarked"] = df["Embarked"].replace({
        "C":"Cherbourg",
        "Q":"Queenstown",
        "S":"Southampton",
    })
    df["Embarked"] = df["Embarked"].astype(pd.api.types.CategoricalDtype(["Cherbourg", "Queenstown", "Southampton"]))

    df = pd.get_dummies(
        df,
        columns=["Sex", "Embarked"],
        drop_first=True,
        dtype=int
    )

    df = df.rename(columns={
        "PassengerId":"Passenger ID",
        "Pclass":"Passenger class",
        "SibSp":"Number of siblings or spouses aboard",
        "Parch":"Number of parents or children aboard",
        "Fare":"Passenger fare",
        "Embarked":"Port of embarkation",
    })

    df = df.dropna()
    
    if dump:
        df.to_csv("cleaned_titanic.csv", index=False)
    return df

if __name__ == "__main__":
    clean_data("Titanic.csv", dump=True)
