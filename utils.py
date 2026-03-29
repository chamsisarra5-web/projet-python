"""
Fonctions utilitaires pour le DM Python Data Science.
"""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def _require_columns(df: pd.DataFrame, required: Iterable[str], *, df_name: str) -> None:
    """
    Vérifie que le DataFrame contient toutes les colonnes requises.
    """
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise KeyError(f"{df_name} : colonnes manquantes : {missing}")


def plot_surrepresentation(
    score_departements: pd.DataFrame,
    candidat: str,
    *,
    top_n: int = 5,
    scale: float = 100.0,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Représente les principales surreprésentations (en valeur absolue)
    pour un candidat donné.

    Parameters
    ----------
    score_departements : pd.DataFrame
        DataFrame contenant au minimum les colonnes
        'code_departement', 'candidat', 'surrepresentation'.
    candidat : str
        Nom du candidat à représenter.
    top_n : int, default=5
        Nombre de départements à afficher.
    scale : float, default=100.0
        Facteur multiplicatif pour l'affichage (100 = pourcentage).
    ax : matplotlib.axes.Axes, optional
        Axe sur lequel dessiner le graphique.

    Returns
    -------
    matplotlib.axes.Axes
        L'axe contenant le graphique.
    """
    _require_columns(
        score_departements,
        {"code_departement", "candidat", "surrepresentation"},
        df_name="score_departements"
    )

    if top_n <= 0:
        raise ValueError("top_n doit être un entier strictement positif.")

    df_candidat = score_departements.loc[
        score_departements["candidat"] == candidat
    ].copy()

    if df_candidat.empty:
        raise ValueError(f"Candidat introuvable dans score_departements : {candidat!r}")

    df_candidat["abs_surrepresentation"] = df_candidat["surrepresentation"].abs()

    df_plot = (
        df_candidat.sort_values("abs_surrepresentation", ascending=False)
        .head(top_n)
        .sort_values("surrepresentation", ascending=True)
    )

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    y = df_plot["code_departement"].astype(str)
    x = df_plot["surrepresentation"].astype(float) * scale

    ax.barh(y=y, width=x)
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Surreprésentation (%)" if scale == 100.0 else "Surreprésentation")
    ax.set_ylabel("Département")
    ax.set_title(f"Top {top_n} des surreprésentations — {candidat}")
    ax.grid(axis="x", alpha=0.2)
    plt.tight_layout()

    return ax


def carte_candidat(
    score_departements: pd.DataFrame,
    candidat: str,
    fond_carte: pd.DataFrame,
    *,
    scale: float = 100.0,
    insee_dep_col: str = "INSEE_DEP",
    ax: Optional[plt.Axes] = None,
    cmap: str = "RdBu_r",
    symmetric: bool = True,
) -> Tuple[pd.DataFrame, plt.Axes]:
    """
    Filtre les résultats pour un candidat donné, effectue la jointure
    avec le fond de carte des départements, puis trace la carte de
    surreprésentation.

    Returns
    -------
    tuple[pd.DataFrame, matplotlib.axes.Axes]
        Le DataFrame joint et l'axe du graphique.
    """
    _require_columns(
        score_departements,
        {"code_departement", "candidat", "surrepresentation"},
        df_name="score_departements"
    )
    _require_columns(
        fond_carte,
        {insee_dep_col},
        df_name="fond_carte"
    )

    score_candidat = score_departements.loc[
        score_departements["candidat"] == candidat
    ].copy()

    if score_candidat.empty:
        raise ValueError(f"Candidat introuvable dans score_departements : {candidat!r}")

    score_candidat["code_departement"] = score_candidat["code_departement"].astype(str)

    fond = fond_carte.copy()
    fond[insee_dep_col] = fond[insee_dep_col].astype(str)

    carte = fond.merge(
        score_candidat,
        left_on=insee_dep_col,
        right_on="code_departement",
        how="left",
        validate="m:1"
    )

    carte["surrepresentation_plot"] = carte["surrepresentation"].astype(float) * scale

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 10))

    vmin = vmax = None
    if symmetric:
        max_abs = np.nanmax(np.abs(carte["surrepresentation_plot"]))
        if np.isfinite(max_abs):
            vmin, vmax = -max_abs, max_abs

    carte.plot(
        column="surrepresentation_plot",
        ax=ax,
        legend=True,
        cmap=cmap,
        edgecolor="black",
        linewidth=0.3,
        vmin=vmin,
        vmax=vmax,
        missing_kwds={"color": "lightgrey"}
    )

    ax.set_title(f"Surreprésentation de {candidat} par département")
    ax.axis("off")
    plt.tight_layout()

    return carte, ax