import pandas as pd

URL = "https://www.data.gouv.fr/fr/datasets/r/182268fc-2103-4bcb-a850-6cf90b02a9eb"

def load_data(url=URL):
    return pd.read_csv(url, low_memory=False)

def prepare_data(df):
    df = df.copy()

    df["code_departement"] = df["code_departement"].astype(str).str.zfill(2)
    df["code_commune"] = df["code_commune"].astype(str).str.zfill(3)
    df["code_commune"] = df["code_departement"] + df["code_commune"]

    df["prenom"] = df["prenom"].fillna("").astype(str).str.strip()
    df["nom"] = df["nom"].fillna("").astype(str).str.strip()
    df["candidat"] = (df["prenom"] + " " + df["nom"]).str.strip()

    return df

def get_exprimes(df):
    return df.loc[~df["candidat"].isin(["Abstentions", "Blancs", "Nuls"])].copy()