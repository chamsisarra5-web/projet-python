def count_candidates(df_exprimes):
    return df_exprimes["candidat"].nunique()


def compute_national_scores(df_exprimes):
    total_exprimes = df_exprimes["voix"].sum()

    score_national = (
        df_exprimes.groupby("candidat", as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "votes_national"})
    )

    score_national["score_national"] = (
        100 * score_national["votes_national"] / total_exprimes
    )

    score_national = score_national.sort_values(
        by="votes_national",
        ascending=False
    ).reset_index(drop=True)

    return score_national


def compute_department_scores(df_exprimes):
    total_dep = (
        df_exprimes.groupby("code_departement", as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "total_exprimes_departement"})
    )

    score_dep = (
        df_exprimes.groupby(["code_departement", "candidat"], as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "votes_departement"})
    )

    score_dep = score_dep.merge(total_dep, on="code_departement", how="left")

    score_dep["score_departement"] = (
        100 * score_dep["votes_departement"] / score_dep["total_exprimes_departement"]
    )

    return score_dep


def add_national_scores(score_departements, score_national):
    return score_departements.merge(score_national, on="candidat", how="left")


def add_surrepresentation(score_departements):
    df = score_departements.copy()
    df["surrepresentation"] = (
        100 * (df["score_departement"] - df["score_national"]) / df["score_national"]
    )
    return df