import pandas as pd

def clean_data(path: str, dump: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path, delimiter=",", quotechar="'", on_bad_lines="error", engine="python")
    df = df.fillna("").astype(str).apply(lambda col: col.str.strip(".")) # strip trailing dots
    df = df.apply(pd.to_numeric, errors="raise").round(2) # round to 2 decimals
    outliers = (df > 100 * df.mean()).any(axis=1) # remove extreme outliers
    if dump:
        print("Removed rows:")
        print(df[outliers].to_string())
    df = df[~outliers]
    if dump:
        df.to_csv("cleaned.csv", index=False)
    return df

if __name__ == "__main__":
    clean_data("wein.csv", dump=True)
