import pandas as pdf

def clean_data(path: str, dump: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path, delimiter=",", quotechar='"', on_bad_lines="error", engine="python")
    # Mal schaun vllt muss man sowas wie das Attribut Cabin ganz rausnehmen, da es zu wenig Werte gibt.
    # Und dann noch ein feld hinzufügen Kind (true oder false) was man entweder aus dem alter oder aus dem titel Zieht.

    if dump:
        df.to_csv("cleaned_titanic.csv", index=False)
    return df