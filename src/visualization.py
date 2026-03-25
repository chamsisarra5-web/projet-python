import matplotlib.pyplot as plt

def plot_top_surrepresentations(df_scores, candidat, top_n=10):
    temp = df_scores.loc[df_scores["candidat"] == candidat].copy()
    temp = temp.sort_values("surrepresentation", ascending=False).head(top_n)
    temp = temp.sort_values("surrepresentation")

    plt.figure(figsize=(8, 6))
    plt.barh(temp["code_departement"], temp["surrepresentation"])
    plt.xlabel("Surreprésentation (%)")
    plt.ylabel("Code département")
    plt.title(f"Top {top_n} des surreprésentations de {candidat}")
    plt.axvline(0)
    plt.tight_layout()
    plt.show()