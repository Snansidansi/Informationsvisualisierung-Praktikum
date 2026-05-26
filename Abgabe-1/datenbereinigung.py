import pandas as pd
import numpy as np

def clean_data(path: str):
    df = pd.read_csv(
            path,
            delimiter=",",
            quotechar="'",
            on_bad_lines=repair_bad_csv_line,
            engine="python"
            )

    df["Positions Played"] = df["Positions Played"].str.split(",")

    textspalten = [
        'Known As', 
        'Full Name', 
        'Positions Played', 
        'Best Position', 
        'Nationality', 
        'Image Link', 
        'Club Name', 
        'Club Position', 
        'Preferred Foot', 
        'National Team Name', 
        'National Team Image Link', 
        'National Team Position', 
        'Attacking Work Rate', 
        'Defensive Work Rate'
        ]

    for col in df.columns:
        if col in textspalten:
            df[col] = df[col].replace("-", "")
        else:
            df[col] = df[col].replace("-", np.nan)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.loc[df["Value(in Euro)"] < 0, "Value(in Euro)"] = 0
    # TODO spalte "On Loan" wird noch nicht korrekt eingelesen

    return df

def repair_bad_csv_line(bad_line):
    # Fix "Value(in Euro)" in line 12922 (1100000,00 € -> 1100000)
    for i, field in enumerate(bad_line):
        if "€" in field and i > 0:
            korrigierter_betrag = bad_line[i-1]
            bad_line = bad_line[:i-1] + [korrigierter_betrag] + bad_line[i+1:]
            break 

    return bad_line
